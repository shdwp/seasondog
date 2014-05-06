from optparse import OptionParser

PATH = 1
DB_PATH = 2
PLAYER_ARGS_OVERRIDE = 3

def runtime_struct(path, opt):
    return {PATH: path,
            DB_PATH: "/home/sp/.seriedog/database",
            PLAYER_ARGS_OVERRIDE: opt.player_args,
            }

