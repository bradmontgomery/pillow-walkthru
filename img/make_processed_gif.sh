#!/bin/bash

# Read in the processed images, write to a temp video file, then extract
# an animated gif.
ffmpeg -f image2 -i 'frames/me_processed%3d.png' -vcodec copy temp.mkv;
ffmpeg -i temp.mkv -pix_fmt rgb24 -loop 0 -r 5 me_processed.gif;
rm temp.mkv;
