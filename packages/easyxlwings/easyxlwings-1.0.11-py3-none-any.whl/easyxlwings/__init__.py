# from pytz import VERSION
# import os
# from pathlib import Path
from .excel2json import excel2json

# from importlib.util import module_from_spec, spec_from_file_location

# setup_path = os.path.join(Path(__file__).parent.parent, "setup.py")

# spec = spec_from_file_location("constants", setup_path)
# constants = module_from_spec(spec)
# spec.loader.exec_module(constants)



# __name___ = constants.__name__
# __author__ = constants.__author__
# __version__ = constants.__author__
# __license__ = constants.__license__
# __url__ = constants.__url__



__all__ = [
    'excel2json',
    'utils'
]