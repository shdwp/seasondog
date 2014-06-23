import os
from seasondog import info
from seasondog import runtime as r

NAME = "plain"
VERSION = 1.0

DB = 1
TRANSACTION = 2
PATH = 3
PLAYER_ARGS = 4
EPISODE = 5

STRLEN = 512


def increment(a):
    return a + 1


def text(s, ln):
    if len(s) <= ln:
        return s + "".join([chr(0) for i in range(ln - len(s))])
    else:
        raise RuntimeError("Str value out of STRLEN!")


def db_struct(path, db={}, transaction={}):
    return {DB: db,
            TRANSACTION: transaction,
            PATH: path,
            }


def db_value(directory, episode, args):
    return text("{}:{}:{}".format(directory, episode, args), STRLEN)


def init(db):
    with open(db[PATH], 'w') as f:
        f.write(text("{}:{},{}:{}".format(info.NAME, info.VERSION, NAME, VERSION), STRLEN)+"\n")


def check(header):
    sdog, db = header.replace(chr(0), "").strip().split(",")
    name, version = db.strip().split(":")
    if name != NAME or float(version) > float(VERSION):
        raise RuntimeError("Unsupported database - adapter {}, {}; db {}, {}".format(NAME, VERSION, name, version))


def load(file):
    db = db_struct(file)

    dir = os.path.join(*os.path.split(file)[:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)

    if not os.path.exists(file):
        init(db)

    with open(file) as f:
        check(f.readline())

        line = f.readline()
        while line:
            directory, episode, player_args = line.strip().split(":")
            player_args = player_args.replace(chr(0), "")

            db[DB][directory] = {
                EPISODE: int(episode),
                PLAYER_ARGS: player_args,}

            line = f.readline()

    return db


def save(db):
    init(db)
    data = db[DB].copy()
    for k, v in db[TRANSACTION].items():
        data[k] = v

    with open(db[PATH], 'a') as f:
        for directory, option in data.items():
            f.write(db_value(directory, option[EPISODE], option[PLAYER_ARGS]) + "\n")


def commit(db):
    update = {}
    new = {}

    f = open(db[PATH], 'r')
    for k, v in db[TRANSACTION].items():
        if db[DB].get(k):
            pos = -1
            line = f.readline()
            while line and (pos < 0):
                directory, episode, player_args = line.strip().split(":")
                if directory == k:
                    pos = abs(pos) + 1

                pos -= 1
                line = f.readline()

            if pos >= 0:
                update[pos] = [k, v]
        else:
            new[k] = v

    f = open(db[PATH], 'r+b')
    f.seek(0)
    for i, [directory, data] in update.items():
        f.seek((i-1)*(STRLEN+1))
        f.write((db_value(directory, data[EPISODE], data[PLAYER_ARGS]) + "\n").encode("utf-8"))

    f = open(db[PATH], 'a')
    for directory, data in new.items():
        f.write(db_value(directory, data[EPISODE], data[PLAYER_ARGS]) + "\n")


def get(db, directory):
    return db[TRANSACTION].get(directory, db[DB].get(directory))


def set(db, directory, data):
    db[TRANSACTION][directory] = data
    return db


def unset(db, directory):
    del db[DB][directory]


def update(db, directory, fn, *args, **kwargs):
    return set(db, directory, fn(get(db, directory), *args, **kwargs))


def migrate(db, old_path, new_path):
    data = get(db, old_path)
    if not data:
        raise RuntimeError(r.format("{c_error}No record on {}!{endc}", old_path))

    set(db, new_path, data)
    unset(db, old_path)
    save(db)


def cleanup(db):
    counter = 0
    unset_directories = []
    for k, v in db[DB].items():
        if not os.path.exists(k):
            counter += 1
            unset_directories.append(k)

    for k in unset_directories:
        unset(db, k)

    if counter > 0:
        save(db)

    return counter
