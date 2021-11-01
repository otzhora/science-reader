#!/usr/bin/env python3
import os
import json
import signal
import subprocess
from pathlib import Path

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


setenv("API_CONFIG", "development")


BASEDIR = Path(os.path.dirname(os.path.abspath(__file__)))
DOCKER_COMPOSE_PATH = BASEDIR / "docker"
API_CONFIG_PATH = BASEDIR / "config"


def docker_compose_file(config):
    return DOCKER_COMPOSE_PATH / f"{config}.yml"


def api_config_file(config):
    return API_CONFIG_PATH / f"{config}.json"


def configure(config):
    with open(api_config_file(config)) as f:
        config = json.load(f)

    config = {item["name"]: item["value"] for item in config}

    for key, value in config.items():
        setenv(key, value)


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    config = os.getenv("API_CONFIG")
    configure(config)
    command = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(command)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def docker_compose_command(subcommands=None):
    config = os.getenv("API_CONFIG")
    configure(config)
    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f"Compose file do not exist {compose_file}")
    command = ["docker-compose", "-p", config, "-f", compose_file]
    if subcommands:
        command.extend(subcommands.split(" "))
    return command


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    command = docker_compose_command() + list(subcommand)

    try:
        p = subprocess.Popen(command)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=5432,
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


@cli.command()
def create_initial_db():
    configure(os.getenv("API_CONFIG"))

    try:
        run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
    except psycopg2.errors.DuplicateDatabase:
        print(
            f"The database {os.getenv('APPLICATION_DB')} already exists ",
            "and will not be recreated"
        )

    from reader_api.init_database import init_db
    init_db()


if __name__ == "__main__":
    cli()
