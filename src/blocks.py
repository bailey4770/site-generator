from enum import Enum
import logging
from config import get_logging_level

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=get_logging_level(),
)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []

    current_block = ""
    for line in markdown.splitlines():
        if not current_block.startswith("```"):
            line = line.strip()

        if (not line or line == "\n") and current_block:
            blocks.append(current_block)
            current_block = ""
            continue

        if current_block:
            current_block += "\n"

        current_block += line

    blocks.append(current_block)
    logger.debug("markdown_to_blocks: blocks: %s", blocks)
    return blocks


def get_block_type(string_block: str) -> BlockType:
    def _is_ordered_list(lines: list[str]):
        number = 1

        for line in lines:
            parts = line.split(" ")
            if parts[0] != f"{number}.":
                return False
            number += 1

        return True

    parts = string_block.split()
    lines = string_block.splitlines()

    unordered_prefixes = ["-", "+", "*"]

    if all(char == "#" for char in parts[0]) and len(parts[0]) <= 6:
        return BlockType.HEADING
    elif string_block.strip().startswith("```") and string_block.strip().endswith(
        "```"
    ):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif any(
        all(line.split()[0] == prefix for line in lines)
        for prefix in unordered_prefixes
    ):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
