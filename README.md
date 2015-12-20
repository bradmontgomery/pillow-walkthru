Pillow Walkthrough Tutorial
===========================

This is a brief walkthrough of [Pillow](https://python-pillow.github.io/), the
python library for image processing. This repo is just a collection of resources
for a short talk taking place on Dec 21, 2015 at the [MEMpy meetup](http://mempy.org)


Background &amp; agenda
-----------------------

- A little history
- What is PIL anyway?
- Pillow installation (hint: `pip install pillow`)
- Usage / Demo
- Animated GIFs with ffmpeg


Required libraries
------------------

See the `requirements.txt` file for python things, namely:

- pillow
- ipython
- matplotlib

For this to be worthwhile, you'll need the following additional libraries (so
Pillow can load images). See [the pillow docs](http://pillow.readthedocs.org/en/3.0.x/installation.html#external-libraries) for descriptions of each.

- libjpeg
- zlib
- libtiff
- libfreetype
- littlecms
- libwebp
- tcl/tk
- openjpeg

On OS X I get these with: `brew install libtiff libjpeg webp little-cms2`


Image/Video Resources
---------------------

See the `img` directory in this repo. It should contain:

- a few sample images that we'll play with: `cake.jgp`, `coffee.jpg`, `texture.jpg`
- a short video file, `me.mov`
- some bash scripts to make working with ffmpe easier:
  - `extract.sh` - extract frames from a video file
  - `make_me_gif.sh` - make an animated gif from the extracted frames
  - `make_processed_gif.sh` - make an animated gif from processed frames


Animated gifs with ffmpeg
-------------------------

Given an input file `me.mov`, export it's frames to .png files in an `out` dir.
Note the scale (1080) is the width of the original movie.

    ffmpeg -i me.mov -vf scale=1080:-1 -r 10 out/me%3d.png


Now, do something with those images. Then, we'll take that collection and
re-create an intermediary video:

    ffmpeg -f image2 -i 'out/me%3d.png' -vcodec copy video.mkv;

from which we can make an animated gif:

    ffmpeg -i video.mkv -pix_fmt rgb24 -loop 0 -r 5 out.gif

All of this assumes you have ffmpeg and the appropriate libs. See this [resource](https://gist.github.com/tskaggs/6394639).
