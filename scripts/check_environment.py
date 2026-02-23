#!/usr/bin/env python3
"""
Environment readiness checker for the RF Workshop.

Uses ONLY Python standard library — must run even before `uv sync`.
Checks all prerequisites and provides actionable fix instructions.
"""
import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Color helpers (ANSI, disabled on non-TTY / old Windows cmd)
# ---------------------------------------------------------------------------

_USE_COLOR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
if sys.platform == "win32":
    # Enable ANSI on Windows 10+ by trying to set the console mode
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        _USE_COLOR = False

GREEN = "\033[92m" if _USE_COLOR else ""
RED = "\033[91m" if _USE_COLOR else ""
YELLOW = "\033[93m" if _USE_COLOR else ""
BOLD = "\033[1m" if _USE_COLOR else ""
RESET = "\033[0m" if _USE_COLOR else ""

# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

def detect_platform():
    """Return (os_name, arch, is_wsl)."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    is_wsl = False
    if system == "linux":
        try:
            with open("/proc/version", "r") as f:
                content = f.read().lower()
                if "microsoft" in content:
                    is_wsl = True
        except OSError:
            pass
    return system, machine, is_wsl


SYSTEM, ARCH, IS_WSL = detect_platform()

# ---------------------------------------------------------------------------
# Check infrastructure
# ---------------------------------------------------------------------------

class CheckResult:
    def __init__(self, name, passed, required=True, message="", detail=""):
        self.name = name
        self.passed = passed
        self.required = required
        self.message = message
        self.detail = detail  # multi-line fix instructions


results: list[CheckResult] = []


def run_cmd(cmd, timeout=15):
    """Run a shell command, return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return -1, "", "command not found"
    except subprocess.TimeoutExpired:
        return -2, "", "timed out"

# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_python_version():
    v = sys.version_info
    ver_str = f"{v.major}.{v.minor}.{v.micro}"
    if v >= (3, 10):
        msg = f"Python {ver_str}"
        if v < (3, 12):
            msg += " (3.12+ recommended)"
        return CheckResult("Python version", True, message=msg)
    return CheckResult("Python version", False, message=f"Python {ver_str} — need >= 3.10",
        detail="""\
       Python >= 3.10 is required. Python 3.12+ is recommended.

       To install:
         Linux (apt):    sudo apt install python3.12 python3.12-venv
         macOS:          brew install python@3.12
         Windows (WSL):  sudo apt install python3.12 python3.12-venv
         Windows:        Download from https://www.python.org/downloads/

       See: https://www.python.org/downloads/""")


def check_uv():
    path = shutil.which("uv")
    if not path:
        return CheckResult("uv", False, message="NOT FOUND",
            detail="""\
       uv is the package manager used by this project (instead of pip).
       It manages dependencies from pyproject.toml and creates reproducible
       virtual environments via uv.lock.

       To install:
         Linux/macOS:  curl -LsSf https://astral.sh/uv/install.sh | sh
         Windows:      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

       After install, restart your terminal or run:  source ~/.bashrc

       See: https://docs.astral.sh/uv/getting-started/installation/""")
    rc, out, _ = run_cmd(["uv", "version"])
    ver = out.strip() if rc == 0 else "unknown version"
    return CheckResult("uv", True, message=ver)


def check_nodejs():
    path = shutil.which("node")
    if not path:
        return CheckResult("Node.js", False, message="NOT FOUND",
            detail="""\
       Node.js >= 18 is required by Browser Library's Playwright engine.
       Playwright (which powers Browser Library) runs a Node.js server
       process that communicates with browsers via the Chrome DevTools
       Protocol. Without Node.js, tests cannot execute.

       To install:
         Linux (apt):    sudo apt install nodejs npm
         Linux (nvm):    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && nvm install 22
         macOS:          brew install node
         Windows (WSL):  sudo apt install nodejs npm
         Windows:        Download from https://nodejs.org/en/download/

       See: https://nodejs.org/en/download/""")
    rc, out, _ = run_cmd(["node", "--version"])
    if rc != 0:
        return CheckResult("Node.js", False, message="installed but --version failed")
    ver_str = out.lstrip("v")
    try:
        major = int(ver_str.split(".")[0])
        if major < 18:
            return CheckResult("Node.js", False, message=f"v{ver_str} — need >= 18",
                detail="       Upgrade Node.js to version 18 or later (22 LTS recommended).\n"
                       "       See: https://nodejs.org/en/download/")
    except ValueError:
        pass
    return CheckResult("Node.js", True, message=f"v{ver_str}")


