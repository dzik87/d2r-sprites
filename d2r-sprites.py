# Diablo II: Resurrected .sprite python exporter
# based on information provided by shalzuth

import os
import glob
import sys
import struct
from PIL import Image
from bitstring import ConstBitStream

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
for f in glob.glob("./data/data/hd/**/*.sprite", recursive = True):
    with open(f, 'rb') as vfile:
        bytes = ConstBitStream(bytes = vfile.read())
        header = ""
        header = header + chr(int(bytes.read(8).hex, 16))
        header = header + chr(int(bytes.read(8).hex, 16))
        header = header + chr(int(bytes.read(8).hex, 16))
        header = header + chr(int(bytes.read(8).hex, 16))
                
        #print("0x00", header)                  # File header - always SpA1
        #print("0x04", bytes.read('uintle:16')) # version maybe ? 31 is different than 61 (61 do not want to be parsed here)
        #print("0x06", bytes.read('uintle:16')) # real frame width
        #print("0x08", bytes.read('uintle:32')) # overall width
        #print("0x0C", bytes.read('uintle:32')) # overall height
        #print("0x10", bytes.read('uintle:32')) # 0
        #print("0x14", bytes.read('uintle:32')) # number of frames
        #print("0x18", bytes.read('uintle:32')) # 0
        #print("0x1C", bytes.read('uintle:32')) # 0
        #print("0x20", bytes.read('uintle:32')) # streamsize
        #print("0x24", bytes.read('uintle:32')) # most of time 4
        
        # version
        bytes.pos = 0x04 * 8
        version = bytes.read('uintle:16')
        
        # image width
        bytes.pos = 0x08 * 8
        width = bytes.read('uintle:32')
        
        # image height
        bytes.pos = 0x0C * 8
        height = bytes.read('uintle:32')
        
        # number of frames
        bytes.pos = 0x14 * 8
        frames = bytes.read('uintle:32')
        frameoff = int(width / frames)
        
        # frame width
        bytes.pos = 0x06 * 8
        framew = bytes.read('uintle:16')
        
        # stream size
        bytes.pos = 0x20 * 8
        streamsize = bytes.read('uintle:32')
        
        # doesn't woth when version is 61
        if version == 31:
            for fram in range(frames):
                with Image.new("RGBA", (framew, height)) as im:
                    px = im.load()
                for y in range(height):
                    for x in range(framew):
                        xx = frameoff * fram + x
                        bytes.pos = (0x28 * 8) + (y * 4 * 8 * width) + (xx * 4 * 8)
                        px[x, y] = (bytes.read("uint:8"), bytes.read("uint:8"), bytes.read("uint:8"), bytes.read("uint:8"))

                sp = f.replace("data/data", "converted")
                ffn = "{}.{:02d}.{}".format(sp, fram, "png")
                ensure_dir(ffn)
                im.save(ffn, 'PNG')
        else:
            print("Skipping {} because version is not 31".format(f))