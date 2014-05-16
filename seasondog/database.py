import os
import copy
from seasondog import info

NAME = "plain"
VERSION = 0.1

DB = 1
TRANSACTION = 2
PATH = 3
PLAYER_ARGS = 4
EPISODE = 5 

STRLEN = 128

def increment(a):
    return a + 1

def text(s, ln):
    if len(s) <= ln:
        return s + "".join([chr(0) for i in range(ln - len(s))])
    else:
        raise RuntimeException("Str value out of STRLEN!")

def db_struct(path, db={}, transaction={}):
    return {DB: db,
            TRANSACTION: transaction,
            PATH: path,
            }

def db_value(directory, episode, args):
    return text("{}:{}:{}".format(directory, episode, args), STRLEN)

def init(file):
    with open(file, 'w') as f:
        f.write("{}:{},{}:{}\n".format(info.NAME, info.VERSION, NAME, VERSION))
    
    return db_struct(file)

def load(file):
    db = db_struct(file)

    dir = os.path.join(*os.path.split(file)[:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)

    if not os.path.exists(file):
        open(file, 'w').close()

    with open(file) as f:
        f.readline() # @TODO: header check
        line = f.readline()
        while line:
            directory, episode, player_args = line.strip().split(":")
            player_args = player_args.replace(chr(0), "")

            db[DB][directory] = {
                    EPISODE: int(episode),
                    PLAYER_ARGS: player_args,
                    }

            line = f.readline()

    return db

def save(db):
    init(db[PATH])
    data = db[DB].copy()
    for k, v in db[TRANSACTION].items():
        data[k] = v

    with open(db[PATH], 'a') as f:
        for directory, option in data.items():
            f.write(db_value(directory, option[EPISODE], option[PLAYER_ARGS]) + "\n")

def commit(db, file):
    map = {}
    
    index = 1
    with open(file) as f:
        f.readline() # @TODO: header check
        line = f.readline()
        while line:
            directory, episode = line.strip().split(":")
            if directory in db[TRANSACTION]:
                map[index] = [directory, db[TRANSACTION][directory]]
                db[DB][directory] = db[TRANSACTION][directory]
                del db[TRANSACTION][directory]
            index += 1
            line = f.readline()
    
    with open(file, 'a') as f:
        f.seek(0)
        for line, [directory, episode] in map.items():
            f.write(db_value(directory, episode) + "\n")


def get(db, directory):
    return db[TRANSACTION].get(directory, db[DB].get(directory))

def set(db, directory, data):
    db[TRANSACTION][directory] = data
    return db

def update(db, directory, fn, *args, **kwargs):
    return set(db, directory, fn(get(db, directory), *args, **kwargs))
