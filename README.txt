# seasondog

Small tool for saving your progress in watching series.

## Installation

You can install seasondog trough pip:
    
    sudo pip install seasondog

## Configuration

First you need to edit copy default .sdogrc from repository to ~, and edit it:

* PLAYER: you need to provide command line for starting your videoplayer. Two placeholders: videofile and player_args

There is another configuration options, they're all documented in example .sdogrc

## Usage

On first call in directory you can provide player args for this directory, where you can setup various per-directory settings (for example - add subtitles). You can use specified functions for file matching in that string, which result substitutes into string.

For example, subtitles for mplayer should be 
    -sub @subs(subs/:-1:,)
, that means - find subtitles in directory sub/, with no limits, and separate all subtitles by symbol ','.

Available funtions:

    @files(path:file_limit:file_delimeter)
        lookup for files (matching uses similar algoritm, but without extension check) in path, limit results to file_limit (-1 for unlimited), join all results by file_delimeter.
        You can skip arguments, the defaults are: path - ., file_limit - (1), file_delimeter - (,).

    @subs(path:file_limit:file_delimeter)
        just like @files, but lookup only subtitles (check by extension).

After you finish setup you can use such commands:

* sdog - watch next episode 
* sdog p(rev) - watch prev episode
* sdog w(atch) - watch current episode
* sdog set <EPISODE> - set episode directly and watch it
* sdog r(eset) - delete current directory (or directory, provided by -f argument) from database
* sdog s(tatus) - get current dir status information
* sdog args <ARGS> - set player args in database
* sdog m(igrate) <DEST> - migrate current's directory status into DEST, with directory name preserved. You can disable preservation and provide full path using -p argument. Also, instead of using current directory you can provide it by yourself with -f <FROM> argument.
* sdog cleanup - remove not-existent directories from database


There is several global options also:
* -a ARGS - override player args
* --database=PATH - override default database location

## License

Copyright © 2014 Vasiliy Horbachenko

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
