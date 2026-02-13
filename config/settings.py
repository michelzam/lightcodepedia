DEFAULT_CODE = "import streamlit as st \n\nst.title('Hi')"

# Editor configuration
LANGUAGE = "python"
HEIGHT = 500

# File paths and names
DEFAULT_FILE_NAME = "new_script.py"
DEFAULT_DIRECTORY_NAME = "."
DEFAULT_MODULE_DIRECTORY = "modules"
GITHUB_ACCESS_TOKEN="GITHUB_ACCESS_TOKEN"
GITHUB_USER_NAME="GITHUB_USER_NAME"
GITHUB_REPO_NAME="GITHUB_REPO_NAME"

ACTIVE_SESSIONS: dict[str, float] = {}
SESSION_TTL = 120  # seconds