from pathlib import Path
from stat import SF_SETTABLE

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


def get_languages() -> list[str]:
    return PROGRAMMING_LANGUAGES


PUBLIC_PATH = Path("public")
STATIC_PATH = Path("static")
CONTENT_PATH = Path("content")
TEMPLATE_PATH: Path = Path("template.html")


def get_public_path():
    return PUBLIC_PATH


def get_static_path():
    return STATIC_PATH


def get_content_path():
    return CONTENT_PATH


def get_template_path() -> Path:
    return TEMPLATE_PATH
