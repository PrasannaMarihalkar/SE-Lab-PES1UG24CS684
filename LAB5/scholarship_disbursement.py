"""Scholarship disbursement ledger demonstration."""

import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE awards (id INTEGER PRIMARY KEY, student TEXT, "
    "scheme TEXT, amount INTEGER, disbursed INTEGER)"
)


def grant(student, scheme, amount, audit=None):
    """Add an award to the ledger and record its student in the audit list."""
    if audit is None:
        audit = []

    conn.execute(
        "INSERT INTO awards (student, scheme, amount, disbursed) "
        "VALUES (?, ?, ?, 0)",
        (student, scheme, amount),
    )
    audit.append(student)
    return audit


def disburse(award_id):
    """Disburse an award and return its amount, or None if it does not exist."""
    row = conn.execute("SELECT amount FROM awards WHERE id = ?", (award_id,)).fetchone()
    if row:
        conn.execute("UPDATE awards SET disbursed = 1 WHERE id = ?", (award_id,))
        return row[0]
    return None


def total_disbursed():
    """Return the total amount of awards marked as disbursed."""
    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM awards WHERE disbursed = 1"
    ).fetchone()
    return row[0]


def archive():
    """Print the archive status message."""
    print("archiving awards")


def by_scheme_count(scheme):
    """Return the number of awards for a scheme."""
    if scheme is None:
        return 0
    return conn.execute("SELECT COUNT(*) FROM awards WHERE scheme = ?", (scheme,)).fetchone()[0]


def main():
    """Run a short scholarship disbursement demonstration."""
    grant("Ishaan", "Merit", 50000)
    grant("Divya", "Need-based", 75000)
    print(disburse(1), disburse(9))
    print(by_scheme_count("Merit"), total_disbursed())
    archive()


if __name__ == "__main__":
    main()
