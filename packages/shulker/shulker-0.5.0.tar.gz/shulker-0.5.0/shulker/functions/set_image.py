import urllib3
import json
import math
from typing import Union
import sys
import os

from PIL import Image
import PIL
import requests
from io import BytesIO
import random

from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.BlockHandler import BlockHandler
from shulker.components.Zone import Zone

from shulker.functions.base_functions import *
from shulker.functions.set_block import meta_set_block, set_block

# TODO: Minecart method? -> https://www.youtube.com/watch?v=MEawKJm-t28

def generate_instructions_random(pixels, palette, coords, orientation, display_mode = "vertical"):
    instructions = generate_instructions(pixels, palette, coords, orientation, display_mode)
    random.shuffle(instructions["cmds"])
    return instructions

def generate_instructions(pixels, palette, coords, orientation, display_mode = "vertical"):
    
    instructions = {"cmds": [], "zone": None}
    
    x = 0

    for line in pixels:
        x += 1
        z = 0
        for pixel in line:
            block = color_picker(pixel, palette)
            if display_mode == "vertical":
                new_coords = BlockCoordinates(coords.x, coords.y + x, coords.z + z)
            else:
                new_coords = BlockCoordinates(coords.x + x, coords.y, coords.z + z)
            
            if orientation in block:
                block = block.replace(f"_{orientation}", "")

                if orientation == "side":
                    block.blockhandler.axis = "x"

                elif orientation == "top":
                    block.blockhandler.axis = "x"

            cmd = meta_set_block(
                new_coords,
                block,
                BlockHandler("replace"),
            )
            instructions["cmds"].append(cmd)
            z += 1
    else:
        instructions["zone"] = Zone(
            coords, BlockCoordinates(coords.x + x, coords.y, coords.z + z)
        )
        
    return instructions
        
def generate_instructions_spiral(pixels, palette, coords, orientation, display_mode = "vertical"):
    
    #TODO only handles vertical for now
    def add_instruction(x, y):
        block = color_picker(pixels[x][y], palette)
        if display_mode == "horizontal":
            relative_cursor = BlockCoordinates(coords.x + cursor[0], coords.y, coords.z + cursor[1])
        elif display_mode == "vertical":
            relative_cursor = BlockCoordinates(coords.x + cursor[0], coords.y + cursor[1], coords.z)
        
        cmd = meta_set_block(
                relative_cursor,
                block,
                BlockHandler("replace"),
            )
        instructions["cmds"].append(cmd)
        
    instructions = {"cmds": [], "zone": None}
    
    width = len(pixels[0])
    height = len(pixels)
    
    x_center = int(width / 2)
    y_center = int(height / 2)
    
    cursor = (x_center, y_center)
    add_instruction(cursor[0], cursor[1])
    
    
    side = 1
    mult = -1
    while len(instructions["cmds"]) < (width * height - side):
        
        for _ in range(1, side + 1):
            cursor = (cursor[0] + 1 * mult, cursor[1])
            add_instruction(cursor[0], cursor[1])
            
            
        for _ in range(1, side + 1):
            cursor = (cursor[0], cursor[1] + 1 * mult)
            add_instruction(cursor[0], cursor[1])
            
        mult = mult * -1
        side += 1
        
    else:
        for _ in range(1, side):
            cursor = (cursor[0] + 1 * mult, cursor[1])
            add_instruction(cursor[0], cursor[1])
        instructions["zone"] = Zone(
            coords, BlockCoordinates(coords.x + width, coords.y, coords.z + height)
        )

    return instructions

def generate_instructions_reverse_spiral(pixels, palette, coords, orientation, display_mode = "vertical"):
    instructions = generate_instructions_spiral(pixels, palette, coords, orientation, display_mode)
    instructions["cmds"] = instructions["cmds"][::-1]
    return instructions

def meta_set_image(
    image: Image, coords: BlockCoordinates, orientation: str, display_mode: str = "vertical", display_order = "normal"
) -> dict:

    
    pixels = list(image.getdata())
    
    width, height = image.size
    pixels = [pixels[i * width : (i + 1) * width] for i in range(height)]
    palette = get_palette(orientation)

    
    if display_order == "normal":
        instructions = generate_instructions(pixels, palette, coords, orientation, display_mode)
    elif display_order == "random":
        instructions = generate_instructions_random(pixels, palette, coords, orientation, display_mode)
    elif display_order == "spiral":
        instructions = generate_instructions_spiral(pixels, palette, coords, orientation, display_mode)
    elif display_order == "reverse_spiral":
        instructions = generate_instructions_reverse_spiral(pixels, palette, coords, orientation, display_mode)
    else: 
        instructions = {"cmds": [], "zone": None}
    return instructions


