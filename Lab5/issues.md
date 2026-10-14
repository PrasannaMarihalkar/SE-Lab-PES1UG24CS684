# Issues Found During Static Code Analysis

The line numbers below refer to the original, unmodified Python file.

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL query construction | Security — Bandit B608 (Medium) | 10 | String formatting inserted values directly into the SQL query. | Used parameterized SQL queries with placeholders. |
| Shell command execution | Security — Bandit B605, B607 (Low) | 26 | `os.system()` started a shell for a simple message. | Removed the shell call and used Python's `print()`. |
| Exception handling | Error handling — Bandit B110, Pylint W0718 | 25–28 | A broad exception was caught and ignored. | Removed the unnecessary exception handler. |
| Mutable default argument | Bug — Pylint W0102 | 9 | The `audit=[]` default could be shared across calls. | Changed the default to `None` and initialized a new list when needed. |
| Global state | Maintainability — Pylint W0603 | 6, 16 | The disbursed total was maintained through a global variable. | Calculated the total from the database instead. |
| Inconsistent return values | Code quality — Pylint R1710 | 15–21 | The function did not explicitly return a value when an award was not found. | Added an explicit `return None`. |
| Function naming | Style — Pylint C0103 | 31 | `bySchemeCount` did not follow snake_case. | Renamed it to `by_scheme_count`. |
| Comparison with None | Style — Pylint C0121, Flake8 E711 | 32 | The code used `scheme == None`. | Changed it to `scheme is None`. |
| Missing documentation | Code quality — Pylint C0114, C0116 | 1, 9, 15, 24, 31, 37 | The module and functions lacked docstrings. | Added module and function docstrings. |
| Long lines | Formatting — Pylint C0301, Flake8 E501 | 5, 10, 17, 19, 34 | Some statements exceeded the configured line limits. | Split long statements across multiple lines. |

## Verification

The original reports were saved before modifying the code. All three tools were run again after the changes to verify the results.
