from typing import Union
from shulker.functions.base_functions import *
from shulker.components.Coordinates import Coordinates
import re

############ SAY ############

def meta_say(text: str) -> str:
    return f"say {text}"

def say(text: str) -> str:
    """Sends a message in the chat"""
    check_output_channel()
    
    cmd = meta_say(text)
    
    status = post(cmd)
    
    return status

######## BAN & KICK ########

def meta_ban(target: str, reason: str) -> str:
    return f"ban {target} {reason}"

def meta_banlist(option: str) -> str:
    return f"banlist {option}"

def ban(target: str, reason: Union[str, None]) -> str:
    """This function bans a player"""
    check_output_channel()
    
    if reason is None:
        reason = ""
        
    cmd = meta_ban(target, reason)
    
    status = post(cmd)
    
    return status
 
def ban_ip(target: str, reason: str) -> str:
    """This function bans an IP"""
    check_output_channel()
    
    cmd = meta_ban(target, reason)
    
    status = post(cmd)
    
    return status
        
def banlist(option: str) -> str:
    """Fetches the banlist"""
    check_output_channel()
    
    cmd = meta_banlist(option)
    
    status = post(cmd)
    
    return status

def meta_kick(target: str, reason: str) -> str:
    return f"kick {target} {reason}"

def kick(target: str, reason: Union[str, None]) -> str:
    """Kicks a player"""
    check_output_channel()
    
    if reason is None:
        reason = ""
        
    cmd = meta_kick(target, reason)
    
    status = post(cmd)
    
    return status

def meta_pardon(target: str) -> str:
    return f"pardon {target}"

def meta_pardon_ip(target: str) -> str:
    return f"pardon-ip {target}"

def pardon(target: str) -> str:
    """Unbans a player"""
    check_output_channel()
    
    cmd = meta_pardon(target)
    
    status = post(cmd)
    
    return status

def pardon_ip(target: str) -> str:
    """This function unbans an IP"""
    check_output_channel()
    
    cmd = meta_pardon_ip(target)
    
    status = post(cmd)
    
    return status

############ OP ############

def meta_op(target: str) -> str:
    return f"op {target}"

def meta_deop(target: str) -> str:
    return f"deop {target}"

def op(target: str) -> str:
    """Gives an operator status to a player"""
    check_output_channel()
    
    cmd = meta_op(target)
    
    status = post(cmd)
    
    return status
        
def deop(target: str) -> str:
    """Removes an operator status from a player"""
    check_output_channel()
    
    cmd = meta_deop(target)
    
    status = post(cmd)
    
    return status
        
############# SEED #############

def meta_seed() -> str:
    return f"seed"

def seed() -> str:
    """Fetches the seed of the world and return it as a string"""
    check_output_channel()
    
    cmd = meta_seed()
    
    status = post(cmd)
    
    seed = re.match(r"Seed: \[(-{0,1}(\d+))\]", status)
    return seed.group(1)

############# DIFFICULTY #############

def meta_set_difficulty(option: str) -> str:
    return f"difficulty {option}"

def meta_get_difficulty() -> str:
    return f"difficulty"

def set_difficulty(option: str) -> str:
    """Sets the difficulty of the world"""
    check_output_channel()
    
    cmd = meta_set_difficulty(option)
    
    status = post(cmd)
    
    return status
        
def get_difficulty() -> Union[bool, str]:
    """Fetches the difficulty of the world"""
    check_output_channel()
    
    cmd = meta_get_difficulty()
    
    status = post(cmd)
    
    difficulty = re.match(r"The difficulty is (\w+)", status)
    return difficulty.group(1)

########### WEATHER ###########

def meta_weather(option: str) -> str:
    return f"weather {option}"

def weather(option: str) -> str:
    """Sets the weather of the world
    Options: clear, rain, thunder"""
    
    check_output_channel()
    
    cmd = meta_weather(option)
    
    status = post(cmd)
    
    return status
        
########### MSG ###########

