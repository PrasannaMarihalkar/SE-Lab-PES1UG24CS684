

\# Issues Found During Static Code Analysis



The original scholarship disbursement program was checked using Pylint, Bandit and Flake8. The following table records the main issues and the changes made to address them.



| Issue | Type | Original line(s) | Description | Fix Approach |

|---|---|---|---|---|

| SQL query construction | Security (Bandit B608) | 10 | The SQL query used string formatting to insert values directly into the query. | Used parameterized SQL queries with placeholders. |

| Shell command execution | Security (Bandit B605, B607) | 26 | `os.system()` was used to print a simple message by starting a shell. | Removed the shell call and used Python's `print()` function. |

| Exception handling | Error handling (Bandit B110, Pylint W0718) | 25–28 | A broad exception was caught and ignored, hiding possible errors. | Removed the unnecessary exception handler. |

| Mutable default argument | Bug (Pylint W0102) | 9 | The `audit=\[]` default list could be shared across function calls. | Changed the default to `None` and initialized a list inside the function. |

| Global state | Maintainability (Pylint W0603) | 6, 16 | The running total was updated using a global variable. | Replaced the global counter with a database query for the total. |

| Inconsistent return values | Code quality (Pylint R1710) | 15–20 | The disbursement function did not explicitly return a value when an award was not found. | Added an explicit `return None`. |

| Function naming | Style (Pylint C0103) | 31 | `bySchemeCount` did not follow the recommended snake\_case naming convention. | Renamed it to `by\_scheme\_count`. |

| Comparison with None | Style (Pylint C0121, Flake8 E711) | 32 | The code used `scheme == None`. | Changed the comparison to `scheme is None`. |

| Missing documentation | Code quality (Pylint C0114, C0116) | 1, 9, 15, 24, 31, 37 | The module and functions did not have docstrings. | Added module and function docstrings. |

| Long lines | Formatting (Pylint C0301, Flake8 E501) | 5, 10, 17, 19, 34 | Some statements exceeded the permitted line length. | Split long statements across multiple lines. |



\## Verification



The original reports were saved before modifying the code. After the fixes, all three tools were run again against the updated program to verify the changes.



