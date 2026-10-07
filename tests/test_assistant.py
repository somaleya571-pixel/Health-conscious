import os
import sys
import pytest

# Add Plugins and project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PLUGINS_DIR = os.path.join(PROJECT_ROOT, 'Plugins')

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if PLUGINS_DIR not in sys.path:
    sys.path.insert(0, PLUGINS_DIR)

from gmail import check_email
import websites
import browsing_functionalities
import database


def test_check_email():
    assert check_email("user@example.com") is True
    assert check_email("test.user+tag@domain.co.in") is True
    assert check_email("invalid-email") is False
    assert check_email("@domain.com") is False
    assert check_email("user@.com") is False


def test_websites_dictionary():
    assert "google" in websites.websites_dict
    assert websites.websites_dict["google"] == "https://www.google.com/"
    assert "github" in websites.websites_dict


def test_open_specified_website_invalid(monkeypatch):
    # Tests query for a website not present in dictionary
    result = browsing_functionalities.open_specified_website("open nonexistentwebsite12345")
    assert result is None


def test_database_operations(monkeypatch, tmp_path):
    # Test sqlite database interaction with temp database
    test_db = tmp_path / "test_chats.db"
    import sqlite3
    conn = sqlite3.connect(str(test_db))
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE ASSISTANT (SERIAL_NO INTEGER PRIMARY KEY,
                      QUERY VARCHAR(255) NOT NULL,
                      DATE_TIME VARCHAR(50) NOT NULL);''')
    conn.commit()

    monkeypatch.setattr(database, "conn", conn)
    monkeypatch.setattr(database, "cursor", cursor)

    # Test add_data
    assert database.add_data("hello assistant") is True

    # Verify inserted record
    cursor.execute("SELECT QUERY FROM ASSISTANT")
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "hello assistant"


def test_data_directory_structure():
    data_dir = os.path.join(PROJECT_ROOT, "Data")
    assert os.path.exists(data_dir)
    assert os.path.exists(os.path.join(data_dir, ".env"))