def check_venv():
    venv_dir = os.path.join(os.getcwd(), ".venv")
    if not os.path.isdir(venv_dir):
        return CheckResult("Virtual environment", False, message=".venv/ not found",
            detail="""\
       The project virtual environment has not been created yet.
       uv creates it automatically when you install dependencies.

       Run:  uv sync

       This reads pyproject.toml + uv.lock and installs all packages
       into .venv/ with exact pinned versions.""")

    # Check for python executable inside
    if sys.platform == "win32":
        py = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        py = os.path.join(venv_dir, "bin", "python")
    if not os.path.isfile(py):
        return CheckResult("Virtual environment", False,
            message=".venv/ exists but missing python executable",
            detail="       Try removing .venv/ and running: uv sync")
    return CheckResult("Virtual environment", True, message=".venv/ OK")


def check_robot_framework():
    venv_bin = os.path.join(os.getcwd(), ".venv", "bin" if sys.platform != "win32" else "Scripts")
    robot = os.path.join(venv_bin, "robot")
    if not os.path.isfile(robot) and not os.path.isfile(robot + ".exe"):
        return CheckResult("Robot Framework", False, message="not installed in .venv",
            detail="""\
       Robot Framework is not installed in the virtual environment.

       Run:  uv sync

       This will install robotframework and all other project dependencies.""")
    rc, out, err = run_cmd([robot, "--version"])
    version_line = out or err
    return CheckResult("Robot Framework", True, message=version_line.split("\n")[0] if version_line else "installed")


def check_browser_library():
    venv_python = os.path.join(
        os.getcwd(), ".venv",
        "bin" if sys.platform != "win32" else "Scripts",
        "python"
    )
    if not os.path.isfile(venv_python) and not os.path.isfile(venv_python + ".exe"):
        return CheckResult("Browser Library", False, message=".venv python not found",
            detail="       Run: uv sync")
    rc, out, err = run_cmd([venv_python, "-c", "from Browser import __version__; print(__version__)"])
    if rc != 0:
        return CheckResult("Browser Library", False, message="import failed",
            detail="""\
       Browser Library is not installed or cannot be imported.

       Run:  uv sync

       Browser Library provides Playwright-based browser automation for
       Robot Framework. It is the modern alternative to SeleniumLibrary.""")
    return CheckResult("Browser Library", True, message=f"v{out.strip()}" if out.strip() else "installed")


def check_rfbrowser_init():
    """Check if Playwright browser binaries are installed."""
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    home = os.path.expanduser("~")
    candidates = [
        env_path,
        os.path.join(home, ".cache", "ms-playwright"),
        os.path.join(home, "Library", "Caches", "ms-playwright"),
        os.path.join(home, "AppData", "Local", "ms-playwright"),
    ]
    for path in candidates:
        if path and os.path.isdir(path):
            # Look for chromium directory
            for entry in os.listdir(path):
                if entry.startswith("chromium"):
                    return CheckResult("Browser init (Chromium)", True,
                        message=f"found in {path}")
            return CheckResult("Browser init (Chromium)", False,
                message=f"playwright dir exists ({path}) but no chromium found",
                detail="""\
       Playwright browsers directory exists but Chromium is not installed.

       Run:  uv run rfbrowser init chromium

       This downloads Chromium browser binaries (~250MB). It is a one-time
       download and may take a few minutes on slow connections.""")

    return CheckResult("Browser init (Chromium)", False,
        message="no Playwright browsers found",
        detail="""\
       Playwright browser binaries have not been downloaded yet.
       Browser Library needs actual browser binaries to run tests.

       Run:  uv run rfbrowser init chromium

       This downloads Chromium (~250MB). It is a one-time download.
       The binaries are stored in ~/.cache/ms-playwright/ (Linux),
       ~/Library/Caches/ms-playwright/ (macOS), or
       %LOCALAPPDATA%/ms-playwright/ (Windows).""")


