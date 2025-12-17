#!/usr/bin/env python3
import argparse
import subprocess
import sys


def run_command(cmd):
    """Run a shell command and stream output."""
    process = subprocess.run(cmd, shell=True)
    if process.returncode != 0:
        sys.exit(process.returncode)


def main():
    parser = argparse.ArgumentParser(description="Development helper CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("up", help="Start all services")
    subparsers.add_parser("down", help="Stop all services")
    subparsers.add_parser("migrate", help="Run Flask-Migrate upgrade")

    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "test_path", nargs="?", default="tests/", help="Path to tests"
    )

    args = parser.parse_args()

    if args.command == "up":
        run_command("docker compose up -d postgres flask-app")
    elif args.command == "down":
        run_command("docker compose down")
    elif args.command == "migrate":
        run_command("docker compose run --rm flask-app flask db upgrade")
    elif args.command == "test":
        run_command(f"docker compose run --rm tests pytest {args.test_path} -q")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