def meta_msg(target: str, message: str) -> str:
    return f"msg {target} {message}"
  
def msg(target: str, message: str) -> str:
    """Sends a private message to a player"""
    
    check_output_channel()
    
    cmd = meta_msg(target, message)
    
    status = post(cmd)
    
    return status

########### GAMEMODE ###########

def meta_default_gamemode(option: str) -> str:
    return f"defaultgamemode {option}"

def meta_gamemode(target: str, option: str) -> str:
    return f"gamemode {option} {target}"

def gamemode(target: str, option: str) -> str:
    """Sets the gamemode of a player
    Available options: survival, creative, adventure, spectator"""
    
    check_output_channel()
    
    cmd = meta_gamemode(target, option)
    
    status = post(cmd)
    
    return status
        
def default_gamemode(option: str) -> Union[bool, str]:
    """Sets the default gamemode of the world
    Available options: survival, creative, adventure, spectator"""
    
    check_output_channel()
    
    cmd = meta_default_gamemode(option)
    
    status = post(cmd)
    
    return status
    
########### TIME ###########

def meta_query_time(option: str) -> str:
    return f"time query {option}"

def query_time(option: str = "day") -> str:
    """Fetches the time of the world and returns it as a string
    Available options: day, daytime, gametime"""
    
    check_output_channel()
    
    cmd = meta_query_time(option)
    
    status = post(cmd)
        
    time = re.match(r"The time is (\d+)", status)
    return time.group(1)

def meta_add_time(value: str, option: str) -> str:
    return f"time add {value}{option}"

def add_time(value: int, option: str = "tick") -> str:
    """Adds time to the world
    Available options: day, second, tick"""
    
    check_output_channel()
    
    option = option[0]
    
    cmd = meta_add_time(value, option)
    
    status = post(cmd)
    
    return status
        
def meta_set_time(value: int, option: str) -> str:
    return f"time set {value}{option}"

def set_time(value: int, option: str = "tick") -> str:
    """Sets the time of the world
    Available options: day, second, tick"""
    
    check_output_channel()
    
    option = option[0]
    
    cmd = meta_set_time(value, option)
    
    status = post(cmd)
    
    return status
        
def meta_time(option: str) -> str:
    return f"time set {option}"

def time(option: str) -> str:
    """Sets the time of the world
    Available options: day, midnight, night, noon"""
    
    check_output_channel()
    
    cmd = meta_time(option)
    
    status = post(cmd)
    
    return status
        
########### EXPERIENCE ###########

def meta_xp_query(target: str, option: str) -> str:
    return f"xp query {target} {option}"

def xp_query(target: str, option: str) -> str:
    """Fetches the experience of a player and return it as a string
    Available options: levels, points"""
    
    check_output_channel()
    
    cmd = meta_xp_query(target, option)
    
    status = post(cmd)
    
    xp = re.findall(r"(\d+) experience " + option, status)
    return xp[0]

########### WHITELIST ###########

def meta_get_whitelist() -> str:
    return "whitelist list"

def get_whitelist() -> list:
    """Fetches the whitelist of the world and return as a list"""
    
    check_output_channel()
    
    cmd = meta_get_whitelist()
    
    status = post(cmd)[:-4]
        
    whitelist = status.split("players: ")[1].split(", ")
    return whitelist

def meta_toggle_whitelist(option: str) -> str:
    return f"whitelist {option}"

def toggle_whitelist(option: str) -> str:
    """Toggles the whitelist of the world
    Available options: on, off"""
    
    check_output_channel()
    
    cmd = meta_toggle_whitelist(option)
    
    status = post(cmd)
    
    return status
        
def meta_reload_whitelist() -> str:
    return f"whitelist reload"

def reload_whitelist() -> str:
    """Reloads the whitelist of the world"""
    
    check_output_channel()
    
    cmd = meta_reload_whitelist()
    
    status = post(cmd)
    
    return status
        
def meta_update_whitelist(option: str, target: str) -> str:
    return f"whitelist {option} {target}"

