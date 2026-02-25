# Windows Setup Guide

## Choose Your Path

| Method | Difficulty | Requirements |
|--------|-----------|-------------|
| **GitHub Codespaces** | Easiest | Web browser + GitHub account |
| **DevContainer (Docker)** | Easy | Docker Desktop + VS Code |
| **Native (WSL2)** | Advanced | WSL2 + manual setup |

**Recommendation:** Use Codespaces for the workshop. It works in your browser.

## Option 1: GitHub Codespaces (Recommended)

This is the easiest option — everything runs in the cloud.

1. Open https://github.com/HackXIt/42vienna-robotframework-workshop
2. Click **"Fork"** → **"Create fork"**
3. On your fork: **"Code"** → **"Codespaces"** → **"Create codespace on main"**
4. Wait ~3-5 minutes for setup
5. In the terminal:
   ```bash
   uv run robot tests/00_setup_verification/
   ```

**Free tier:** 60 hours/month on 2-core machines. More than enough for the workshop.

## Option 2: DevContainer with Docker Desktop

1. **Install Docker Desktop:**
   - Download from https://www.docker.com/products/docker-desktop/
   - During install, enable **WSL 2** backend
   - If prompted, enable Hyper-V or WSL2 in Windows Features

2. **Install VS Code:**
   - Download from https://code.visualstudio.com/

3. **Install Dev Containers extension:**
   - In VS Code: Extensions (Ctrl+Shift+X) → search "Dev Containers" → Install

4. **Clone and open:**
   ```powershell
   git clone https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop.git
   ```
   - Open the folder in VS Code
   - Click **"Reopen in Container"** when prompted (bottom-right notification)

5. **Verify:**
   ```bash
   uv run robot tests/00_setup_verification/
   ```

### Docker Desktop Troubleshooting

- **"WSL 2 is not installed"** → Run `wsl --install` in PowerShell (admin), restart
- **"Virtualization not enabled"** → Enable VT-x/AMD-V in BIOS settings
- **Docker Desktop won't start** → Check Windows Features: "Virtual Machine Platform" and "Windows Subsystem for Linux" must be enabled

## Option 3: Native Setup with WSL2 (Advanced)

1. **Install WSL2:**
   ```powershell
   # In PowerShell (admin):
   wsl --install
   ```
   Restart your computer. Set up Ubuntu when prompted.

2. **Inside WSL2 terminal:**
   ```bash
   # Install Node.js 22 via nvm
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
   source ~/.bashrc
   nvm install 22

   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc

   # Clone the repo (use WSL home, NOT /mnt/c/)
   cd ~
   git clone https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop.git
   cd 42vienna-robotframework-workshop

   # Install dependencies
   uv sync
   uv run rfbrowser init chromium

   # Verify
   python scripts/check_environment.py
   uv run robot tests/00_setup_verification/
   ```

3. **VS Code WSL integration:**
   - Install the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) in VS Code
   - In WSL terminal: `code .` opens the project in VS Code connected to WSL

### WSL2 Troubleshooting

- **Permission denied** → Don't clone into `/mnt/c/` (Windows filesystem). Use `~/` instead.
- **rfbrowser init hangs** → Check if Windows Firewall is blocking the download
- **EACCES npm errors** → WSL filesystem permission issue. Use `nvm` instead of system npm.
- **"Cannot open display"** → Headless mode is required in WSL. Don't use `headless=${False}`.

## Common Windows Issues

| Problem | Fix |
|---------|-----|
| `uv: command not found` | Restart terminal after install, or `source ~/.bashrc` |
| `node: command not found` | Restart terminal, or install via nvm |
| Docker build hangs | Increase Docker Desktop memory limit (Settings → Resources) |
| Git line ending warnings | Run `git config --global core.autocrlf input` |
| Slow filesystem in WSL | Move project out of `/mnt/c/` to `~/` in WSL |

## Verify Your Setup

Regardless of which option you chose, run the environment check:

```bash
python scripts/check_environment.py
```

This checks all 11 prerequisites and shows exactly what's wrong and how to fix it.
