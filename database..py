import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "predictions.db"
)


def get_connection():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT,

            crop TEXT,

            disease TEXT,

            confidence REAL,

            severity TEXT,

            solution TEXT,

            created_at TEXT

        )
    """)

    connection.commit()

    connection.close()


def save_prediction(
    image_name,
    crop,
    disease,
    confidence,
    severity,
    solution
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (
            image_name,
            crop,
            disease,
            confidence,
            severity,
            solution,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        image_name,
        crop,
        disease,
        confidence,
        severity,
        solution,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()

    connection.close()


def get_predictions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]