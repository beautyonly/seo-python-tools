#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TO DO LIST
# 倒放的 gif 体积会大幅增加，暂时不知道如何解决

from PIL import Image,ImageSequence
import sys

def reverse_gif(gif_path,save_path="out.gif"):
    im = Image.open(gif_path)
    if im.is_animated:
        frames = [ f.copy() for f in ImageSequence.Iterator(im) ]
        frames.reverse()
        frames[0].save(save_path,save_all=True,append_images=frames[1:])
    else:
        raise TypeError('image is not animated')
        
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gif_path = sys.argv[1]
        try:
            save_path = sys.argv[2]
        except:
            reverse_gif(gif_path)
        else:
            reverse_gif(gif_path,save_path)
        finally:
            print("Done")
    else:
        print('Error : no gif_path or save_path ')