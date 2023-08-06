from typing import Union

from shulker.components.Block import Block
from shulker.components.BlockState import BlockState
from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.BlockHandler import BlockHandler

from shulker.functions.base_functions import *


def meta_set_block(coords: BlockCoordinates, block: Block, handler: Union[BlockHandler, None]) -> str:
    return f"setblock {coords} {block}{(' ' + str(handler)) if handler else ''}"


def set_block(
    coords: Union[BlockCoordinates, tuple],
    block: Union[Block, str],
    handler: Union[BlockHandler, str] = "replace",
) -> str:
    """
    Returns a bool that is set to True
    if no message was sent back by the game or the
    message itself if there was an issue

    Available handlers:
        'replace' — The old block drops neither itself nor any contents. Plays no sound.
        'destroy' — The old block drops both itself and its contents (as if destroyed by a player). Plays the appropriate block breaking noise.
        'keep' — Only air blocks are changed (non-air blocks are unchanged).

    Defaults to 'replace'
    """

    check_output_channel()

    coords = format_arg(coords, BlockCoordinates)
    block = format_arg(block, Block)
    handler = format_arg(handler, BlockHandler)

    cmd = meta_set_block(coords, block, handler)

    status = post(cmd)

    return status


meta_definition = {
    "setblock": {
        "type": "literal",
        "children": {
            "pos": {
                "type": "argument",
                "parser": BlockCoordinates,
                "children": {
                    "block": {
                        "type": "argument",
                        "parser": BlockState,
                        "children": {
                            "destroy": {"type": "literal", "executable": True},
                            "keep": {"type": "literal", "executable": True},
                            "replace": {"type": "literal", "executable": True},
                        },
                        "executable": True,
                    }
                },
            }
        },
    }
}
