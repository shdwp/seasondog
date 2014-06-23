import os
import re
from seasondog import matcher
from seasondog import database as database
from seasondog import runtime as r
from seasondog import config

def player_args(runtime, data, string):
    for call in re.finditer(r"(\@(?P<fn>[a-zA-Z_]+)\((?P<args>[^@]*)\))", string):
        match = call.group(1)
        args = call.group("args").split(":")
        fn = call.group("fn")

        if fn == "subs":
            path = args[0] if len(args) > 0 else "."
            limit = int(args[1]) if len(args) > 1 else 1
            delim = args[2] if len(args) > 2 else " "

            files = matcher.match_subs(path, data[database.EPISODE], -1)
            if files:
                if limit != -1:
                    files = files[:limit]
                string = string.replace(match, "\"{}\"".format(delim.join(files)))
            else:
                print(r.format("{red}Warning: function {} matched nothing!{endc}", fn))
                string = string.replace(match, "")

        elif fn == "files":
            path = args[0] if len(args) > 0 else "."
            limit = int(args[1]) if len(args) > 1 else 1
            delim = args[2] if len(args) > 2 else " "

            files = matcher.match_file(path, data[database.EPISODE], -1)
            if files:
                if limit != -1:
                    files = files[:limit]
                string = string.replace(match, "\"{}\"".format(delim.join(files)))
            else:
                print(r.format("{red}Warning: function {} matched nothing!{endc}", fn))
                string = string.replace(match, "")

        elif fn == "var":
            vars = {"path": runtime[r.PATH],
                    "episode": data[database.EPISODE],
                    }

            string = string.replace(match, "\"{}\"".format(vars.get(args[0])))

    return string
        
def watch(runtime, data):
    episode = data[database.EPISODE]

    results = matcher.match_episode(runtime[r.PATH], episode)
    file = results[0] if results else None
    if file:
        if not runtime[r.PLAYER_ARGS_OVERRIDE]:
            args = player_args(runtime, data, data[database.PLAYER_ARGS])
        else:
            args = player_args(runtime, data, runtime[r.PLAYER_ARGS_OVERRIDE])

        print(r.format("{c_title}Episode {c_ep_number}{bold}#{episode}{endc}\n        {c_path}{path}\n        {c_args}{args}\n{endc}{c_control}[↵ watch, ^C break]{endc}", 
            episode=episode, 
            path=os.path.split(file)[-1],
            args=args if args else "",
            ))
        try:
            input()
        except KeyboardInterrupt:
            return
        
        os.system(config.PLAYER.format(player_args=args, videofile=file))
    else:
        print(r.format("{c_title}Episode {c_ep_number}{bold}#{episode}{endc}\n        {red}No episodes matched!{endc}", 
            episode=episode))

