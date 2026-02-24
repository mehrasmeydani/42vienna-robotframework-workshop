# Browser Library Guide

Browser Library uses [Playwright](https://playwright.dev/) under the hood for browser automation. It's the modern alternative to SeleniumLibrary.

## Browser Lifecycle

```
Browser → Context → Page
```

```robotframework
# Create a browser (like opening Chrome)
New Browser    chromium    headless=${True}

# Create a context (like an incognito window — isolated cookies/storage)
New Context

# Create a page (like opening a new tab)
New Page    https://www.saucedemo.com

# ... do your testing ...

# Clean up
Close Browser    ALL
```

**Why three levels?**
- **Browser:** The browser application (chromium, firefox, webkit)
- **Context:** Isolated session (cookies, storage don't leak between contexts)
- **Page:** A tab within a context

## Selectors

Browser Library supports multiple selector strategies:

| Strategy | Syntax | Example |
|----------|--------|---------|
| CSS | `css=...` | `css=.inventory_item` |
| ID | `id=...` | `id=user-name` |
| Text | `text=...` | `text=Sauce Labs Backpack` |
| XPath | `xpath=...` | `xpath=//button[@id='login']` |
| Default (CSS) | just write it | `.inventory_item` |

**SauceDemo examples:**
```robotframework
# By ID (most reliable for unique elements)
Fill Text    id=user-name    standard_user

# By CSS class
Get Text    css=.title    ==    Products

# By text content
Click    text=Sauce Labs Backpack

# Complex CSS selectors
Click    css=.inventory_item:has-text("Backpack") button
```

## Key Keywords

### Interactions

```robotframework
# Click an element
Click    id=login-button

# Type text into an input field
Fill Text    id=user-name    standard_user

# Select from a dropdown
Select Options By    css=.product_sort_container    value    lohi

# Check/uncheck a checkbox
Check Checkbox    id=remember-me
Uncheck Checkbox    id=remember-me
```

### Assertions (Getter Keywords)

Browser Library's getter keywords have **built-in assertions** — no need for a separate `Should Be Equal`:

```robotframework
# Get Title checks the page title
Get Title    ==    Swag Labs           # exact match
Get Title    contains    Swag          # partial match

# Get Text checks element text
Get Text    css=.title    ==    Products

# Get Url checks the current URL
Get Url    *=    /inventory.html       # contains
Get Url    ==    https://www.saucedemo.com/inventory.html  # exact

# Get Element Count
${count}=    Get Element Count    css=.inventory_item
Should Be Equal As Numbers    ${count}    6

# Get Attribute
Get Attribute    id=user-name    placeholder    ==    Username
```

**Assertion operators:**
| Operator | Meaning |
|----------|---------|
| `==` | Equals |
| `!=` | Not equals |
| `contains` | Contains substring |
| `*=` | Contains (alias) |
| `^=` | Starts with |
| `$=` | Ends with |
| `matches` | Regex match |

### Navigation

```robotframework
# Navigate to a URL
Go To    https://www.saucedemo.com

# Go back/forward
Go Back
Go Forward

# Reload
Reload
```

### Screenshots

```robotframework
# Take a screenshot (saved to results directory)
Take Screenshot

# Take a screenshot with a custom name
Take Screenshot    filename=login_page
```

### Waiting

Browser Library has **auto-waiting** built in — it automatically waits for elements to be visible and ready before interacting. You rarely need explicit waits.

If you do need to wait:

```robotframework
# Wait for an element to appear
Wait For Elements State    css=.inventory_item    visible    timeout=10s

# Wait for navigation
Wait For Navigation    url=*/inventory.html
```

## Headless vs Headed Mode

```robotframework
# Headless (default in CI, no visible window)
New Browser    chromium    headless=${True}

# Headed (shows the browser — useful for debugging)
New Browser    chromium    headless=${False}
```

In this workshop, tests use `headless=${True}` for CI compatibility. To see the browser while developing locally:

```bash
uv run robot --variable HEADLESS:false tests/00_setup_verification/
```
