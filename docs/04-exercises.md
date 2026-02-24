# Workshop Exercises

Progressive exercises from beginner to advanced. Work through them in order.

## Exercise 1: Verify Your Setup (Warmup)

Run the setup verification test:

```bash
uv run robot tests/00_setup_verification/
```

**Tasks:**
1. Observe the terminal output — what does `1 test, 1 passed` mean?
2. Open `results/log.html` in your browser — explore the test log
3. Open `results/report.html` — this is the test report

## Exercise 2: Your First Test

Open `tests/01_first_test/first_browser_test.robot` and read through it.

**Tasks:**
1. Run it: `uv run robot tests/01_first_test/`
2. Read the comments — they explain each keyword
3. **Create your own test:** Copy `_template.robot` to your exercise file:
   ```bash
   cp tests/student_exercises/_template.robot tests/student_exercises/yourname_exercise_1.robot
   ```
4. Write a test that:
   - Opens SauceDemo
   - Checks the page title is "Swag Labs"
   - Checks that a login button exists (`id=login-button`)

## Exercise 3: Login Tests

Study `tests/02_login_tests/login.robot` and the `resources/login_page.resource`.

**Tasks:**
1. Run the login tests: `uv run robot tests/02_login_tests/`
2. Create a new exercise file and write tests that:
   - Log in with `standard_user` / `secret_sauce` and verify you land on the products page
   - Try logging in with `problem_user` — does it succeed? What's different about this user?
   - Try logging in with an empty username AND empty password

**Hint:** Import `../../resources/common.resource` and `../../resources/login_page.resource` in your Settings section.

## Exercise 4: Products and Cart

Study `tests/03_product_tests/` and `tests/04_cart_tests/`.

**Tasks:**
1. Write a test that:
   - Logs in
   - Adds "Sauce Labs Backpack" to the cart
   - Verifies the cart badge shows "1"
   - Opens the cart
   - Verifies "Sauce Labs Backpack" is in the cart

**Hint:** You'll need to import `products_page.resource` and `cart_page.resource`.

## Exercise 5: Complete Purchase (E2E)

Now for the big one — a full end-to-end test.

**Tasks:**
1. Write a test that performs a complete purchase:
   - Login with `standard_user`
   - Add 2 products to the cart
   - Go to the cart
   - Proceed to checkout
   - Fill in checkout information (any first name, last name, zip)
   - Complete the purchase
   - Verify the confirmation message: "Thank you for your order!"

**Hint:** Study `tests/06_e2e_scenarios/complete_purchase.robot` if you get stuck.

## Exercise 6: Keyword Abstraction (Advanced)

**Tasks:**
1. Create a new resource file `resources/my_keywords.resource`
2. Define a keyword `Purchase Product` that takes a product name and:
   - Adds it to cart
   - Goes to cart
   - Proceeds to checkout
   - Fills checkout info
   - Completes the purchase
3. Write a test that uses your new keyword to purchase "Sauce Labs Bike Light"

This is the **page object pattern** in action — abstracting complex flows into reusable keywords.

## Exercise 7: Data-Driven Testing (Advanced)

**Tasks:**
1. Create a test using `[Template]` that tests login with multiple credential sets:
   - Valid credentials → should succeed
   - Wrong password → should show error
   - Locked user → should show locked message
   - Empty username → should show required error

Study the `[Template]` section in `docs/02-rf-syntax-cheatsheet.md`.

## Exercise 8: AI-Assisted Testing (Demo)

**Tasks:**
1. Open Claude Code or GitHub Copilot in your Codespace
2. Describe a test scenario in natural language:
   > "Write a Robot Framework test that verifies products can be sorted by name Z-to-A on SauceDemo"
3. Review the generated test — does it look correct?
4. Run it and see if it passes
5. If it fails, refine your prompt or fix the test manually

## Submitting Your Work

1. Stage your files:
   ```bash
   git add tests/student_exercises/yourname_*.robot
   ```
2. Commit:
   ```bash
   git commit -m "Add exercises by yourname"
   ```
3. Push to your fork:
   ```bash
   git push origin main
   ```
4. Create a Pull Request:
   - Go to your fork on GitHub
   - Click **"Contribute"** → **"Open pull request"**
   - Fill in the PR template
   - Click **"Create pull request"**
5. Watch the CI run your tests!
