from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.Block import Block
from shulker.components.Zone import Zone
from shulker.components.Entity import Entity
from shulker.server.singleton import singleton
import json
import os
import sys

__all__ = [
    "check_output_channel",
    "post",
    "default_check",
    "execute_check",
    "unexpected_status",
    "format_arg",
    "nest",
    "entity_list"
]


def entity_list():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/mc_data/registries.json") as f:
        registries = json.load(f)
    
    entities = []
    for entity in registries["minecraft:entity_type"]["entries"].keys():
        entities.append(entity.replace("minecraft:", ""))
        
    return entities


def check_output_channel():
    if singleton.check_status():
        return singleton
    else:
        raise NoOutputChannelProvided(f"No output channel was initialized in the code")


def post(cmd: str):
    return singleton.post(cmd)


def nesting_process(commands: list, base_coords: BlockCoordinates, set_plane: bool):

    from shulker.functions.set_block import meta_set_block
    from shulker.functions.summon import meta_summon

    # The activator rail, first passenger, that will get powered
    # once its host the redstone block, has settled on the ground
    rail = Entity('falling_block')
    rail.nbt.id = rail.descriptor
    rail.nbt.BlockState = {'Name':'activator_rail'}
    rail.nbt.Time = 1

    passengers = []

    # This is the pack of third level passengers, this bit of the third level
    # are the custom commands of the nesting
    for command in commands:
      main_cmds_minecart = Entity('command_block_minecart')
      main_cmds_minecart.nbt.id = main_cmds_minecart.descriptor
      main_cmds_minecart.nbt.Command = command
      passengers.append(main_cmds_minecart.nbt)

    # This pack of the third level passengers represents the last
    # part of the nesting, the commands that will kill the contraption

    # This part is the command block that deletes the blocks
    zone = Zone(base_coords, base_coords.offset(0, -2 if not set_plane else -3, 0))
    block = Block('command_block')
    block.nbt = {'auto':1, 'Command':f'fill {zone} air'}

    command = meta_set_block(base_coords, block, "replace")

    deleter_minecart = Entity('command_block_minecart')
    deleter_minecart.nbt.id = deleter_minecart.descriptor
    deleter_minecart.nbt.Command = command
    passengers.append(deleter_minecart.nbt)

    # This part is the command block that kills the contraption entities
    command = 'kill @e[distance=..1]'

    killer_minecart = Entity('command_block_minecart')
    killer_minecart.nbt.id = killer_minecart.descriptor
    killer_minecart.nbt.Command = command
    passengers.append(killer_minecart.nbt)

    rail.nbt.Passengers = passengers

    # The base of the contraption, the redstone block that will power
    # its next passenger, the activator rail.
    base = Entity("falling_block")
    base.nbt.BlockState = {'Name':'redstone_block'}
    base.nbt.Time = 1
    base.nbt.Passengers = [rail.nbt]

    cmd = meta_summon(base.descriptor, base_coords.offset(0, 0, 0), base.nbt)
    
    return cmd


def nest_commands(commands: list, base_coords: BlockCoordinates, set_plane):
  
    # NOTE: The byte size of the string also depends on using do
    # double or single quotes 
    
    # This is 49, the size of an empty string
    string_overhead = sys.getsizeof('')
    
    # This is 88, the size of a string with the value of an empty command block minecart
    # We substract the overhead because it will be put inside the command
    string_addition = sys.getsizeof('{id:"command_block_minecart",Command:""},') - string_overhead
    
    # This is 356, the size of the base command if you substract the empty command block minecart
    # it is substracted because it will be added for each commands
    cmd = nesting_process([""], base_coords, set_plane)
    base_cmd_size = sys.getsizeof(cmd) - string_addition
    
    # We save the base size, and create a variable that will be used to
    # track the current size of the nest we're creating (= pkg/package)
    current_cmd_size = base_cmd_size
    
    nests = []
    pkg = []
    
    # While there are still any commands left to be nested
    while len(commands):
      
      # Determine the size of the next command
      next_command_size = sys.getsizeof(commands[0]) + string_addition - string_overhead
      
      # If it fits in the current nest, add it to the nest (pkg)
      if current_cmd_size + next_command_size < 1400:
        current_cmd_size += next_command_size
        pkg.append(commands.pop(0))
      
      # Otherwise, create a new nest (pkg) and add the previous nest in the list of nests
      else:
        current_cmd_size = base_cmd_size
        nests.append(pkg)
        pkg = []
    else:
      # Add the last nest to the list of nests
      nests.append(pkg)
    
    return nests


def place_nests(nests: list, base_coords: BlockCoordinates, set_plane, plane_block):
  
  from shulker.functions.set_zone import meta_set_zone

  # If set_plane is set to true, we fill a zone with a plane that will
  # be used to place the nests on top of it
  
  cmds = []
  
  if set_plane:
    wideness = round(len(nests) / 16)
    zone = Zone(base_coords.offset(0, -3, 0), base_coords.offset(0 + wideness, -3, len(nests) - 1 % 16))
    cmd = meta_set_zone(zone, plane_block, "replace")
    cmds.append(cmd)
  
  for i, nest in enumerate(nests):
    cmd = nesting_process(nest, base_coords.offset(round(i/16), 0, i % 16), set_plane)
    cmds.append(cmd)

  return cmds
  
  
def nest(commands: list, base_coords: BlockCoordinates, set_plane=True, plane_block=Block('barrier'), dry_run=False):
  nests = nest_commands(commands, base_coords, set_plane)
  
  cmds = place_nests(nests, base_coords, set_plane, plane_block)
  
  if dry_run:
    return cmds
  else:
    for cmd in cmds:
      post(cmd)


def default_check(response):
    if response == "":
        return True
    else:
        return response


def execute_check(response):
    if response == "Test passed":
        return True
    elif response == "Test failed":
        return False
    else:
        return response


def unexpected_status(file_name, status):
    raise UnexpectedReturn(
        f'The say command in {file_name.split("/")[-1]} didn\'t properly function and returned: "{status}"'
    )


def format_arg(argument, component):
    if isinstance(argument, component):
        return argument

    if isinstance(argument, str):
        return component(argument)
    elif isinstance(argument, tuple):
        return component(*argument)
    elif isinstance(argument, list):
        return component(*argument)
    else:
        raise InvalidArgumentType(
            f'Invalid argument type, could not parse "{argument}" as a valid component.'
        )


class InvalidArgumentType(Exception):
    pass


class UnexpectedReturn(Exception):
    pass


class NoOutputChannelProvided(Exception):
    pass
