# Oath Fan Made Print and Play

This converts Tabletop Simulator (TTS) cache files into printable PDFs.

At time of writing Oath New Foundations is not widely available, but the design has been fixed for some time.
We're able to play in Tabletop Simulator (TTS) now, but what about playing over the board?

If you just want to print the finished PDFs, go to this [fileshare](https://drive.proton.me/urls/WA9T4HZKA4#Kk7TvAFDGP46). 
Otherwise read on to learn how those files were made.

This repo contains a script - `namer.py` that copies TTS cached images into this repo's `input` folder,
giving the files more readable names. It assumes you've loaded up TTS with the Buried Giant Oath New Foundations game. Some of the content is lazily loaded, so you'll need to open all the Clockwork bags in TTS to get it to cache those files locally.

Then this repo contains another script - `oath.py` - that chops up those assets into 8.5x11" pages. You can print them out and 
play New Foundations today. It takes a ton of flags, pass it `--help` for a list.

# Local environment setup
I used `uv` and `direnv`, rather than `pyenv`. I forget exactly how you, a new user, should use it, 
but I did take notes (to myself) on what I did in `Start a Python Project` in Anytype.


# Physical World Assumptions

- You own base Oath, sleeved it, and own a working printer and a pair of scissors for cutting up cards. 
- You don't want to print out the stuff from base game you already have (exception: you can print the base game denizens).
- Since the cardlist is growing, you'll need some extra cardboard backs for the new cards - I used old Netrunner cards and sleeves, even though they were a bit too big. For the relics, I ordered "Wyrmspan" sized sleeves and cut up some cardstock to give them some backbone. For sites I just left them unsleeved. 

- You're on a unix-like system with imagemagick installed. Linux, for example. Or MacOS with brew. Or maybe, just maybe, Windows with WSL, but no I don't want to fix the headaches that come from supporting Windows.