def update_whitelist(option: str, target: str) -> str:
    """Updates the whitelist of the world
    Available options: add, remove"""
    
    check_output_channel()
    
    cmd = meta_update_whitelist(option, target)
    
    status = post(cmd)
    
    return status
        
############ ADMIN ############

def meta_stop() -> str:
    return "stop"

def stop() -> str:
    """Stops the server"""
    
    check_output_channel()
    
    cmd = meta_stop()
    
    status = post(cmd)
    
    return status
        
def meta_save_all() -> str:
    return "save-all"

def save_all() -> Union[bool, str]:
    """This function saves the world"""
    
    check_output_channel()
    
    cmd = meta_save_all()
    
    status = post(cmd)
    
    return status
        
def meta_toggle_save(option: str) -> str:
    return f"save-{option}"

def toggle_save(option: str) -> str:
    """Toggles the auto-save of the world
    Available options: on, off"""
    
    check_output_channel()
    
    cmd = meta_toggle_save(option)
    
    status = post(cmd)
    
    return status
        
############# HELP #############

def meta_help(value: str) -> str:
    return f"help {value}"

def parse_help(prepender = ""):
    
    cmd = meta_help(prepender)
    
    data = post(cmd)
        
    # Remove all \x1b[.. color code from the status
    data = re.sub(r"\x1b\[[0-9;]*m", "", data)
    
    # Find the number of help pages
    nb_pages = re.findall(r" \(\d+/(\d+)\)", data)
    
    if nb_pages:
        nb_pages = nb_pages[0]
    elif " Help: " in data and not nb_pages:
        nb_pages = 1
    else:
        raise Exception("No help found")
        
    help_cmds = {}
    for page in range(1, int(nb_pages) + 1):
                
        cmd = meta_help(prepender + str(page))
        
        data = post(cmd)
            
        data = re.sub(r"\x1b\[[0-9;]*m", "", data)
        lines = data.splitlines()[(1 if page > 1 else 2):]
        
        for line in lines:
            if not line.startswith("/") and ":" not in line:
                continue
            splitted = line.split(": ")
            command = splitted[0]
            value = splitted[1]
            help_cmds[command] = value
    
    return help_cmds

def help(value: str = "") -> dict:
    """Fetches the help of the world and return a dict of it
    If a value is specified it will fetch the help of the value only"""
    
    check_output_channel()

    cmds = parse_help(value)
    for key in cmds:
        if not key.startswith('/'):
            cmds[key] = parse_help(prepender=key + " ")
            
    return cmds

############# LIST #############

def meta_list_players(uuids: bool = False) -> str:
    if uuids:
        uuids = "uuids"
    else:
        uuids = ""
    return f"list {uuids}"

def list_players(uuids: bool = False) -> list:
    """Fetches the list of players in the world
    If uuids is set to True it will be a list of uuids returned"""
    
    check_output_channel()
    
    cmd = meta_list_players(uuids)
    
    status = post(cmd)
    
    # Remove all \x1b[.. color code from the status
    status = re.sub(r"\x1b\[[0-9;]*m", "", status)
    
    players = status.split("players online: ")[1].split(", ")
        
    return players

############# SPECTATE #############

def meta_spectate(target: str, player: str) -> str:
    return f"spectate {target} {player}"

def spectate(target: str, player: str) -> str:
    """Makes the target spectates a player"""
    
    check_output_channel()
    
    cmd = meta_spectate(target, player)
    
    status = post(cmd)
    
    return status
        
        
############# SET WORLD SPAWN #############

def meta_set_world_spawn(pos: Coordinates, yaw: int) -> str:
    return f"setworldspawn {pos} {yaw}"

def set_world_spawn(pos: Union[Coordinates, tuple], yaw: int = 0) -> str:
    """This function sets the world spawn"""
    
    check_output_channel()
    
    pos = format_arg(pos, Coordinates)

    cmd = meta_set_world_spawn(pos, yaw)
    
    status = post(cmd)
    
    return status