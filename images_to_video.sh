#!/bin/bash

ffmpeg -f image2 -pattern_type glob -i 'images/resized/*.jpg' output.mp4