def set_image(
    source: str,
    coords: Union[BlockCoordinates, tuple],
    orientation: str = "side",
    url: bool = False,
    resize = None,
    display_mode: str = "vertical",
    display_order: str = "normal",
) -> Zone:
    """
    This function takes the path to an image or an URL
    (in which case, url must be passed as True), downloads it,
    and sends back the setblocks instruction to print the image
    in the provided orientation

    Orientation can either be "side", "top", "bottom" depending from where
    you want people to look at the image.

    If a player name is provided, the player will be teleported to make sure the
    printing doesn't happen out of bound (and therefore fail)
    """

    check_output_channel()

    if url == True:
        response = requests.get(source)
        image = Image.open(BytesIO(response.content))
    else: 
        image = Image.open(source) 
    
    if resize:
        image = image.convert("RGB").resize(resize)
    
    image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    if display_mode == "vertical":
        image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    if display_order == "spiral" or display_order == "reverse_spiral":
        image = image.rotate(90)

    coords = format_arg(coords, BlockCoordinates)

    if orientation not in ["side", "top", "bottom"]:
        raise ValueError(
            f"Orientation must either be side, top or bottom for set_image()"
        )

    instructions = meta_set_image(image, coords, orientation, display_mode, display_order)
    status = {
      "cmd": [],
      "zone": instructions["zone"]
    }
    
    for cmd in instructions["cmds"]:
        ret = post(cmd)
        if ret and ret != '':
          status['cmd'].append(ret)

    return True


def get_palette(orientation):

    try:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{path}/mc_data/palette.json") as f:
            palette = json.load(f)

    except FileNotFoundError:
        palette = create_palette()

    return palette[orientation]


def get_closest_color(pixel, block_palette, orientation):

    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/mc_data/block_list.json") as f:
        block_list = json.load(f)

    orientations = ["top", "bottom", "front"]
    for index, value in enumerate(orientations):
        if value == orientation:
            orientations.pop(index)

    excluded_block_tags = [
        "shulker",
        "sand",
        "powder",
        "glass",
        "front",
        "coral",
        "dead",
        "trapdoor",
        "chorus",
        "_ore",
    ]

    excluded_blocks = [
        "ice",
    ]

    best_delta = None

    for block in block_palette["averages"]:

        block_name = block["texture"].split("/")[-1]

        if any(other_orientation in block_name for other_orientation in orientations):
            continue

        if f"minecraft:{block_name}" not in list(block_list.keys()):
            continue

        elif any(to_exclude in block_name for to_exclude in excluded_block_tags):
            continue

        elif any(to_exclude == block_name for to_exclude in excluded_blocks):
            continue

        elif block["pixels"] != 256:
            continue

        elif block["stddev_rgb"] == 0.00000:
            continue

        delta = math.sqrt(
            (pixel[0] - block["rgba"][0]) ** 2
            + (pixel[1] - block["rgba"][1]) ** 2
            + (pixel[2] - block["rgba"][2]) ** 2
        )

        if best_delta is None or delta < best_delta:
            best_delta = delta
            best_match = block_name

    return best_match


def color_picker(pixel, palette):

    r = int(pixel[0] / 32)
    g = int(pixel[1] / 32)
    b = int(pixel[2] / 32)

    index = r * 64 + g * 8 + b
    return palette[str(index)]


def print_palette(coords, orientation="side"):
    palette = get_palette(orientation)

    n = 8
    for x in range(n):
        for y in range(n):
            for z in range(n):
                coords = BlockCoordinates(x * 3, y * 3 + 5, z * 3)

                set_block(
                    coords,
                    palette[str(x * 64 + y * 8 + z)],
                )


def create_palette():

    print(
        "It looks like this is the first time you're using set_image() and no pre-existing block palette was found. Please hold on while it's generating!"
    )

    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/mc_data/blocks_color.json") as f:
        block_palette = json.load(f)

    palette = {"side": {}, "top": {}, "bottom": {}}

    for orientation in ["side", "top", "bottom"]:

        print(f"-> Generating the palette for the '{orientation}' orientation")

        for i in range(0, 8):
            for j in range(0, 8):
                for k in range(0, 8):

                    block = get_closest_color(
                        (i * 32, j * 32, k * 32), block_palette, orientation
                    )

                    palette[orientation][str(i * 64 + j * 8 + k)] = block

    with open(f"{path}/mc_data/palette.json", "w+") as f:
        json.dump(palette, f, indent=4)

    return palette
