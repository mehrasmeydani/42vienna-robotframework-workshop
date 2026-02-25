# Student Workflow Guide

How to set up your environment, write tests, and submit your work.

## Step 1: Fork the Repository

A "fork" is your personal copy of the repository on GitHub. You'll work in your fork and submit changes back via a Pull Request.

1. Go to https://github.com/HackXIt/42vienna-robotframework-workshop
2. Click the **"Fork"** button (top-right corner)
3. On the "Create a new fork" page:
   - **Owner:** Your GitHub username (already selected)
   - **Repository name:** Keep the default
   - Leave "Copy the `main` branch only" checked
4. Click **"Create fork"**

You now have your own copy at `https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop`.

## Step 2: Open a Codespace

Codespaces gives you a full development environment in your browser — no local installation needed.

1. Go to **your fork** (not the original repo): `https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop`
2. Click the green **"Code"** button
3. Switch to the **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait ~3-5 minutes for the environment to build

The DevContainer automatically installs everything: Python, Node.js, Robot Framework, Browser Library, and Chromium.

### Verify Your Setup

When the terminal appears in your Codespace, run:

```bash
uv run robot tests/00_setup_verification/
```

You should see: `1 test, 1 passed, 0 failed`

If anything fails, run the environment check:

```bash
python scripts/check_environment.py
```

## Step 3: Write Your Tests

1. **Create your exercise file** from the template:
   ```bash
   cp tests/student_exercises/_template.robot tests/student_exercises/yourname_exercise_1.robot
   ```
   Replace `yourname` with your actual name (lowercase, no spaces).

2. **Edit the file** in VS Code (it's already open in your Codespace)

3. **Run your test** to verify it works:
   ```bash
   uv run robot tests/student_exercises/yourname_exercise_1.robot
   ```

4. **Check the results** — open `results/log.html` for detailed execution logs

See [Exercises](04-exercises.md) for progressive exercise instructions.

## Step 4: Commit Your Work

```bash
# Stage your files
git add tests/student_exercises/yourname_*.robot

# Commit
git commit -m "Add exercises by yourname"

# Push to your fork
git push origin main
```

## Step 5: Create a Pull Request

A Pull Request (PR) asks the instructor to review and merge your work into the original repository.

1. Go to **your fork** on GitHub
2. You should see a banner: **"This branch is 1 commit ahead of HackXIt:main"**
3. Click **"Contribute"** → **"Open pull request"**
4. Fill in the PR template:
   - Describe what your test verifies
   - Check the checklist items
   - Select which SauceDemo flows you tested
5. Click **"Create pull request"**

### What happens after you submit?

1. **CI runs your tests** — GitHub Actions automatically runs all tests including yours
2. **Results posted** — A comment appears on your PR with pass/fail results
3. **Instructor reviews** — The instructor checks your tests and provides feedback
4. **Merge** — Once approved, your tests are merged into the main repository

### First-time contributor CI approval

When you create your first PR from a fork, GitHub Actions requires the repository maintainer (instructor) to approve the workflow run. This is a security feature. The instructor will approve it during the workshop — you don't need to do anything extra.

## Troubleshooting

### "I can't push to origin"

Make sure you're pushing to **your fork**, not the original repository. Check your remote:

```bash
git remote -v
```

You should see your username in the URL: `https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop.git`

### "My Codespace doesn't have the latest changes"

If the instructor updated the main repository after you forked:

```bash
# Add the original repo as "upstream"
git remote add upstream https://github.com/HackXIt/42vienna-robotframework-workshop.git

# Fetch and merge updates
git fetch upstream
git merge upstream/main
```

### "The PR template didn't appear"

The template shows automatically when creating a PR to the main repository. If it didn't appear, you can copy the checklist from `.github/PULL_REQUEST_TEMPLATE.md`.

### "CI didn't run on my PR"

For first-time contributors from forks, the instructor must approve the workflow run. Raise your hand or ask the instructor to approve it via the Actions tab.

## Alternative: Collaborator Access (Plan B)

If forking causes issues during the workshop, the instructor can add you as a collaborator:

1. **Instructor adds you:** Provide your GitHub username to the instructor
2. **Accept the invitation:** Check your GitHub notifications or email
3. **Clone the repo directly:**
   ```bash
   git clone https://github.com/HackXIt/42vienna-robotframework-workshop.git
   ```
4. **Create a branch:**
   ```bash
   git checkout -b yourname-exercises
   ```
5. **Work, commit, push, and create a PR** from your branch to `main`

This skips the fork step but otherwise works the same way.
