import os

# Path to database file. You need to touch it by yourself
DB_PATH = os.path.join(os.path.expanduser("~"), ".seasondog", "database")

# Command to execute for playing videofile. 
PLAYER = "mplayer -lavdopts threads=4 -fs {player_args} \"{videofile}\""

# Extensions for lookuping subs
# from wiki
SUB_EXTENSIONS = ["srt", "ass", "aqt", "gsub", "sub", "ttxt", "pjs", "psb", "rt", "stl", "ssa", "usf", "idx",]

# Extensions for lookuping videofiles
# from .dir_colors
MOVIE_EXTENSIONS = ["mov","mpg","mpeg","m2v","mkv","webm","ogm","mp4","m4v","mp4v","vob","qt","nuv","wmv","asf","rm","rmvb","flc","avi","fli","flv","gl","dl","xcf","xwd","yuv","cgm","emf",]
