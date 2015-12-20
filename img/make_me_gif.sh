#!/bin/bash


# Read in original extracted images, write to a temp video file, then extract
# an animated gif.
ffmpeg -f image2 -i 'frames/me%3d.png' -vcodec copy temp.mkv;
ffmpeg -i temp.mkv -pix_fmt rgb24 -loop 0 -r 5 me.gif;
rm temp.mkv;
