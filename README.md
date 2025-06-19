# oath-new-foundations-print-n-play
Tools for printing out Oath:NF assets on paper with ink

# Local environment setup
I used `uv` and `direnv`, rather than `pyenv`. At time of writing the notes are private to me in Anytype. 

# Setup `input` subdir

blah blah blah

# Run In This Dir

```
python denizen_combiner.py 
(
    cd wip || exit 1
    for f in denizens*.png ; do convert $f -rotate 90 rot-$f ; done
)
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o output/denizens.pdf wip/rot-denizens-*.png
python edifice_combiner.py
(
    cd wip || exit 1
    for f in edifices*.png ; do convert $f -rotate 90 rot-$f ; done
)
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o output/edifices.pdf wip/rot-edifices-*.png
python site_renamer.py
python tile.py 2 2 wip/site-\*.jpg wip/sites-\*.png
(
    cd wip || exit 1
    for f in sites-*.png ; do convert $f -rotate 90 rot-$f ; done
)
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o output/sites.pdf wip/rot-sites-*.png
```
