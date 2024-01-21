#!/usr/bin/env python3
import argparse
from datetime import datetime
from typing import Any, Dict

import mysql.connector



def create(args) -> None:
    conn = mysql.connector.MySQLConnection(
        host=args.host, port=args.port, user=args.user, password=args.password,
    )

    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE `{args.db}`")
    cursor.execute(f"USE `{args.db}`")
    cursor.execute(
        """
            CREATE TABLE `_migration` (
                `date` DATETIME(6) DEFAULT NOW(6),
                `version` INT NOT NULL,
                `migration` VARCHAR(255) NOT NULL,
                `migration_hash` CHAR(40) COMMENT "[NOT IMPLEMENTED] Hash of SQL transaction used for migration + previous migration hash - used to ensure previous migrations haven't modified since application",
                `schema_hash` CHAR(40) COMMENT "[NOT IMPLEMENTED] Hash of full SHOW CREATE TABLE output post-migration - used to ensure schema has not changed outside of tracked migrations",
                PRIMARY KEY (`date`)
            )
        """
    )
    _record_migration(cursor, -1, "__baseline__")

    conn.commit()
    conn.close()


def down() -> None:
    pass


def list_migrations() -> None:
    pass


def up() -> None:
    pass


def flock_cli() -> None:
    parser = argparse.ArgumentParser(description="Barebones database migration utility")
    parser.set_defaults(func=None, has_conn=False)

    subparsers = parser.add_subparsers()

    auth_args = argparse.ArgumentParser(add_help=False)
    auth_args.add_argument("host", help="MySQL server IP or hostname")
    auth_args.add_argument("db", help="MySQL database name")
    auth_args.add_argument("user", help="Name of MySQL user")
    auth_args.add_argument("password", help="MySQL user password")
    auth_args.add_argument(
        "-p", "--port", type=int, default=3306, help="Port mysql server is on"
    )
    auth_args.set_defaults(has_conn=True)

    migrate_args = argparse.ArgumentParser(add_help=False)
    migrate_args.add_argument(
        "-m",
        "--migration-dir",
        default=".",
        help="Directory containing migration files",
    )

    sub_create = subparsers.add_parser(
        "create", parents=(auth_args,), help="Create a database"
    )
    sub_create.set_defaults(func=create)

    sub_list = subparsers.add_parser(
        "list", parents=(migrate_args,), help="List available migrations"
    )
    sub_list.set_defaults(func=list_migrations)

    sub_up = subparsers.add_parser(
        "up",
        parents=(auth_args, migrate_args),
        help="Migrate a database up to a given version",
    )
    sub_up.set_defaults(func=up)
    sub_up.add_argument(
        "-v",
        "--version",
        help="Version to migrate up to - must be greater than current version. Default is latest",
    )

    sub_down = subparsers.add_parser(
        "down",
        parents=(auth_args, migrate_args),
        help="Migrate a database down to a given version",
    )
    sub_down.set_defaults(func=down)
    sub_down.add_argument(
        "-v",
        "--version",
        required=True,
        help="Version to migrate down to - must be less than current version",
    )

    args = parser.parse_args()

    args.func(args)


def _record_migration(cursor: mysql.connector.cursor.MySQLCursor, version: int, migration: str) -> None:
    cursor.execute(
        "INSERT INTO `_migration`VALUES (%s, %s, %s, %s, %s)",
        (datetime.now(), version, migration, None, None)
    )


if __name__ == "__main__":
    flock_cli()
