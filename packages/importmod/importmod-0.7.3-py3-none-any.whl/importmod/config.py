import configparser
import os
import typing

from portmod.globals import env

path = os.path.join(env.CONFIG_DIR, "importmod.cfg")
try:
    config = configparser.ConfigParser()
    config.read(path)
    NEXUS_KEY: typing.Optional[str] = config["importmod"]["NEXUS_KEY"]
except KeyError:
    print(
        f"NEXUS_KEY not configured, looking for key NEXUS_KEY under importmod in %{path}"
    )
    NEXUS_KEY = None
