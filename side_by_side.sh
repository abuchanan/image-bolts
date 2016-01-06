ffmpeg -i test.mp4 -vf "[in] scale=iw/2:ih/2, pad=2*iw:ih [left]; 
    movie=test-corrected.mp4, scale=iw/2:ih/2 [right]; 
    [left][right] overlay=main_w/2:0 [out]" -b:v 768k test_compare.mp4
