import importlib
import sys
import os
import importlib.util
import yaml
from types import ModuleType
import streamlit as st

from config.settings import DEFAULT_MODULE_DIRECTORY
from usecases.common.backend.file_access import DiskManager, GitManager
from usecases.common.backend.module_loader import ModuleLoader


def create_module(sel_file: str, reload: bool = False, debug: bool = False) -> ModuleLoader:

    if "key_loaders" not in st.session_state:
        st.session_state.key_loaders = {}
    if (sel_file not in st.session_state.key_loaders.keys()) or reload:

        repo = get_dynamic_repo()

        if repo and repo.check_file_exists(f"{sel_file}.yaml"):
            ...
        else:
            if "static_repo" not in st.session_state:
                repo = DiskManager(directory=DEFAULT_MODULE_DIRECTORY)
                st.session_state.static_repo = repo
                repo.scan_files(reload=reload)
            else:
                repo = st.session_state.static_repo
                # repo = st.session_state.key_loaders[sel_file]._repo

        if not repo.check_file_exists(f"{sel_file}.yaml"):
            return None

        yaml_str = repo.read_content(f"{sel_file}.yaml")

        loader = ModuleLoader(module_name=sel_file, _debug=debug,
                              yaml_str=yaml_str, _repo=repo)
        loader.load()
        st.session_state.key_loaders[sel_file] = loader

    else:
        loader = st.session_state.key_loaders[sel_file]



    # pymodule = importlib.import_module("welcome")

    return loader



def clone_module(module_loader: ModuleLoader, reload: bool = False, debug: bool = False) -> ModuleLoader:

    sel_file = f"{module_loader.module_name}_clone"

    if "key_loaders" not in st.session_state:
        st.session_state.key_loaders = {}
    if (sel_file not in st.session_state.key_loaders.keys()) or reload:

        if False:
            repo = get_dynamic_repo()

            if repo and repo.check_file_exists(f"{sel_file}.yaml"):
                ...
            else:
                if "static_repo" not in st.session_state:
                    repo = DiskManager(directory=DEFAULT_MODULE_DIRECTORY)
                    st.session_state.static_repo = repo
                    repo.scan_files(reload=reload)
                else:
                    repo = st.session_state.static_repo
                    # repo = st.session_state.key_loaders[sel_file]._repo

            if not repo.check_file_exists(f"{sel_file}.yaml"):
                return None

            yaml_str = repo.read_content(f"{sel_file}.yaml")

        yaml_str = module_loader.yaml_str

        loader = ModuleLoader(module_name=sel_file, _debug=debug, yaml_str=yaml_str, _repo=module_loader._repo)
        loader.load()
        st.session_state.key_loaders[sel_file] = loader

    else:
        loader = st.session_state.key_loaders[sel_file]



    # pymodule = importlib.import_module("welcome")

    return loader



def exec_module(loader: ModuleLoader) -> ModuleLoader:
    loader.run()
    return loader

def import_loader(sel_file: str) -> ModuleLoader:
    loader = create_module(sel_file)
    exec_module(loader)
    return loader

def create_dynamic_module(module_name: str) -> ModuleType:
    loader = create_module(module_name)
    return loader.module.value

def import_module(module_name: str, designing: bool = False, reload: bool = False, run: bool = True) -> ModuleType:
    loader = create_module(sel_file=module_name, reload=reload)
    # print(f"import_module: {module_name}, {loader is None = }")
    loader.module.designing = designing
    if run:
        exec_module(loader)
    return loader.module.value

def preview_module(module_loader: ModuleLoader, designing: bool = False, reload: bool = False, run: bool = True) -> ModuleType:
    loader = clone_module(module_loader, reload=reload)
    # print(f"import_module: {module_name}, {loader is None = }")
    loader.module.designing = designing
    if run:
        exec_module(loader)
    return loader.module.value


def get_module(module_name: str) -> ModuleType:
    return st.session_state.key_loaders[module_name].module.value

def get_mud() -> ModuleType:
    module_name = st.session_state.mud
    return st.session_state.key_loaders[module_name].module.value

def get_loader(sel_file: str) -> ModuleLoader:
    if sel_file not in st.session_state.key_loaders.keys():
        return None
    return st.session_state.key_loaders[sel_file]

def get_dynamic_repo() -> GitManager:
    if "dynamic_repo" in st.session_state.keys():
        if st.session_state.dynamic_repo is not None:
            return st.session_state.dynamic_repo

    if "user_name" not in st.session_state:
        return None

    user_name = st.session_state.user_name
    repo_name = st.session_state.user_info[0]
    access_token = st.session_state.user_info[1]
    repo_manager = GitManager(
        directory="/modules",
        repo_name=repo_name,
        access_token=access_token,
        user_name=user_name
    )
    repo_manager.parent = st.session_state.static_repo
    st.session_state.dynamic_repo = repo_manager
    return repo_manager


# Custom Loader that creates the module from the YAML file
class YamlLoader(importlib.abc.Loader):
    def __init__(self, yaml_file: str):
        self.yaml_file = yaml_file

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType | None:
        # if self.yaml_file in st.session_state.key_loaders:
        #     loader = st.session_state.key_loaders[self.yaml_file]
        #     exec_module(loader)
        return None

    def exec_module(self, module: ModuleType) -> None:
        dynamic_module = create_dynamic_module(self.yaml_file)
        loader = st.session_state.key_loaders[self.yaml_file]
        exec_module(loader)
        module.__dict__.update(dynamic_module.__dict__)


# Custom Finder that looks for a YAML file for the module
class YamlFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: list | None,
                  target: ModuleType | None) -> importlib.machinery.ModuleSpec | None:
        yaml_file = f"{fullname}"

        if create_module(yaml_file) is not None:
            return importlib.util.spec_from_loader(fullname, YamlLoader(yaml_file))

        return None  # Let other finders handle it if YAML is not found


# Add the custom finder to the system's meta path
sys.meta_path.insert(0, YamlFinder())
