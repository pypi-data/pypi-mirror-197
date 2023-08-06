import json
import os

from typing import Union

from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.NBT import NBT
from shulker.components.Coordinates import Coordinates
from shulker.components.Entity import Entity

from shulker.functions.base_functions import *


def meta_summon(entity: str, coords: BlockCoordinates, nbt_data: NBT) -> str:
    return f"summon {entity} {coords} {nbt_data}"


def summon(
    entity: Union[Entity, str],
    coords: Union[BlockCoordinates, Coordinates, tuple],
    nbt_data: Union[NBT, dict, str, None] = None
) -> str:
    """
    Summons an entity at coords, can be provided nbt_data
    """

    check_output_channel()
        
    if type(entity) is str:
      entities = entity_list()
    elif type(entity) is Entity:
      if entity.nbt is not None and nbt_data == None:
        nbt_data = entity.nbt
        entity.nbt = ""
        
    if type(entity) is not str and type(entity) is not Entity:
        raise TypeError(f"Expected type str or Entity, got {type(entity)}")
    elif type(entity) is str and entity.replace("minecraft:", "") not in entities:
        raise ValueError(f"Entity {entity} is not a valid entity")
    
    if nbt_data is not None:
        nbt_data = format_arg(nbt_data, NBT)
    else:
        nbt_data = ""

    coords = format_arg(coords, Coordinates)
        
    cmd = meta_summon(entity, coords, nbt_data)

    status = post(cmd)
    
    return status
