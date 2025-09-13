import os
import time
import shutil
from abc import ABC
from dataclasses import dataclass, field
from glob import glob
from typing import List, Dict, Any
from github import Github, NamedUser, Repository, GithubException, ContentFile, Commit
import shutil
from usecases.common.backend.tracing import trace_execution_time, print_stack


@dataclass
class FileHandler:
    name: str = ""
    content: str = ""
    timestamp: str = ""
    sha: str = ""
    icon: str = "📃"
    message: str = ""

    @property
    def label(self) -> str:
        return (f"{self.icon} {self.name}\t{self.timestamp}\t{len(self.content)} bytes"
                f"\t sha: {self.sha[:7]} # {self.message}")

# Forward declaration
class RepoManager:
    pass

@dataclass
class RepoManager(ABC):
    directory: str = "."
    file_name: str = "" # default or last file name
    files: Dict[str, FileHandler] = field(default_factory=dict)
    # TODO: Add a default implementation for the following
    parent: RepoManager = None
    _debug: bool = True

    def read_content(self, file_name: str = "") -> str:
        pass

    def OLD_configure(self) -> bool:
        """
        Configure the repository manager.
        :return: True if configuration is successful, False otherwise.
        This one should be redefined in subclasses
        """
        return False

    def check_file_exists(self, file_name: str = "") -> bool:
        if len(file_name) == 0:
            file_name = self.file_name
        ret = file_name in self.files.keys()
        if (not ret) and (self.parent is not None):
            ret = self.parent.check_file_exists(file_name)
        return ret

    def save_content(self, content: str) -> str:
        pass

    def scan_files(self, reload: bool = False) -> List[str]:
        pass

    def scan_file(self, file_name: str) -> str:
        pass

    def check_access(self) -> (bool, Any):
        """
        Checks access to github
        :return: (bool, Any) - True if access is granted + info/credits.
        """
        return False, "Not implemented"

    def create_file(self, file_name: str, content: str) -> str:
        raise Exception("Not implemented in a generic way!")

@dataclass
class DiskManager(RepoManager):
    backup_before_save: bool = False

    def __post_init__(self):
        self.scan_files()

    def read_content(self, file_name: str = "") -> str:
        if len(file_name) == 0:
            file_name = self.file_name
        file_path = os.path.join(self.directory, file_name)
        with open(file_path, "r") as f:
            content = f.read()
        self.files[file_name] = FileHandler(name=file_name, content=content)
        self.files[file_name].timestamp = time.ctime(os.path.getmtime(file_path))
        return content

    def scan_file(self, file_name: str) -> str:
        return self.read_content(file_name)

    def check_file_exists(self, file_name: str = "") -> bool:
        if len(file_name) == 0:
            file_name = self.file_name
        file_path = os.path.join(self.directory, file_name)
        return os.path.exists(file_path)

    import os
    import shutil
    import time

    def _create_backup(self, file_name: str) -> None:
        """
        Creates a backup while preserving the original directory tree inside the _bak folder.
        """
        original_path = os.path.join(self.directory, file_name)
        backup_root = os.path.join(self.directory, "_bak")

        # Preserve the subdirectory structure inside the _bak folder
        relative_path = os.path.relpath(original_path, self.directory)
        backup_path = os.path.join(backup_root, relative_path)

        # Add timestamp to backup file
        base_name, ext = os.path.splitext(backup_path)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = f"{base_name}_{timestamp}{ext}"

        # Ensure the corresponding subdirectory exists inside _bak
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        # Copy the file while preserving metadata
        shutil.copy2(original_path, backup_path)

        print(f"Backup created at {backup_path}")

    def _OLD_create_backup(self, file_name: str):
        directory: str = self.directory
        save_path: str = os.path.join(directory, file_name)
        backup_dir: str = os.path.join(directory, "_bak")
        base_name, ext = os.path.splitext(file_name)
        timestamp: str = time.strftime("%Y%m%d_%H%M%S")
        backup_file_name: str = f"{base_name}_{timestamp}{ext}"
        backup_path: str = os.path.join(backup_dir, backup_file_name)

        # print(f"{backup_path = } {directory = } {backup_file_name = } {backup_dir = }")

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)

        shutil.copy2(save_path, backup_path)

    def save_content(self, content: str) -> str:
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

        # Backup the existing file
        if self.backup_before_save:
            self._create_backup(self.file_name)

        save_path = os.path.join(self.directory, self.file_name)
        with open(save_path, "w") as f:
            f.write(content)
        print(f"Saved content to {save_path} {self.directory = } {self.file_name = }")
        return save_path

    def scan_files(self, reload: bool = True) -> List[str]:
        file_paths: list[str] = glob(os.path.join(f"{self.directory}", '*.py'))
        file_paths += glob(os.path.join(f"{self.directory}", '*.yaml'))
        file_names: list[str] = [os.path.basename(file_path) for file_path in file_paths]
        if reload:
            self.files.clear()
            for file_name in file_names:
                self.files[file_name] = FileHandler(name=file_name)
                self.files[file_name].content = self.read_content(file_name)
        return file_names

    def _get_free_space_mb(self) -> int:
        """Returns the free disk space in megabytes for the given path."""
        path = self.directory
        disk_usage = shutil.disk_usage(path)
        return disk_usage.free // (1024 * 1024)  # Convert bytes to MB

    def check_access(self) -> (bool, Any):
        # check access to disk, and disk remaining space
        free_space = self._get_free_space_mb()
        if free_space < 10:
            return False, f"Disk free space is {free_space} "
        return True, f"Disk free space is {free_space} "

    def create_file(self, file_name: str, content: str) -> str:
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

        save_path = os.path.join(self.directory, file_name)
        with open(save_path, "w") as f:
            f.write(content)


        print(f"Created file {save_path} {self.directory = } {file_name = }")
        return save_path


