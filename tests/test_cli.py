import pytest
from app import create_app
from config import TestConfig

def test_init_db_cli():
    app = create_app(TestConfig)
    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Database tables initialized" in result.output
