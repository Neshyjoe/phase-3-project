import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




from typer.testing import CliRunner
from user_cli import app  # import your Typer app here

runner = CliRunner()

def test_create_user():
        result = runner.invoke(app, [
        'create', 'Joash', 'joash@example.com', '1234', '25', 'M'
    ])

    
   

    assert result.exit_code == 0


def test_update_user():
    # assuming user with id 1 exists after create test
    result = runner.invoke(app, ['update', '1', '--name', 'joash Updated'])
    assert result.exit_code == 0
    assert "User updated:" in result.output

def test_delete_user():
    result = runner.invoke(app, ['delete', '1'])
    assert result.exit_code == 0
    assert "deleted" in result.output or "not found" in result.output