from .connect import RconClient as connect
from .ping import ping
from .create import DockerInstance as create
from .singleton import singleton

post = singleton.post