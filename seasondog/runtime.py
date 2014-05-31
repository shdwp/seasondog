from optparse import OptionParser
from seasondog import config

PATH = 1
DB_PATH = 2
PLAYER_ARGS_OVERRIDE = 3

def runtime_struct(path, opt):
    return {PATH: path,
            DB_PATH: config.DB_PATH,
            PLAYER_ARGS_OVERRIDE: opt.player_args,
            }

def format(s, *args, **kwargs):
    kwargs.update(config.COLORS)
    return s.format(*args, **kwargs)
