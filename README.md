# oath-new-foundations-print-n-play
## the tool to playing Oath New Foundations over the board in 2025
Tools for printing out Oath:NF assets on paper with ink.
At time of writing Oath New Foundations is the better part of a year away, but the game design is wrapping up. 
We'll be able to play in TTS early, but what about playing Over the Board?

Discord user DomV rips the digital assets from TTS and puts them in a google drive doc for reference. 
They're not easy to print out though, because, for example, the denizen cards are on a huge 6x5 grid - unless
you have a poster printer, that's pretty awkward. 

This repo contains tooling for chopping up those assets into 8.5x11" pages. You can print them out and 
play New Foundations today. 

# Local environment setup
I used `uv` and `direnv`, rather than `pyenv`. I forget exactly how you, a new user, should use it, 
but I did take notes (to myself) on what I did in `Start a Python Project` in Anytype. 

# Setup `input` subdir

Download DomV's assets to the input/ directory. So for example `<root>/input/Visions.jpg` should be a thing. 
And a lot of other jpegs besides that.

Note that the easiest way to d/l them all is to `cd ..` and then right-click the folder in Google Drive. 
Download the zip and then do a little splicing. 

## Update: now building my own `input` subdir
Well actually now I'm copying the images directly out of TTS in a format that's mostly the same as DomV's. 
This script is in namer.py. You could theoretically do this too. 

# Assumptions

- You own base Oath, sleeved it, and own a working printer and a pair of scissors for cutting up cards. 
- You don't want to print out the crab you already have. 
- Since the cardlist is growing, you'll need some extra cardboard backs for the new cards - I used Netrunner. 
- You're on a unix-like system with imagemagick installed. Linux, for example. Or MacOS with brew. Or maybe, just maybe, Windows with WSL, but no I don't want to fix the headaches that come from supporting Windows. Fix your own CRLF errors or whatever. As a wise man once said: "here's a nickel kid, buy yourself a real operating system."

# Rip it!!
```
python oath.py --all
```
See also:
```
python oath.py --help
```

# A request

Hey it's your pal: humanity. I don't know if you noticed, but we're in a real scrap here. We're endangering ourselves with massive carbon emissions. So if you want to tip me for my time making this tool, please go somewhere you were going to go before, but use your body's power instead of a car. Walk to that post office. Bike to the grocery. Go see if your friend is home. Get out and get moving. Let the dinosaur juice lay in the ground - those guys had a really hard day. 

Hey by the way, do you wanna buy my Netrunner cards? They're cheap. 
