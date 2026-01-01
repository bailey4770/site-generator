from pathlib import Path
import logging

PROGRAMMING_LANGUAGES = [
    "python",
    "go",
    "javascript",
    "typescript",
    "java",
    "c",
    "cpp",
    "csharp",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "rust",
    "scala",
    "perl",
    "r",
    "matlab",
    "dart",
    "lua",
    "groovy",
    "bash",
    "shell",
    "powershell",
    "sql",
    "html",
    "css",
    "xml",
    "json",
    "yaml",
    "markdown",
    "objective-c",
    "haskell",
    "elixir",
    "erlang",
    "clojure",
    "julia",
    "fortran",
    "cobol",
    "assembly",
    "vhdl",
    "verilog",
]
PUBLIC_PATH = Path("public")
STATIC_PATH = Path("static")
CONTENT_PATH = Path("content")
TEMPLATE_PATH: Path = Path("template.html")
LOGGING_LEVEL = logging.INFO


def get_languages() -> list[str]:
    return PROGRAMMING_LANGUAGES


def get_public_path() -> Path:
    return PUBLIC_PATH


def get_static_path() -> Path:
    return STATIC_PATH


def get_content_path() -> Path:
    return CONTENT_PATH


def get_template_path() -> Path:
    return TEMPLATE_PATH


def get_logging_level():
    return LOGGING_LEVEL
