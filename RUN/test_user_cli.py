


from typer.testing import CliRunner
from user_cli import app  # import your Typer app here

runner = CliRunner()

def test_create_user():
    result = runner.invoke(app, ['create', '--name', 'Zaki', '--email', 'zaki@example.com', '--password', '1234', '--age', '25', '--gender', 'M'])
    assert result.exit_code == 0
    assert "User created:" in result.output

def test_update_user():
    # assuming user with id 1 exists after create test
    result = runner.invoke(app, ['update', '1', '--name', 'Zaki Updated'])
    assert result.exit_code == 0
    assert "User updated:" in result.output

def test_delete_user():
    result = runner.invoke(app, ['delete', '1'])
    assert result.exit_code == 0
    assert "deleted" in result.output or "not found" in result.output