""" reorg4terastitcher.py by Puifai Santisakultarm 3/16/2017
    This script will rename and reorganize lightsheet microscopy files for use
    with TeraStitcher (http://abria.github.io/TeraStitcher/).

    Every computer comes with Python 2 and standard library and will be able to
    run this script.

    Input:  Tiff files from Zeiss Lightsheet microscope. Export your CZI file
    into TIFF files using ZEN blue export. The filenames will be filename_v#z###.tif

    Output:  Folders within folders, ready for TeraStitcher
"""

import Tkinter as Tk, tkFileDialog
import os, shutil, glob

# hiding root alllows file diaglog GUI to be shown without any other GUI elements
root = Tk.Tk()
root.withdraw()
original_dir = tkFileDialog.askdirectory() + '/'
# change current directory to where user selected
os.chdir(os.path.dirname(original_dir))

# ask user for image and tile information
print('regorg4terastitch.py is written to run on any computers, without having to install anything. That''s why it needs a little humanly help')
print(':)')
numRow = int(raw_input('Enter number of tile rows:  '))
numCol = int(raw_input('Enter number of tile columns:  '))
width_pix = int(raw_input('Enter each image width in pixels:  '))
height_pix = int(raw_input('Enter each image height in pixels:  '))
pixOverlap = int(raw_input('Enter number of pixels overlap:  '))
microns_per_pix = float(raw_input('Enter XY microns/pixel:  '))
numSlice = int(raw_input('Enter number of slices:  '))
z_move_microns = float(raw_input('Enter z-step in microns:  '))

# create a new directory structure
TeraStitcher_dir = os.path.dirname(original_dir) + '_TeraStitcher'
if os.path.exists(TeraStitcher_dir):
    shutil.rmtree(TeraStitcher_dir)
os.mkdir(TeraStitcher_dir)
os.chdir(TeraStitcher_dir)

stage_move_microns = (width_pix - pixOverlap) * microns_per_pix
rowFolder = 0

for row in range(numRow):
    os.mkdir(str(rowFolder).zfill(6))
    os.chdir(str(rowFolder).zfill(6))
    current_first_level_dir = os.getcwd()
    colFolder = 0
    for col in range(numCol):
        rowFolder_colFolder = str(rowFolder).zfill(6) + '_' + str(colFolder).zfill(6)
        os.mkdir(rowFolder_colFolder)
        colFolder = colFolder + int(round(z_move_microns,1)*10)
    rowFolder = rowFolder + int(round(stage_move_microns,1)*10)
    os.chdir(TeraStitcher_dir)
