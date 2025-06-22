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
python retile.py 1358 1051 1 1 wip/site-\*.jpg 2 2 wip/sites-\*.png
(
    cd wip || exit 1
    for f in sites-*.png ; do convert $f -rotate 90 rot-$f ; done
)
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o output/sites.pdf wip/rot-sites-*.png
python retile.py 673 673 10 5 input/Relics\*.jpg 3 4 wip/relics-\*.png
img2pdf --pagesize letter --imgsize 6.75inx9in --fit shrink -o output/relics.pdf wip/relics-*png
python retile.py 827 1417 1 1 input/player-actions\*.jpg 2 2 wip/player-actions-\*.png
dm@pop-os:~/oath$ img2pdf --pagesize letter --imgsize 7.5inx10in --fit shrink -o output/player-actions.pdf wip/player-actions-00.png 
python retile.py 1181 1181 1 1 input/Banner\*.jpg 2 1 wip/banners-\*.png
img2pdf --pagesize letter --imgsize 6inx3in --fit shrink -o output/banners.pdf wip/banners-00.png
python retile.py 520 795 7 6 input/Foundation\ Trait\ Cards.jpg 4 4 wip/foundation-trait-cards-\*.png
img2pdf --pagesize letter --imgsize 7inx10in --fit shrink -o output/foundation-trait-cards.pdf wip/foundation-trait-cards-0*.png
python retile.py 827 1417 1 1 input/Player\ Aid\ \*.jpg 2 2 wip/player-aids-\*.png
img2pdf --pagesize letter --imgsize 5.25inx9in --fit shrink -o output/player-aids.pdf wip/player-aids-00.png 

img2pdf --pagesize letter --imgsize 7.25inx7in --fit shrink -o output/vision-cards.pdf input/Vision\ Cards.jpg 


```
