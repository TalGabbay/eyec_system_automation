import os
import shutil


def create_directory(directory_path):
    """
    Create a directory if it does not exist.

    Args:
        directory_path (str): The path of the directory to create.
    """
    try:
        os.makedirs(directory_path)
        print("Directory created successfully.")
    except OSError as e:
        print(f"Error: {directory_path} cannot be created. Reason: {e}")


def delete_directory(directory_path):
    """
    Delete a directory and its contents recursively.

    Args:
        directory_path (str): The path of the directory to delete.
    """
    try:
        shutil.rmtree(directory_path)
        print("Directory and its contents deleted successfully.")
    except OSError as e:
        print(f"Error: {directory_path} cannot be deleted. Reason: {e}")


def create_new_file(file_path):
    """
    Create a new file.

    Args:
        file_path (str): The path of the new file to create.
    """
    try:
        with open(file_path, 'w') as file:
            pass  # Empty pass to ensure the file is created
        print("File created successfully.")
    except OSError as e:
        print(f"Error: {file_path} cannot be created. Reason: {e}")