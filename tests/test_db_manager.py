import pytest
from unittest.mock import patch, MagicMock
from src.db.db_manager import DBManager

@pytest.fixture
def db_mock():
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield DBManager()
