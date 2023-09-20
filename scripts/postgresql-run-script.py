"""Run an SQL script on PostgreSQL Database

This code runs an SQL script into PostgreSQL database with parameter
substition. Note that the statements are executed line-by-line.

Parameter Substitution:
    In order for the parameters to be replaced on the file they need to be
    on the format ":parameter". For example, if you want to replace the
    a username and password parametesr the statement should look like this

        $ CREATE USER :username WITH PASSWORD ':password'

    The command should be run with

        $ python postgres-run-script.py -s username=myuser -s password=pass

Running the Code:
    To run this code please export the following required environment
    variables. You can also create a .env file that it will be loaded
    automatically (make sure to commit this file):

    * POSTGRESQL_USER: User to connect with the PostgreSQL
    * POSTGRESQL_PASSWORD: Password of the user above
    * POSTGRESQL_HOST: URL/Host of the PostgreSQL Server
    * POSTGRESQL_PORT: Port to connect to the PostgreSQL server

    For more information about other options. Run:

        $ python setup-postgresql.py --help
"""

# TODO: Add unit tests
import os
import sys
import logging
import re
import click

from tqdm import tqdm
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.engine.base import Engine

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

POSTGRESQL_USER = os.environ.get("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
POSTGRESQL_HOST = os.environ.get("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.environ.get("POSTGRESQL_PORT")
POSTGRESQL_DATABASE = os.environ.get("POSTGRESQL_DATABASE")


@click.command()
@click.option(
    "-s",
    "--substitutions",
    # nargs=-1,
    multiple=True,
    type=str,
    help=(
        "Substitutions for the script. For this to work, the SQL script "
        "should contain the string to be replaced in a :variable format. Here "
        "you should omit the ':'"
    ),
)
@click.option(
    "-d",
    "--database",
    type=str,
    default=None,
    help=(
        "Database where the script should run. A null value represents "
        "connection to the default database"
    ),
)
@click.argument("path", nargs=1)
def main(path: str, database: str, substitutions: str) -> None:
    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(
            POSTGRESQL_USER,
            POSTGRESQL_PASSWORD,
            POSTGRESQL_HOST,
            POSTGRESQL_PORT,
            database if database else "",
        ),
        isolation_level="AUTOCOMMIT",
    )

    with open(path, "r") as f:
        sql_file_content = f.read()

    params = parse_params(substitutions)
    stmts = parse_statements(sql_file_content, params)

    logging.debug(f"Statements: {stmts}")

    logging.info("Running script...")
    run_script(engine, stmts)
    logging.info("Script executed successfully!")


def parse_params(params: tuple) -> dict:
    """Parse parameters to dict, checking if they are correctly formatted

    Args:
        params (tuple): Tuple of parameters

    Raises:
        SyntaxError: If not on format oldvalue=replacement

    Returns:
        dict: parameters in a dict format
    """
    r = re.compile(".*=.*")

    parsed_params = {}
    for s in params:
        split = s.split("=")
        if not r.match(s) or len(split) != 2:
            raise SyntaxError(
                (
                    f"Parameter {s} is not correctly formatted."
                    "The correct format is old=new."
                )
            )
        parsed_params[split[0]] = split[1]
    return parsed_params


def parse_statements(file: str, params: dict) -> list:
    """Parse statements replacing the parameters values.

    Args:
        file (str): File content
        params (dict): Parameters to be replaced on the script
        is_line (bool): Executes the statements line-by-line. Useful for
                        statements that cannot be on transaction blocks

    Returns:
        list: statements to execute on PostgreSQL
    """

    for old, new in params.items():
        file = file.replace(f":{old}", new)

    stmts = []
    for s in file.split(";\n"):
        st = re.sub(r"--.*\n", "", s.strip())
        if st != "":
            stmts.append(text(st))

    return stmts


def run_script(engine: Engine, stmts: list[str]) -> None:
    """Runs an SQL script into Postgres
    Args:
        engine (Engine): SQL Alchemy engine to connect with PostgreSQL.
        stmts (list[str]): Statements to run on the PostgreSQL
    """
    with engine.connect() as conn:
        for s in tqdm(stmts):
            conn.execute(s)


if __name__ == "__main__":
    main()