@dataclass
class GitManager(RepoManager):
    repo_name: str = ""
    access_token: str = ""
    user_name: str = ""
    branch: str = "main"  # Default branch
    repo: Repository = field(default=None, init=False)
    github: Github = field(default=None, init=False)
    user: NamedUser = field(default=None, init=False)

    @trace_execution_time
    def __post_init__(self):
        assert len(self.access_token) > 0, "⚠️ Missing GitHub Token"
        assert len(self.user_name) > 0, "⚠️ User not connected"
        assert len(self.repo_name) > 0, "⚠️ Missing GitHub Repository"
        # assert len(self.branch) > 0
        full_repo_name = f"{self.user_name}/{self.repo_name}"
        if self._debug:
            print(f"....Connecting to {full_repo_name}")
        # print_stack()
        self.github = Github(self.access_token)
        self.repo = self.github.get_repo(full_repo_name)

        # Ensure the branch exists
        try:
            self.repo.get_branch(self.branch)
        except GithubException:
            raise ValueError(f"Branch {self.branch} does not exist.")

    # @trace_execution_time
    def read_content(self, file_name: str = "") -> str:
        if len(file_name) == 0:
            file_name = self.file_name
        if file_name in self.files.keys():
            return self.files[file_name].content
        elif self.parent is not None:
            return self.parent.read_content(file_name)
        raise ValueError(f"File '{file_name}' not found in cache.")

    # @trace_execution_time
    def save_content(self, content: str) -> str:
        if len(self.file_name) == 0:
            raise ValueError("File name must be specified before saving content.")

        file_name = f"{self.directory}/{self.file_name}"
        commit_message = f"Updated from lightcode: {self.file_name}"

        try:
            existing_file = self.repo.get_contents(file_name, ref=self.branch)
            # Update the file if it exists
            response = self.repo.update_file(path=existing_file.path,
                                  message=commit_message,
                                  content=content,
                                  sha=existing_file.sha,
                                  branch=self.branch)
            #print(f"Saved content to {self.file_name} in GH {self.directory} # {commit_message} on {self.repo_name} {self.branch = }")
            #print(f"Response: {response}")

        except GithubException as e:
            print(f"Error: {e}")
            if e.status == 404:
                # File does not exist, so create a new one
                self.repo.create_file(file_name, commit_message, content, branch=self.branch)
            else:
                raise e

        # Updating the local cache
        self.files[file_name] = FileHandler(name=file_name, content=content, timestamp=time.ctime(), sha="")
        return file_name

    # @trace_execution_time
    def save_content_as(self, content: str, new_file_name: str) -> str:
        assert new_file_name != "", "⚠️ New file name must be specified."

        new_path = f"{self.directory}/{new_file_name}"
        commit_message = f"Saved as new file from lightcode: {new_path}"

        try:
            # Update the file if it exists
            response = self.repo.create_file(path=new_path,
                                  message=commit_message,
                                  content=content,
                                  branch=self.branch)
            #print(f"Saved content to {self.file_name} in GH {self.directory} # {commit_message} on {self.repo_name} {self.branch = }")
            #print(f"Response: {response}")

        except GithubException as e:
            print(f"Error: {e}")
            if e.status == 404:
                # File does not exist, so create a new one
                self.repo.create_file(file_name, commit_message, content, branch=self.branch)
            else:
                raise e

        # Updating the local cache
        self.files[new_file_name] = FileHandler(name=new_file_name, content=content, timestamp=time.ctime(), sha="")
        return new_file_name


    # @trace_execution_time
    def scan_files(self, reload: bool = False) -> List[str]:
        if reload:
            self.files.clear()

        folder_content: List[ContentFile] = self.repo.get_contents(self.directory)

        file_names = []
        for content_file in folder_content:
            if content_file.type == "file":  # Check if the item is a file
                self._load_file(content_file)
                file_names.append(content_file.name)

        return file_names

    # @trace_execution_time
    def scan_file(self, file_name: str) -> str:
        if file_name not in self.files.keys():
            return self.parent.scan_file(file_name)
        content_file: ContentFile = self.repo.get_contents(f"{self.directory}/{file_name}")
        self._load_file(content_file)
        return file_name

    # @trace_execution_time
    def _load_file(self, content_file):
        file_content: ContentFile = self.repo.get_contents(content_file.path)
        content: str = file_content.decoded_content.decode("utf-8")
        file_handler = FileHandler(name=content_file.name, content=content)
        file_handler.timestamp = content_file.last_modified
        file_handler.icon = "￥"
        commits = self.repo.get_commits(path=content_file.path)
        file_handler.sha = commits[0].sha  # last one
        file_handler.message = commits[0].commit.message
        self.files[content_file.name] = file_handler
        # for commit in commits:
        #     sha = commit.sha
        #     message = commit.commit.message
        #     date = commit.commit.author.date

    def check_access(self) -> (bool, Any):
        """
        Checks access to github
        :return: (bool, Any) - True if access is granted + info/credits.
        """

        # Get the rate limit status
        rate_limit = self.github.get_rate_limit()

        if self._debug:
            print(f"{rate_limit = }")

        if rate_limit.core.remaining == 0:
            return False, "Rate limit exceeded"

        if rate_limit.search.remaining == 0:
            return False, "Rate limit exceeded"

        return True, rate_limit

    def create_file(self, file_name: str, content: str) -> str:
        """
        Create a new file in the GitHub repository.

        :param file_name: Name of the file to create (e.g., "example.py")
        :param content: Text content to write into the file
        :return: Full path of the created file (e.g., "modules/example.py")
        :raises FileExistsError: If the file already exists in the repo
        :raises GithubException: For any other API-related error
        """
        safe_dir = self.directory.lstrip("/")  # Ensure no leading slash
        full_path = f"{safe_dir}/{file_name}"
        commit_message = f"Created from LightCode: {file_name}"

        try:
            # Check if the file already exists
            self.repo.get_contents(full_path, ref=self.branch)
            raise FileExistsError(f"File '{full_path}' already exists in the repository.")
        except GithubException as e:
            if e.status == 404:
                # File does not exist — create it
                response = self.repo.create_file(
                    path=full_path,
                    message=commit_message,
                    content=content,
                    branch=self.branch
                )
                commit_sha = response["commit"].sha

                # Update local cache
                self.files[file_name] = FileHandler(
                    name=file_name,
                    content=content,
                    timestamp=time.ctime(),
                    sha=commit_sha,
                    icon="🆕",
                    message=commit_message
                )

                return full_path
            else:
                raise e