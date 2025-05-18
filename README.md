# Secure and Modular Bash Script Template

> **License:** GNU AGPL-3.0-or-later  
> **Copyright (C) 2025 Rafael Mori**  
> **Inspired by Adrelanos' [helper-scripts](https://github.com/Whonix/helper-scripts)**

This repository provides a robust template for writing secure, maintainable, and modular Bash scripts. It includes best practices for error handling, logging, colorized output, and safe environment setup. The structure is designed to help you avoid common pitfalls in shell scripting, such as accidental root execution, function name collisions, and improper sourcing.

## Key Features

- **Security First**: Prevents execution as root or via sudo, and enforces safe shell options (`errexit`, `nounset`, `pipefail`).
- **Modular Design**: Functions are prefixed and exported selectively to avoid polluting the global namespace.
- **Logging & Colors**: Built-in logger with color support, background detection, and high-contrast output for better UX.
- **Wrapper Example**: Shows how to create a secure entry point for your scripts, with argument routing and environment validation.
- **Extensible Utilities**: Includes utilities for user prompts, secret input, and terminal buffer management.

## Example Usage

```bash
# Secure wrapper usage
./examples/secure_wrapper.sh 2 arg1 arg2
```

This will safely route execution to the appropriate script and function, ensuring all environment checks and logging are in place.

## How to Use

1. **Copy the template scripts** to your project.
2. **Replace all `myname` prefixes** with your script's name.
3. **Customize the wrapper** to fit your use case.
4. **Leverage the logger and color utilities** for consistent output and error handling.

## Why Use This Template?

- Avoids common shell scripting mistakes.
- Makes your scripts easier to maintain and extend.
- Provides a professional foundation for automation, DevOps, and CI/CD tasks.

---

### Share with the Community

Feel free to use this template as a base for your own scripts and share improvements or use cases with the community via Gist, DEV.to, or other platforms!
