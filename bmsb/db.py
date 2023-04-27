# -*- coding: utf-8 -*-
"""Establishes an easy-to-use interface for working with PostgreSQL database."""

from __future__ import annotations

import os

import psycopg2

__author__ = "Luke Zaruba"
__credits__ = ["Luke Zaruba", "Mattie Gisselbeck"]
__status__ = "Production"


class Database:
    """
    A class used to represent a database connection.

    Methods
    -------
    initialize_from_env()
        Initializes a database object, based on environmental variable.
    connect()
        Makes connection to database.
    query(query)
        Executes query on database.
    close()
        Closes connection to database.
    """

    def __init__(
        self, host: str, user: str, password: str, db_name: str, port: int
    ) -> None:
        """Instantiates a database connection to a PostgreSQL database.

        :param str host: Host address of the database you would like to access.
        :param str user: Username credential for the database you would like to access.
        :param str password: Password credential for the database you would like to access.
        :param str db_name: Name of the database that you would like to access.
        :param int port: Port number of database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port

        # Set Connection to None
        self.connection = None

    @classmethod
    def initialize_from_env(cls) -> Database:
        """Instantiates a database connection to a PostgreSQL database using enviornmental variables."""
        # Extract Secrets
        host = os.environ.get("HOST")
        user = os.environ.get("USER")
        password = os.environ.get("PASSWORD")
        db_name = os.environ.get("DBNAME")
        port = os.environ.get("DBPORT")

        # Return Instance
        return cls(host, user, password, db_name, port)

    def connect(self) -> None:
        """Makes connection to database."""
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.password,
            port=self.port,
        )

    def query(self, query: str, user_input: str) -> str:
        """Executes a query on a database connection. A connection should already exist.

        :param str query: A SQL query that will be executed.
        :param str user_input: User input for query.
        :return str: The return from the SQL query.
        """
        # Open Cursor
        with self.connection.cursor() as c:
            # Try to Execute
            try:
                # Execute Query
                c.execute(query, (user_input,))

                # Commit to DB
                self.connection.commit()

                # Return Output
                return c.fetchall()

            except Exception as e:
                # Roll Back Transaction if Invalid Query
                self.connection.rollback()

                # Display Error
                return "Error: " + str(e)

    def close(self):
        """Closes connection to database."""
        # Close Connection
        self.connection.close()

        # Set Connection to None
        self.connection = None


class Query:
    """
    A class used to store SQL queries and format the results of queries.

    Methods
    -------
    format(result)
        Formats query output as a GeoJSON.
    """

    # Huff Simple Queries
    SIMPLE_HUFF_IN = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    SIMPLE_HUFF_OUT = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    SIMPLE_HUFF_RISK = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """

    # Huff Decay Queries
    DECAY_HUFF_IN = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    DECAY_HUFF_OUT = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    DECAY_HUFF_RISK = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """

    # Gravity Queries
    GRAVITY_IN = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    GRAVITY_OUT = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """
    GRAVITY_RISK = """
        SELECT JSON_AGG(ST_asGeoJSON(rankings))
        FROM (
            SELECT *, RANK() OVER (ORDER BY <field>) as rank
            FROM <table>
        ) as rankings
        WHERE rank <= %s;
    """

    @staticmethod
    def format(output: str) -> str:
        # Alter Formatting
        middle = str(output[0][0]).replace("'", "")
        begin = """{"type": "FeatureCollection", "features": """
        end = "}"

        geojson = begin + middle + end

        # Return New String
        return geojson
