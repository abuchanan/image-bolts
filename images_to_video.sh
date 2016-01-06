#!/bin/bash

ffmpeg -f image2 -pattern_type glob -i 'P*.JPG' test.mp4
