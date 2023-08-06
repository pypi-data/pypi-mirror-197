import json

def print_registries():
    registries = get_registries()
        
    for key in registries.keys():
        print("--->", key.replace("minecraft:", ""))

def get_registries():
    with open('../functions/mc_data/registries.json') as f:
        registries = json.load(f)
        
    return registries

def get_registry_keys(registry: str):
    registries = get_registries()
    
    if not registry.startswith("minecraft:"):
        registry = "minecraft:" + registry
        
    return registries[registry]

def print_registry_keys(registry: str):
    keys = get_registry_keys(registry)
    
    for key in keys:
        print("--->", key.replace("minecraft:", ""))
        
def get_commands():
    with open('../functions/mc_data/commands.json') as f:
        commands = json.load(f)
    return commands

def print_commands():
    commands = get_commands()     
    for command in commands["children"]:
        print("--->", command)

computed_commands = ["title", "bossbar", "setblock", "fill", "summon", "say",
                     "ban", "ban-ip", "banlist", "kick", "op", "deop", "seed",
                     "difficulty", "weather", "msg", "gamemode", "time", "w", 
                     "tell", "xp", "experience", "whitelist", "stop", "reload",
                     "save-all", "save-off", "save-on", "help", "list", "pardon", 
                     "pardon-ip", "setworldspawn"]
excluded_commands = ["advancement", "perf", "me", "defaultgamemode", "jfr", 
                     "debug", "spectate", "trigger", "tm", "teammsg"]
complex_commands = ["worldborder", "execute", "tp", "particle", "gamerule", 
                    "loot", "playsound", "team"]

def print_todo_commands():
    commands = get_commands()     
    for command in commands["children"]:
        if command not in computed_commands and command not in excluded_commands and command not in complex_commands:
            print("--->", command)
            
def print_done_commands():
    for command in computed_commands:
        print("--->", command)
        
def print_excluded_commands():
    for command in excluded_commands:
        print("--->", command)
        
def print_complex_commands():
    for command in complex_commands:
        print("--->", command)

def print_commands_summary():
    print("Done:")
    print_done_commands()
    print()
    print("Todo:")
    print_todo_commands()
    print()
    print("Complex:")
    print_complex_commands()
    print()
    print("Excluded:")
    print_excluded_commands()
         
print_commands_summary()