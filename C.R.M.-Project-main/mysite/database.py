from __future__ import annotations
import os
import sys
import argparse
import subprocess
from typing import Optional

try:
    import pyodbc
except Exception as e:
    print("ERROR: 'pyodbc' is required. Install with: pip install pyodbc")
    raise SystemExit(1)

# Defaults (can be overridden by env vars or CLI args)
DEFAULT_SERVER = os.environ.get("MSSQL_SERVER", "DESKTOP-47SJR24")
DEFAULT_DB = os.environ.get("MSSQL_DB", "crm_database")
DEFAULT_DRIVER = os.environ.get("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")
DEFAULT_USE_WINDOWS_AUTH = os.environ.get("MSSQL_WINDOWS_AUTH", "1") in ("1", "true", "True")
DEFAULT_USER = os.environ.get("MSSQL_USER", "sa")
DEFAULT_PASSWORD = os.environ.get("MSSQL_PASSWORD", "1234")
DEFAULT_COLLATION = os.environ.get("MSSQL_COLLATION", "SQL_Latin1_General_CP1_CI_AS")


def make_conn_string_to_master(
    server: str,
    driver: str,
    use_windows_auth: bool,
    user: str,
    password: str,
    extra_params: Optional[str] = "TrustServerCertificate=yes;"
) -> str:
    if use_windows_auth:
        return f"DRIVER={{{driver}}};SERVER={server};DATABASE=master;Trusted_Connection=yes;{extra_params}"
    else:
        return f"DRIVER={{{driver}}};SERVER={server};DATABASE=master;UID={user};PWD={password};{extra_params}"


def database_exists(cursor: pyodbc.Cursor, db_name: str) -> bool:
    cursor.execute("SELECT name FROM sys.databases WHERE name = ?", db_name)
    return cursor.fetchone() is not None


def create_database(cursor: pyodbc.Cursor, db_name: str, collation: str) -> None:
    sql = f"CREATE DATABASE [{db_name}] COLLATE {collation};"
    cursor.execute(sql)


def run_migrations(cwd: Optional[str] = None) -> int:
    cmd = [sys.executable, "manage.py", "migrate"]
    print("Running migrations:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=cwd or ".", capture_output=False)
    return proc.returncode


def main() -> int:
    p = argparse.ArgumentParser(description="Create SQL Server database if missing.")
    p.add_argument("--server", default=DEFAULT_SERVER)
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--driver", default=DEFAULT_DRIVER)
    p.add_argument("--no-windows-auth", action="store_true", help="Use SQL authentication (provide --user/--password)")
    p.add_argument("--user", default=DEFAULT_USER)
    p.add_argument("--password", default=DEFAULT_PASSWORD)
    p.add_argument("--collation", default=DEFAULT_COLLATION)
    p.add_argument("--migrate", action="store_true", help="Run Django migrations after creating/confirming DB")
    p.add_argument("--manage-dir", default=".", help="Directory where manage.py lives (used by --migrate)")

    args = p.parse_args()

    server = args.server
    db = args.db
    driver = args.driver
    use_win = not args.no_windows_auth
    user = args.user
    password = args.password
    collation = args.collation

    connstr = make_conn_string_to_master(server, driver, use_win, user, password)

    print(f"Connecting to SQL Server '{server}' (master) using driver '{driver}' ...")
    try:
        conn = pyodbc.connect(connstr, autocommit=True)
    except Exception as e:
        print("ERROR: Could not connect to SQL Server:", e)
        return 2

    try:
        cur = conn.cursor()
        if database_exists(cur, db):
            print(f"Database '{db}' already exists.")
        else:
            print(f"Database '{db}' not found — creating...")
            create_database(cur, db, collation)
            # verify
            if database_exists(cur, db):
                print(f"Database '{db}' created successfully.")
            else:
                print("ERROR: Creation reported no error but database not found.")
                return 3
    except Exception as e:
        print("ERROR during database check/create:", e)
        return 4
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

    if args.migrate:
        rc = run_migrations(cwd=args.manage_dir)
        if rc != 0:
            print("ERROR: migrations failed (exit code", rc, ")")
            return 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())