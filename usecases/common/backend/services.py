"""
business logics and data processing

from backend.data_access import fetch_data

def get_data():
    data = fetch_data()
    # Add any business logic or data processing here
    return data
"""

# For Alex: I encapsulated services in classes to make them more modular

import subprocess
from dataclasses import dataclass
import traceback
import sys

from usecases.common.backend.file_access import DiskManager
from usecases.common.backend.module_loader import ModuleLoader
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals
from usecases.common.backend.file_access import RepoManager

@dataclass
class CodeExecutor:
    code: str = ""
    _debug: bool = False


@dataclass
class CodeLauncher(CodeExecutor):

    def run_code(self) -> list:
        """
        Runs the code and returns a list of annotations or an empty list if no errors
        :return:
        """

        try:
            code = self.code
            # byte_code = compile_restricted(code, '<string>', 'exec')
            # exec(byte_code, safe_globals, None)
            exec(code)
            return []
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.extract_tb(exc_tb)
            annotations = []
            for frame in tb:
                annotation_text = f"{exc_type.__name__}: {exc_value} (in {frame.name} at line {frame.lineno})"
                annotations.append({
                    "row": frame.lineno - 1,  # Line number (1-indexed to 0-indexed)
                    "column": 0,  # Column number
                    "type": "error",
                    "text": annotation_text
                })
            return annotations

    def run_code_sub(self) -> str:
        # Run the code as a subprocess
        print("=> Code to run as a subprocess:")
        print(self.code)
        print("=> Running code as a subprocess")
        result = subprocess.run(['python', '-c', self.code],
                                capture_output=True, text=True)
        print(result.stdout)
        return result.stdout


@dataclass
class YamlLauncher(CodeExecutor):
    code: str = ""
    loader: ModuleLoader = None
    repo: RepoManager = None

    def __post_init__(self):
        assert self.repo is not None

    def run_code(self) -> list:
        exec("print('I am a yaml launcher')")

        loader = ModuleLoader(module_name="new_module",
                              yaml_str=self.code,
                              _debug=self._debug,
                              _repo=self.repo)
        self.loader = loader

        module = loader.load()
        loader.run()

        return []  # To be implemented with annotations


@dataclass
class ScriptManager:
    code: str = ""

    def save(self, directory: str, filename: str) -> str:
        """
        Save the script to a file
        :param directory:
        :param filename:
        :return: saved path
        """
        handler: DiskManager = DiskManager(directory=directory, file_name=filename)
        return handler.save_content(self.code)

    def scan(self, directory: str) -> list[str]:
        handler: DiskManager = DiskManager(directory=directory)
        # file_names = handler.scan_files(reload=False)
        return handler.files.keys()


