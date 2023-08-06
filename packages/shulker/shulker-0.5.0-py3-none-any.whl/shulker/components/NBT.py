from nbtlib import parse_nbt
from nbtlib import Byte, Short, Int, Long, Float, Double, String, ByteArray, IntArray, LongArray, List, Compound
from typing import Union

class NBT:
    def __init__(self, compound: Union[dict, str, Compound] = "{}"):
        
        if compound in [None, "", "{}", {}]:
            nbt = None
        elif type(compound) is Compound:
            nbt = compound
        elif type(compound) is dict:
            nbt = parse_nbt(str(compound))
        elif isinstance(compound, str):
            nbt = parse_nbt(compound)
        else:
            raise ValueError(f"Expected dict, str or Compound, got {type(compound)}")
        
        if nbt:
            for key in nbt:
                object.__setattr__(self, key, nbt[key])
            
    def flatten(self, arg):
        if type(arg) is Byte:
            return f'{int(arg)}b'
        elif type(arg) is Short:
            return f'{int(arg)}s'
        elif type(arg) is Int:
            return f'{int(arg)}'
        elif type(arg) is Long:
            return f'{int(arg)}L'
        elif type(arg) is Float:
            return f'{float(arg)}f'
        elif type(arg) is Double:
            return f'{float(arg)}d'
        elif type(arg) is String: # refer to test_NBT_with_args in test_NBT.py
            if '"' in arg:
                return f"'{str(arg)}'"
            else:
                return f'"{str(arg)}"'
        elif type(arg) is ByteArray:
            return f'[{",".join([int(str(int(x))) for x in arg])}]b'
        elif type(arg) is IntArray:
            return f'[{",".join([str(int(x)) for x in arg])}]'
        elif type(arg) is LongArray:
            return f'[{",".join([str(int(x)) for x in arg])}]L'
        elif isinstance(arg, List):
            return f'[{",".join([self.flatten(x) for x in arg])}]'
        elif type(arg) is Compound:
            if arg == {}:
                return "{}"
            return str(NBT(arg))

    def __setattr__(self, name, value):
        if isinstance(value, str):
          value = f'"{value}"'
          
        elif type(value) is list:
          new_value = "["
          for things in value:
            new_value += f"{things},"
          value = new_value[:-1] + "]"
          if value == "]":
            value = []

        if not isinstance(value, (List[Compound])):
          nbt = f"{{{name}:{value}}}"
          parsed_nbt = parse_nbt(nbt)
          super().__setattr__(name, parsed_nbt[name])
        else:
          super().__setattr__(name, value)
        
    def __str__(self):

        buff = ""

        for key in dir(self):
            if key.startswith("__"):
                continue
            elif key == "flatten":
                continue

            value = getattr(self, key)
            value = self.flatten(value)

            buff += f"{key}:{value},"

        if buff != "":
            buff = buff[:-1]
            return f"{{{buff}}}"
        else:
            return ""
