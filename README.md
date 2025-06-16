# oath-new-foundations-print-n-play
Tools for printing out Oath:NF assets on paper with ink

# Local environment setup
I used `uv` and `direnv`, rather than `pyenv`. At time of writing the notes are private to me in Anytype. 

# Setup `oath-res` dir

blah blah blah

# Run This

```
python red-triangle-filter.py 
for f in denizens*.png ; do convert $f -rotate 90 rot-$f ; done
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o denizens.pdf rot-denizens-*.png
for f in edifices*.png ; do convert $f -rotate 90 rot-$f ; done
img2pdf --pagesize letter --imgsize 7inx9in --fit shrink -o edifices.pdf rot-edifices-*.png
```
