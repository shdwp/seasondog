#!/usr/bin/env python
import os
import sys
import info
import database as database
import matcher as matcher
import watcher
import runtime as r
from optparse import OptionParser

def init_wizard(runtime, db):
    print("No record found on {}".format(runtime[r.PATH]))
    data = {database.EPISODE: 1,
            database.PLAYER_ARGS: input("Player args > "),
            }
    database.set(db, runtime[r.PATH], data)
    return data

if __name__ == "__main__":
    parser = OptionParser(epilog="version {}, {}".format(info.VERSION, info.URL))
    parser.set_usage(
"""{} [action=next,prev,reset,status,set,args]
    next - watch next episode
    prev - previous
    watch - watch current episode
    set <EPISODE> - set progress
    args <ARGS> - set player args
    reset - reset progress and settings for directory
    status - show progress and settings
""".format(info.NAME))
    parser.add_option("-a", "--player-args", help="Provide overriding player args")
    (opt, args) = parser.parse_args()

    runtime = r.runtime_struct(os.path.abspath("."), opt)
    
    db = database.load(runtime[r.DB_PATH])

    action = len(args) > 0 and args[0] or "next"
    data = database.get(db, runtime[r.PATH])
    iswatch = True

    if not data or action == "reset":
        data = init_wizard(runtime, db)

    if action == "next":
        data[database.EPISODE] += 1
    elif action == "prev":
        data[database.EPISODE] -= 1
    elif action == "watch":
        pass
    elif action == "set":
        data[database.EPISODE] = args[1]
    elif action == "args":
        data[database.PLAYER_ARGS] = args[1]
        iswatch = False
    elif action == "status":
        print("{} v{}, database {} v{} ({})\nInternal path: {}\nCurrent episode: {}\nPlayer args: {}".format(
            info.NAME,
            info.VERSION,
            database.NAME,
            database.VERSION,
            db[database.PATH],
            runtime[r.PATH],
            data[database.EPISODE],
            data[database.PLAYER_ARGS],))
        iswatch = False

    database.set(db, runtime[r.PATH], data)
    database.save(db)

    if iswatch:
        watcher.watch(runtime, data)

