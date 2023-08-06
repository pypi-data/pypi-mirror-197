from typing import Union
from shulker.functions.base_functions import *

############### BOSSBAR ###############

def meta_add_bossbar(id: str) -> str: 
  return f"bossbar add {id} {{\"text\":\"\"}}"

def meta_create_bossbar(id: str, text:str, target: str, value: int, color: str, progress: str, max: int, visible: bool) -> list:
    instructions = []
    
    instructions.append(f"bossbar set {id} value {value}")
    instructions.append(f"bossbar set {id} name {{\"text\":\"{text}\"}}")
    instructions.append(f"bossbar set {id} color {color}")
    instructions.append(f"bossbar set {id} players {target}")
    instructions.append(f"bossbar set {id} style {progress}")
    instructions.append(f"bossbar set {id} max {max}")
    instructions.append(f"bossbar set {id} visible {str(visible).lower()}")    
    
    return instructions

def meta_list_bossbar() -> str: 
  return "bossbar list"

def meta_remove_bossbar(id: str) -> str: 
  return f"bossbar remove {id}"

def meta_get_bossbar(id: str, option: str) -> str: 
  return f"bossbar get {id} {option}"

def meta_set_bossbar(id: str, option: str, value: str) -> str: 
  return f"bossbar set {id} {option} {value}"

def add_bossbar(id: str) -> str:
    """Adds a bossbar with the given id"""
    cmd = meta_add_bossbar(id)
    status = post(cmd)
    return status
 
def create_bossbar(
    id: str,
    text: str,
    target: Union[str, None] = "@a",
    value: int = 100,
    color: str = "white",
    style: str = "progress",
    max: int = 100,
    visible: bool = True,
) -> list:
    """
    Available colors: ["pink", "blue", "red", "green", "yellow", "purple", "white"]
    If target is None, it will only add the bossbar, but not display it to anyone.
    """

    check_output_channel()
    
    if target == None:
        target = ""
    
    cmd = meta_add_bossbar(id)
    cmd_2 = meta_create_bossbar(id, text, target, value, color, style, max, visible)

    status = post(cmd)
    
    status_2 = []
    for instruction in cmd_2:
      status_2.append(post(instruction))
    
    status_2.extend(status)
    
    return status

def list_bossbar() -> list:
    """Returns a list of all the bossbars"""
    check_output_channel()
    
    cmd = meta_list_bossbar()
    
    status = post(cmd)
        
    status = status[:-4]
    
    result = []
    bossbars = status.split(": ")[1].split(", ")
    for bossbar in bossbars:
        bossbar = bossbar.replace("[", "").replace("]", "")
        result.append(bossbar)
   
    return result

def remove_bossbar(id: str) -> str:
    """
    Removes the bossbar with the given id
    """
    
    check_output_channel()
    
    cmd = meta_remove_bossbar(id)
    
    status = post(cmd)
    
    return status

def get_bossbar(id: str, option: str) -> Union[list, int]:
    """
    Returns the values of the 'option' that was asked for, 
    of corresponding to the bossbar id.
    
    The 'players' options returns a list
    """

    check_output_channel()
    
    cmd = meta_get_bossbar(id, option)
    
    status = post(cmd)[:-4]
    
    if "players" in option:
        value = status.split(": ")[1].split(", ")
    else:
        value = status.split(" ")[-1]
        
    if "<--[HERE]" in value:
        raise ValueError(f"bossbar get cannot fetch {option}'s value")
    
    return value

def set_bossbar(id: str, option: str, value: str) -> str:
    """
    Sets the value of the bossbar with the given id
    Availables options: ["value", "max", "color", "style", "players", "name", "visible"]
    """

    check_output_channel()
    
    cmd = meta_set_bossbar(id, option, value)
    
    status = post(cmd)
        
    return status

############### TITLES ###############

def meta_show_gui(type: str, text: str, target: str) -> dict:
    return f"title {target} {type} {{\"text\":\"{text}\"}}"

def meta_clear_gui(target: str) -> dict:
    return f"title {target} clear"

def meta_set_gui_time(target: str, fade_in: int, stay: int, fade_out: int) -> dict:
    return f"title {target} times {fade_in} {stay} {fade_out}"

def show_gui(type: str, text: str, target: str = "@a") -> str:
    """
    Shows a title or a subtitle or an actionbar to the given target
    Available types: ["title", "subtitle", "actionbar"]
    """

    check_output_channel()
    
    cmd = meta_show_gui(type, text, target)
    
    status = post(cmd)
    
    return status

def clear_gui(target: str = "@a") -> str:
    """Clears the title, subtitle or actionbar for the target"""
    
    check_output_channel()
    
    cmd = meta_clear_gui(target)

    status = post(cmd)
    
    return status
        
def set_gui_time(target: str = "@a", fade_in: int = 10, stay: int = 70, fade_out: int = 20) -> str:
    """
    Sets the fade in, stay and fade out time of the title, subtitle or actionbar for the target
    Providing no values defaults to default time values
    """

    check_output_channel()
    
    cmd = meta_set_gui_time(target, fade_in, stay, fade_out)

    status = post(cmd)
    
    return status