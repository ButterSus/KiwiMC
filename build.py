from __future__ import annotations

# Default libraries
# -----------------

import toml
import json
from argparse import ArgumentParser
from typing import TypedDict, Any, List
from pathlib import Path

# Custom libraries
# ----------------

from src.kiwiTokenizer import Tokenizer
from src.kiwiAST import AST
from src.assets.kiwiTools import dumpAST, dumpTokenizer


# Dict with default values
# ------------------------

class DefaultDict(dict):
    defaultDict: dict

    def __init__(self, defaultDict: dict, value: dict):
        self.defaultDict = defaultDict
        super().__init__(value)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, __key: str) -> Any:
        result = super().get(__key)
        if result is None:
            return self.defaultDict.get(__key)
        return result

    def toDict(self) -> dict:
        return dict(self.items())


# Config TOML
# -----------

class ConfigOptions(TypedDict):
    include_directories: List[str]
    entry_function: str
    output_directory: str
    default_scope: str


configOptions: ConfigOptions = {
    "include_directories": [],
    "entry_function": "main",
    "output_directory": "bin",
    "default_scope": "public"
}


class ConfigProject(TypedDict):
    project_name: str
    entry_file: str
    mc_version: str


configProject: ConfigProject = {
    "project_name": "untitled",
    "entry_file": "main",
    "mc_version": "1.16.5"
}


class ConfigTOML(TypedDict):
    project: ConfigProject
    options: ConfigOptions


configTOML: ConfigTOML = {
    "project": configProject,
    "options": configOptions
}


# Terminal arguments
# ------------------

class ConfigTerminal(TypedDict):
    path: str
    debug: bool
    create_project: bool


# General config
# --------------

class ConfigGeneral(ConfigProject, ConfigOptions, ConfigTerminal):
    pass


class Terminal:
    """
    The main task of this class is
    - collect build options for frontend and backend without checking correctness
    """

    argparser: ArgumentParser
    arguments: ConfigTerminal
    configGeneral: ConfigGeneral
    pathGeneral: Path

    # Config options
    # --------------

    def __init__(self):
        self.get_arguments()
        self.get_options()

    def get_arguments(self):
        self.argparser = ArgumentParser(description='Kiwi Datapack Official Compiler')
        self.argparser.add_argument('path', type=str, help='Path to your project')
        self.argparser.add_argument('--debug', default=False, action='store_true',
                                    help='Compiles grammar and print details (for devs)')
        self.argparser.add_argument('--create-project', default=False, action='store_true',
                                    help='Creates new project')
        self.arguments = vars(self.argparser.parse_args())
        self.pathGeneral = Path(self.arguments['path'])

    def get_options(self):
        def combineDictionaries(*values: DefaultDict | dict) -> dict:
            result = dict()
            for value in values:
                if isinstance(value, DefaultDict):
                    result |= value.toDict()
                else:
                    result |= value
            return result

        currentConfigTOML: ConfigTOML \
            = DefaultDict(configTOML, toml.load(str(self.pathGeneral / 'kiwi_project.toml')))
        currentConfigProject: ConfigProject \
            = DefaultDict(configProject, currentConfigTOML['project'])
        currentConfigOptions: ConfigOptions \
            = DefaultDict(configOptions, currentConfigTOML['options'])
        self.configGeneral = combineDictionaries(
            self.arguments, currentConfigProject, currentConfigOptions)


# General directories
# -------------------

class Directories(TypedDict):
    bin: Path
    data: Path
    project: Path
    functions: Path


class Constructor:
    """
    The main task of this class is
    - construct base for compiler
    """

    configGeneral: ConfigGeneral
    directories: Directories

    def __init__(self, configGeneral: ConfigGeneral):
        self.configGeneral = configGeneral
        self.directories = dict()
        self.folders()
        self.files()

    def folders(self):
        self.directories['bin'] = Path(self.configGeneral['output_directory'])
        self.directories['bin'].mkdir(exist_ok=True)

        self.directories['data'] = Path(self.directories['bin'] / 'data')
        self.directories['data'].mkdir(exist_ok=True)

        self.directories['project'] = Path(self.directories['data'] / self.configGeneral['project_name'])
        self.directories['project'].mkdir(exist_ok=True)

        self.directories['functions'] = Path(self.directories['project'] / 'functions')
        self.directories['functions'].mkdir(exist_ok=True)

    def files(self):
        pass


class Builder:
    """
    The main task of this class is
    - connect all parts of compiler together
    """

    # Parts of compiler
    # -----------------

    terminal: Terminal
    constructor: Constructor
    tokenizer: Tokenizer
    ast: AST

    # General parameters
    # ------------------

    configGeneral: ConfigGeneral

    def __init__(self):
        self.terminal = Terminal()
        self.configGeneral = self.terminal.configGeneral
        self.constructor = Constructor(self.configGeneral)
        with open(self.configGeneral['entry_file']) as file:
            self.tokenizer = Tokenizer(file.read())
            self.ast = AST(self.tokenizer.lexer)
        print(dumpAST(self.ast.module))


if __name__ == '__main__':
    Builder()
