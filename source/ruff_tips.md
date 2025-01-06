---
date: 2025/01/06 14:10
---

# Ruff TIPS

## 公式ドキュメント

[Ruff — Ruff documentation](https://ruff.readthedocs.io/en/latest/)

## ごく私的Ruff設定メモ

以下を`pyproject.toml`に記述しておくと、`ruff lint`や`ruff format`を実行するときに、設定が反映される。

```python
[tool.ruff]
# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

line-length = 88
indent-width = 4

src = ["chatbot", "personalogic", "tests"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle
    "W",    # pycodestyle
    "F",    # pyflakes
    "I",    # isort
    "D",    # pydocstyle
    "UP",   # pyupgrade
    "CPY",  # flake8-copyright
    "LOG",  # flake8-logging
    "G",    # flake8-logging-format
    "ERA",  # eradicate
]
ignore = [
    "UP035", # deprecated-import
    "D400",  # ends-in-period
    "D417",  # undocumented-param
    "E501",  # Line too long
]

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D", "UP"]
[tool.ruff.lint.pydocstyle]
convention = "google"
[tool.ruff.format]
# Enable reformatting of code snippets in docstrings.
docstring-code-format = true
quote-style = "double"
line-ending = "lf"
skip-magic-trailing-comma = false
```
