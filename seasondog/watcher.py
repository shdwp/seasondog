import os
import re
from seasondog import matcher
from seasondog import database as database
from seasondog import runtime as r
from seasondog import config

def player_args(runtime, data, string):
    for call in re.finditer(r"(\@(?P<fn>[a-zA-Z_]+)\((?P<args>[^@]*)\))", string):
        match = call.group(1)
        args = call.group("args").split(" ")
        fn = call.group("fn")

        if fn == "subs":
            limit = int(args[1]) if len(args) > 1 else 1
            delim = args[2] if len(args) > 2 else " "

            files = matcher.match_subs(args[0], data[database.EPISODE], -1)
            if files:
                if limit != -1:
                    files = files[:limit]
                string = string.replace(match, "\"{}\"".format(delim.join(files)))
            else:
                string = string.replace(match, "")

        elif fn == "files":
            limit = int(args[1]) if len(args) > 1 else 1
            delim = args[2] if len(args) > 2 else " "

            files = matcher.match_file(args[0], data[database.EPISODE], -1)
            if files:
                if limit != -1:
                    files = files[:limit]
                string = string.replace(match, "\"{}\"".format(delim.join(files)))
            else:
                string = string.replace(match, "")

    return string
        
def watch(runtime, data):
    episode = data[database.EPISODE]

    file = matcher.match_episode(runtime[r.PATH], episode)[0]
    if file:
        if not runtime[r.PLAYER_ARGS_OVERRIDE]:
            args = player_args(runtime, data, data[database.PLAYER_ARGS])
        else:
                args = player_args(runtime, data, runtime[r.PLAYER_ARGS_OVERRIDE])

        print(r.format("{c_title}Episode {c_ep_number}{bold}#{episode}{endc}\n        {c_path}{path}\n        {c_args}{args}\n{endc}{c_control}[[enter] - watch, [^c] - break]{endc}", 
            episode=episode, 
            path=os.path.split(file)[-1],
            args=args,
            ))
        try:
            input()
        except KeyboardInterrupt:
            return
        
        os.system(config.PLAYER.format(player_args=args, videofile=file))
    else:
        print("Episode #{}\n        No episodes matched!".format(episode))

