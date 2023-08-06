# mc-api
Use Python to control Minecraft through commands.

# Usage
Git clone then `sudo pip install -e .`

# How it works: 
Two things are available to the user: 
  - top level functions: designed for beginners and ease of use. 
    E.g.: ```set_block((0, 10, 0), 'dirt')``` will place a dirt block in x=0, y=10, z=0.
    
  - components: for a more advanced use in your programm, components let you declare and store attributes about an item. 
    E.g.: ```Block("dirt")``` will represent a dirt block. 
