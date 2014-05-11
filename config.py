import os

# Path to database file. You need to touch it by yourself
DB_PATH = os.path.join(os.path.expanduser("~"), ".seasondog", "database")

# Command to execute for playing videofile. 
PLAYER = "mplayer -lavdopts threads=4 -fs {player_args} \"{videofile}\""

# Extensions for lookuping subs
SUB_EXTENSIONS = ["srt", "ass"]

# Extensions for lookuping videofiles
MOVIE_EXTENSIONS = ["avi", "mkv", "mp4"]
