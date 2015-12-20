#!/bin/bash

# Extract frames from a video file (me.mov) into an output folder.
if [ ! -d frames ]; then
    mkdir frames;
fi
ffmpeg -i me.mov -vf scale=1080:-1 -r 10 frames/me%3d.png
