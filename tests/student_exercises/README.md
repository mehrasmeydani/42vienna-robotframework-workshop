# Student Exercises

This directory is where you create your own test files during the workshop.

## How to create a new test

1. Copy the template file:
   ```bash
   cp tests/student_exercises/_template.robot tests/student_exercises/yourname_exercise1.robot
   ```

2. Edit the file — update the Documentation and write your test steps.

3. Run your test:
   ```bash
   uv run robot tests/student_exercises/yourname_exercise1.robot
   ```

4. Check the results in the `results/` directory — open `log.html` in your browser.

## Naming convention

Use this pattern: `{username}_exercise_{N}.robot`

Examples:
- `jdoe_exercise_1.robot`
- `jdoe_exercise_2.robot`

## Creating a Pull Request

1. Stage your test file:
   ```bash
   git add tests/student_exercises/yourname_*.robot
   ```

2. Commit:
   ```bash
   git commit -m "Add tests by yourname"
   ```

3. Push:
   ```bash
   git push origin main
   ```

4. Create a PR on GitHub (your fork → upstream repository).

## Tips

- Look at the example tests in `tests/` for inspiration
- Import resource files from `resources/` for reusable keywords
- Use `[Tags]    student    exercise` to tag your tests
- Run only your tests: `uv run robot tests/student_exercises/yourname_*.robot`
