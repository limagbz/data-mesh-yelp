# Contributing Guide

First of all, thanks to be interested in contributing! If not already, we encourage you to look into our
[README](README.md) for some overview of the project. The next sections will guide you on how to better
contribute with this project.

1. [Style Guide](#style-guide)
1. [Best Practices](#best-practices)
1. [References](#references)

## Style Guide

To maintain a better readability and structure for this project below are some general styleguide rules
followed by this project

- Use **kebab-case** when naming folders and files;
- No more that **110 characters** per line, this is to ensure a good readability of the code. URLs and tables
are the only exception for this rule;
- No **Trailing whitespaces** on the end of the lines;
- Always end the file with a **blank line**;
- When writting documentation use angled brackets ("<>") for places where the user needs to interact. For
For example, `command <PARAMETER>`;
- Always set **fixed versions** for packages, tools and anything that could be versioned;

We also follow some language/tools specific rules (that have precedence over the ones above). Below are the
references for their styleguides:

- **Markdown:** For Markdown we follow [Google's Markdown Style Guide](https://google.github.io/styleguide/docguide/style.html);
- **Shell Scripts:** We also follow [Google's Shell Style Guide](https://google.github.io/styleguide/shellguide.html);
- **YAML:** YAML files follow the rules found on [yamlint configuration](.yamllint) and are evaluated
automatically. See [yamlint: rules](https://yamllint.readthedocs.io/en/stable/rules.html) for description for
each rule used by the project.

## Best Practices

Below are some references for best practices from tools, languages and related technologies of this project.

- [Docker: Development best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker: Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker: Security best practices](https://docs.docker.com/develop/security-best-practices/)

## References

- [Wrangling Web Contributions: How to Build a CONTRIBUTING.md](https://mozillascience.github.io/working-open-workshop/contributing/)
- [Awesome Guidelines](https://github.com/Kristories/awesome-guidelines)
- [Github: Contributing Guide](https://github.com/github/docs/blob/main/CONTRIBUTING.md)
