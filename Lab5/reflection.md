# Lab 5: Static Code Analysis — Reflection

## 1. What did you learn from this lab?

I learned that static code analysis can find common problems in a program without executing it. It helped me identify security issues, unsafe function arguments, naming problems and formatting mistakes.

## 2. What is the difference between Pylint, Bandit and Flake8?

Pylint checks code quality and common programming mistakes. Bandit checks for possible security issues. Flake8 checks Python style and formatting. Using all three helped me identify different types of problems in the same program.

## 3. What issues did you find, and how did you fix them?

The original program used string formatting to construct an SQL query, had a mutable default argument and used a shell command to print a message. It also ignored exceptions. I used parameterized SQL, changed the default argument to None, removed the unnecessary shell command and exception handler, and corrected the naming, documentation and formatting issues.

## 4. How did static analysis improve the program, and what are its limitations?

The original Pylint score was 5.00/10, and the final score was 10.00/10. Bandit initially reported one medium-severity and three low-severity findings, while the final scan reported no findings. The final Flake8 report was empty. The demonstration program also produced the expected output. However, static analysis cannot guarantee that a program is completely correct, so testing its behaviour remains important.
