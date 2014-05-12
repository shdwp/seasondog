# seasondog

Small tool for saving your progress in watching series.

## Installation

Currently not published as pip package, but have no dependencies, so just link *\_\_init\_\_.py* into somewhere you have in $PATH.

## Configuration

First you need to edit *config.py*:

* *DB_PATH*: as default, database located in *~/.seasondog/database*, but you can change it with this variable
* *PLAYER*: you need to provide command line for starting your videoplayer. Two placeholders: videofile and player_args
* *SUB_EXTENSIONS* and *MOVIE_EXTENSIONS*: you can change or add file extensions for lookuping various files.

## Usage

On first call in directory you can provide player args for this directory, where you can setup various per-directory settings (for example - add subtitles). You can use command *@subs* in that string, its like function call:

    @subs(directory_to_lookup/ file_limit file_delimeter)

For mplayer this string should be `-sub @subs(subs/ -1 ,)`, that means - *find subtitles in directory sub/, with no limits, and separate all subtitles by symbol `,`*.

After you finish setup you can use such commands:

* `sdog` - watch next episode 
* `sdog prev` - watch prev episode
* `sdog watch` - watch current episode
* `sdog set <EPISODE>` - set episode directly and watch it
* `sdog reset` - reset progress and settings for directory
* `sdog status` - get current dir status information
* `sdog args <ARGS>` - set player args

And you can use option `-a` for one-time overriding player args. 

## License

Copyright © 2014 Vasiliy Horbachenko

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
