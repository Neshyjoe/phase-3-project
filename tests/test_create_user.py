import pytest
from typer.testing import CliRunner
from user_cli import app  # Assuming your Typer app is in 'user_cli.py'

runner = CliRunner()

def test_create_user():
    def test_create_user():
    result = runner.invoke(app, [
        'create', 'Joash', 'joash@example.com', '1234', '25', 'M'
    ])

    print("\n=== OUTPUT ===")
    print(result.output)
    print("=== EXCEPTION ===")
    print(result.exception)

    assert result.exit_code == 0

    # Print the output and exception to inspect the error
    print("Output:", result.output)  # This will show the standard output or any error message.
    print("Exception:", result.exception)  # This will show the exception, if any, raised by Typer.

    # Assert the exit code is 0 (indicating success)
    assert result.exit_code == 0
    
    # Optionally, you can assert that a specific success message is in the output:
    # assert "User Joash created" in result.output
