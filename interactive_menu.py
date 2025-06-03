from prompt_toolkit.shortcuts import radiolist_dialog

def menu_selection():
    """Displays an interactive menu using arrow keys for navigation."""
    options = [
        ("login", "Login"),
        ("create", "Create User"),
        ("update", "Update User"),
        ("delete", "Delete User"),
        ("list", "List Users"),
        ("exit", "Exit")
    ]
    
    result = radiolist_dialog(
        title="Health Simplified - Select an Action",
        values=options
    ).run()

    if result is None:
        print("\nNo selection made. Returning to the main menu...")
        return "exit"  
    
    print(f"\nUser selected: {result}")  
    return result