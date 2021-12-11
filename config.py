"""This script contains the configuration that run all the project"""

import sqlite3
import os

con = sqlite3.connect(os.getenv("SQL_PATH"))