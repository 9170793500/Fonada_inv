import os
import glob

# __all__ = [ "control", "user"]

# __all__=[os.path.basename(f)[:-3] for f in glob(os.path.dirname(__file__)+"*/.py")]


module_directory = os.path.dirname(__file__)


module_files = [f[:-3] for f in os.listdir(module_directory) if f.endswith('.py')]


__all__ = module_files