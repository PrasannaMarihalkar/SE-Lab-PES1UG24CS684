

\# Lab 5: Static Code Analysis — Reflection



\## 1. What did you learn from this lab?



I learned that static code analysis can help find issues in a program before running it. It helped me identify problems with security, function arguments, naming and formatting. I also learned that fixing these issues makes the code easier to read and maintain.



\## 2. What is the difference between Pylint, Bandit and Flake8?



Pylint checks code quality and common programming mistakes. Bandit checks for possible security issues. Flake8 checks formatting and Python style rules. Using all three helped me check different parts of the same program instead of depending on only one tool.



\## 3. What issues did you find, and how did you fix them?



The original program used string formatting to construct an SQL query, had a mutable default argument and used a shell command just to print a message. It also had an exception handler that ignored errors. I used parameterized SQL, changed the default argument to None, removed the unnecessary shell command and exception handler, and corrected the naming, documentation and formatting issues.



\## 4. How did static analysis improve the program, and what are its limitations?



The original Pylint score was 5.00/10, and the final score was 10.00/10. Bandit initially reported one medium-severity and three low-severity findings, while the final scan reported no findings. Flake8's initial violations were also resolved. The sample program produced the same output after the changes. However, static analysis cannot guarantee that a program is completely correct, so running the program and testing its behaviour is still important.



