import os
import sys
import optparse
from seasondog import info
from seasondog import database as database
from seasondog import matcher as matcher
from seasondog import watcher
from seasondog import runtime as r
from optparse import OptionParser

def init_wizard(runtime, db):
    print(r.format("No record found on {c_path}{}{endc}.", runtime[r.PATH]))
    try:
        data = {database.EPISODE: 0,
                database.PLAYER_ARGS: input("Player args: "),
                }
    except KeyboardInterrupt:
        raise RuntimeError(r.format("{c_error}Cancelled.{endc}"))

    database.set(db, runtime[r.PATH], data)
    return data 

def opt_parser():
    parser = OptionParser(epilog="version {}, {}".format(info.VERSION, info.URL))
    parser.set_usage(
"""{} [action=next,prev,reset,status,set,args]
    n(ext) - watch next episode
    p(rev) - previous
    w(atch) - watch current episode
    set <EPISODE> - set progress
    args <ARGS> - set player args
    r(eset) - reset progress and settings for directory
        -f <PATH> - provide directory PATH instead of default .
    m(igrate) <DESTINATION> - migrate current directory to DESTINATION. 
        Directory name is preserved, only it's location is changed
        -f <PATH> - provide directory PATH instead of default .
        -p - don't preserve directory name, DESTINATION is full path to directory
    s(tatus) - show progress and settings\n""".format(info.NAME))
    parser.add_option("-a", "--player-args", help="Provide overriding player args")
    parser.add_option("-f", "--from", help="Provide from parameter for migration (instead of using current directory)")
    parser.add_option("-p", "--not-preserve", help="Don't preserve directory name", action="store_true")

    return parser

def arg(args, n):
    try:
        return args[n]
    except IndexError:
        raise RuntimeError(r.format("{c_error}Command requires at least {} argument(s)!{endc}", n))

def main():
    (opt, args) = opt_parser().parse_args()
    runtime = r.runtime_struct(os.path.abspath("."), opt)
    db = database.load(runtime[r.DB_PATH])

    action = len(args) > 0 and args[0] or "next"

    try:
        if action == "migrate" or action == "m":
            if opt.__dict__["from"]:
                old_path = os.path.abspath(opt.__dict__["from"])
                whatever, dir = os.path.split(old_path)
            else:
                whatever, dir = os.path.split(runtime[r.PATH])
                old_path = os.path.abspath(runtime[r.PATH])

            if opt.not_preserve:
                new_path = os.path.abspath(arg(args, 1))
            else:
                new_path = os.path.abspath(os.path.join(arg(args, 1), dir))

            try:
                input(r.format("New directory for {c_path}{}{endc} is {c_path}{}{endc}. Is this right?\n{c_control}[↵ watch, ^C break]{endc}", old_path, new_path))
                data = database.get(db, old_path)
                if not data:
                    raise RuntimeError(r.format("{c_error}No record on {}!{endc}", old_path))

                database.set(db, new_path, data)
                database.unset(db, old_path)
                database.save(db)
            except KeyboardInterrupt:
                pass

            return

        data = database.get(db, runtime[r.PATH])
        iswatch = True

        if action == "reset" or action == "r":
            path = opt.__dict__["from"] if opt.__dict__["from"] else runtime[r.PATH]
            try:
                database.unset(db, path)
            except KeyError:
                print(r.format("{c_error}There's no record at {c_path}{}{c_error} !{endc}", path))
            database.save(db)

            return

        elif action == "status" or action == "s":
            print(r.format(
                "{blue}{}{endc} v{}, database {} v{} ({grey}{}{endc})\nInternal path: {grey}{}{endc}",
                info.NAME,
                info.VERSION,
                database.NAME,
                database.VERSION,
                db[database.PATH],
                runtime[r.PATH],))

            if data:
                print(r.format("Current episode: {blue}{}{endc}\nPlayer args: {blue}{}{endc}",
                    data[database.EPISODE],
                    data[database.PLAYER_ARGS] or "None",))
            else:
                print(r.format("No data on {c_path}{}{endc}.", runtime[r.PATH]))

            return

        if not data:
            data = init_wizard(runtime, db)
        if action == "next" or action == "n":
            data[database.EPISODE] += 1
        elif action == "prev" or action == "p":
            data[database.EPISODE] -= 1
        elif action == "watch" or action == "w":
            pass
        elif action == "set":
            try:
                data[database.EPISODE] = int(arg(args, 1))
            except ValueError:
                raise RuntimeError(r.format("{c_error}{} is not a number!{endc}", arg(args, 1)))

        elif action == "args":
            data[database.PLAYER_ARGS] = arg(args, 1)
            iswatch = False

        database.set(db, runtime[r.PATH], data)
        database.save(db)

        if iswatch:
            watcher.watch(runtime, data)
    except RuntimeError as e:
        print(e)

