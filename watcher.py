import matcher
import os
import database as database
import runtime as r

MPLAYER = "mplayer -lavdopts threads=4 -fs \"{}\""
MPLAYER_SUB = "-sub {}"

def watch(runtime, data):
    episode = data[database.EPISODE]

    file = matcher.match(runtime[r.PATH], episode)
    if file:
        print("Episode #{}\n        {}\n[[enter] - watch, [^c] - break]".format(episode, file))
        try:
            input()
        except KeyboardInterrupt:
            return
        os.system(MPLAYER.format(file))
    else:
        print("Episode #{}\n        No episodes matched!".format(episode))

