# AI-Assisted Testing

Using AI tools to generate and improve Robot Framework tests.

## Why AI + Testing?

AI doesn't replace testers — it **accelerates test creation**. The tester still designs the test strategy, decides what to test, and validates results. AI helps with:
- Generating test code from natural language descriptions
- Suggesting selectors and assertions
- Creating boilerplate test structure
- Reviewing tests for best practices

## Using AI in Your Codespace

### GitHub Copilot

If you have Copilot enabled, it will suggest completions as you type in `.robot` files.

**Tips:**
- Start typing a test case name and let Copilot complete the steps
- Write a `[Documentation]` string first — Copilot uses it as context
- Accept suggestions with Tab, reject with Esc

### Claude Code

Claude Code can generate complete test files from descriptions.

**Example prompts:**
- "Write a Robot Framework test that verifies products can be sorted by name Z-to-A on SauceDemo"
- "Create a test that adds 3 items to cart, removes one, and verifies the cart count is 2"
- "Generate a data-driven login test using [Template] for all SauceDemo users"

## Robot Framework MCP Server

This project includes configuration for [rf-mcp](https://pypi.org/project/rf-mcp/), which gives AI agents access to Robot Framework-specific knowledge:
- Keyword documentation from installed libraries
- Library-specific patterns and best practices
- Test structure conventions

The MCP server is configured in `.claude/settings.json` and installed as a dev dependency.

## Best Practices

1. **Always review AI-generated tests** — AI can produce plausible but incorrect selectors
2. **Run the test** — Don't trust code that hasn't been executed
3. **Understand before committing** — If you can't explain what a test does, don't submit it
4. **Use AI for boilerplate, not strategy** — Decide WHAT to test yourself, let AI help with HOW

## Demo: AI Test Generation

During the workshop, we'll demonstrate:

1. Describe a test scenario in natural language
2. AI generates a complete `.robot` file
3. Run the generated test
4. Observe failures and refine
5. Compare AI-generated vs hand-written tests

The goal is not "AI writes all tests" but "AI saves time on repetitive parts so you can focus on test design."