def check_git_config():
    rc_name, name, _ = run_cmd(["git", "config", "user.name"])
    rc_email, email, _ = run_cmd(["git", "config", "user.email"])
    issues = []
    if rc_name != 0 or not name:
        issues.append("user.name")
    if rc_email != 0 or not email:
        issues.append("user.email")
    if issues:
        missing = " and ".join(issues)
        return CheckResult("Git configuration", False, message=f"missing {missing}",
            detail=f"""\
       Git {missing} must be set for creating commits.
       These are stored locally and used in commit metadata.

       Run:
         git config --global user.name "Your Name"
         git config --global user.email "your.email@example.com" """)
    return CheckResult("Git configuration", True, message=f"{name} <{email}>")


def check_docker():
    path = shutil.which("docker")
    if not path:
        return CheckResult("Docker", True, required=False,
            message="not installed (optional — only needed for local DevContainer)",
            detail="""\
       Docker is optional. It's only needed if you want to run the
       DevContainer locally instead of using GitHub Codespaces.

       If using Codespaces (recommended), you can skip this.""")
    rc, out, _ = run_cmd(["docker", "info"], timeout=10)
    if rc != 0:
        return CheckResult("Docker", True, required=False,
            message="installed but daemon not running (optional)",
            detail="       Docker is installed but the daemon is not running.\n"
                   "       Start Docker Desktop or run: sudo systemctl start docker")
    return CheckResult("Docker", True, required=False, message="running")


def check_network(url, name):
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "RF-Workshop-EnvCheck/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return CheckResult(f"Network: {name}", True, message=f"reachable ({resp.status})")
    except urllib.error.HTTPError as e:
        # HTTP errors still mean the server is reachable
        return CheckResult(f"Network: {name}", True, message=f"reachable (HTTP {e.code})")
    except Exception as e:
        return CheckResult(f"Network: {name}", False, message=f"unreachable — {e}",
            detail=f"""\
       Cannot reach {url}.
       This may be due to a firewall, proxy, or network issue.

       Verify:
         - You have internet access
         - No corporate proxy is blocking the connection
         - Try opening {url} in a web browser""")

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def print_result(r: CheckResult):
    if r.passed:
        tag = f"{GREEN}[PASS]{RESET}"
    elif r.required:
        tag = f"{RED}[FAIL]{RESET}"
    else:
        tag = f"{YELLOW}[WARN]{RESET}"
    print(f"  {tag} {BOLD}{r.name}{RESET}: {r.message}")
    if not r.passed and r.detail:
        print(r.detail)
        print()


def main():
    os_label = SYSTEM
    if IS_WSL:
        os_label = "WSL (Windows Subsystem for Linux)"
    print(f"\n{BOLD}=== RF Workshop Environment Check ==={RESET}")
    print(f"  Platform: {os_label} ({ARCH})")
    print(f"  Python:   {sys.executable}")
    print(f"  CWD:      {os.getcwd()}")
    print()

    checks = [
        check_python_version,
        check_uv,
        check_nodejs,
        check_venv,
        check_robot_framework,
        check_browser_library,
        check_rfbrowser_init,
        check_git_config,
        check_docker,
        lambda: check_network("https://www.saucedemo.com", "saucedemo.com"),
        lambda: check_network("https://github.com", "github.com"),
    ]

    for check_fn in checks:
        result = check_fn()
        results.append(result)
        print_result(result)

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed_required = [r for r in results if not r.passed and r.required]
    failed_optional = [r for r in results if not r.passed and not r.required]

    print()
    border = "═" * 46
    print(f"  ╔{border}╗")
    print(f"  ║  {'Environment Check:':20s} {passed}/{total} passed{' ' * 14}║")
    if failed_required:
        print(f"  ║  {len(failed_required)} issue(s) need fixing before you start{' ' * 5}║")
    else:
        print(f"  ║  {GREEN}All required checks passed!{RESET}{' ' * 17}║")
    print(f"  ╠{border}╣")
    if failed_required:
        for r in failed_required:
            line = f"  FAIL: {r.name}"
            print(f"  ║  {RED}{line:{44}s}{RESET}║")
    elif failed_optional:
        for r in failed_optional:
            line = f"  WARN: {r.name} (optional)"
            print(f"  ║  {YELLOW}{line:{44}s}{RESET}║")
    else:
        line = "Ready for the workshop!"
        print(f"  ║  {GREEN}{line:{44}s}{RESET}║")
    print(f"  ╚{border}╝")
    print()

    sys.exit(1 if failed_required else 0)


if __name__ == "__main__":
    main()
