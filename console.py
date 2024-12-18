#!/usr/bin/env python3
"""This module contains the console for the application."""
import cmd


class FoodifyConsole(cmd.Cmd):
    intro = ("Welcome to the Foodify console. Type 'help' or '?' to list "
             "commands.\n")
    prompt = "(foodify) "

    def do_quit(self, arg):
        """Quit the console."""
        print("Goodbye!")
        return True

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D) to exit the console."""
        print("Goodbye!")
        return True

    def help_quit(self):
        print("Exits the console. Usage: quit")

    def help_EOF(self):
        print("Exits the console with EOF (Ctrl+D).")


if __name__ == "__main__":
    FoodifyConsole().cmdloop()
