
# coding: utf-8

# # reorg4terastitcher.py
# 
# by Puifai Santisakultarm 3/16/2017
# 
# This script will rename and reorganize lightsheet microscopy files for use with TeraStitcher (http://abria.github.io/TeraStitcher/).
# 
# Input:  tiff files from Zeiss Lightsheet microscope. This script assume the "backward S" scanning pattern. Export your CZI file into TIFF files using ZEN blue export. The filenames will be filename_v#z#.tif. The number of digits after the character 'v' can vary. No problemo.
# 
# Output:  Folders within folders with appropriate files moved and renamed, ready for TeraStitcher. The first level of folders represent rows of tiles. The next level down represents columns of tiles.
# 
# Requirement:  Python 2.7. No installation of any libraries needed. The rationale is that every computer comes with Python 2 and standard library and will be able to run this script. So, say I leave the Salk's Biophotonics Core and we get new computer/update old ones, users can still run this script without Puifai's help...

# In[1]:

import Tkinter as Tk, tkFileDialog
import os, shutil, glob
import timeit


# In[2]:

# hiding root alllows file diaglog GUI to be shown without any other GUI elements
root = Tk.Tk()
root.withdraw()
root.call('wm','attributes','.','-topmost',True)
original_dir = tkFileDialog.askdirectory() + '/'
# change current directory to where user selected
os.chdir(os.path.dirname(original_dir))


# In[3]:

# ask user for image and tile information
print('regorg4terastitch.py is designed to run on any computers, without having to install anything.')
print('Therefore, it needs a little humanly help :)')
print('')
numCol = int(raw_input('Enter number of horizontal tiles:  '))
numRow = int(raw_input('Enter number of vertical tiles:  '))
numSlice = int(raw_input('Enter number of slices:  '))
microns_per_pix = float(raw_input('Enter XY microns/pixel:  '))
z_move_microns = float(raw_input('Enter z-step in microns:  '))
width_pix = int(raw_input('Enter each image width in pixels:  '))
height_pix = int(raw_input('Enter each image height in pixels:  '))
pixOverlap = int(raw_input('Enter number of pixels overlap:  '))
print('')


# In[4]:

# assume "backward S" scanning pattern, create tile orientation map
tileOrientation = range(1,numRow * numCol + 1)
for row in range(numRow):
    if row % 2 == 1: # only reverse tile orientation if in odd row. Remember row starts from 0 not 1
        tileOrientation[row * numCol:row * numCol + numCol] = tileOrientation[row * numCol + numCol - 1:row * numCol -1:-1]
tileNumDigit = len(str(numRow * numCol))

#print('tileNumDigit = %s' %tileNumDigit)
#print('tileOrientation = %s' %tileOrientation)


# In[5]:

def copy_and_rename_files_in_tile4terastitcher(tileNum,tileNumDigit,original_dir,folder_to_move_to,z_move_microns):
    '''
    This function moves all the files in each tile into appropriate TeraStitcher
    folders and rename them according to their depth in z
    '''
    os.chdir(original_dir)
    search_word = ('*_v' + str(tileNum).zfill(tileNumDigit) + '*.tif*')
    files_in_tile = glob.glob(search_word)
    new_filename = 0
    numFileReorg = 0
    
    for file in files_in_tile:
        original_filefullpath = os.path.join(original_dir,file)
        new_filefullpath = os.path.join(folder_to_move_to,str(new_filename).zfill(6) +'.tif')
        #print('original_filefullpath = %s' %original_filefullpath)
        #print('new_filefullpath = %s' %new_filefullpath)
        #print('')
        print('working on:  %s' %file)
        shutil.copyfile(original_filefullpath,new_filefullpath)
        numFileReorg += 1
        new_filename = new_filename + int(round(z_move_microns,1)*10)
        
    return numFileReorg


# In[6]:

# create a new directory structure
TeraStitcher_dir = os.path.dirname(original_dir) + '_TeraStitcher'
if os.path.exists(TeraStitcher_dir): # if this folder already exists, remove it
    shutil.rmtree(TeraStitcher_dir)
os.mkdir(TeraStitcher_dir)
os.chdir(TeraStitcher_dir)

stage_move_microns = (width_pix - pixOverlap) * microns_per_pix # assume overlap in x and y are the same
rowFolder = 0
i = 0
totalNumFileReorg = 0


# In[7]:

tic = timeit.default_time() #timing how long it takes to finish processing files
for row in range(numRow):
    os.mkdir(str(rowFolder).zfill(6))
    os.chdir(str(rowFolder).zfill(6))
    current_first_level_dir = os.getcwd()
    #print('')
    #print('current_first_level_dir = %s'%current_first_level_dir)

    colFolder = 0
    for col in range(numCol):
        rowFolder_colFolder = str(rowFolder).zfill(6) + '_' + str(colFolder).zfill(6)
        os.mkdir(rowFolder_colFolder)
        # move appropriate files and rename them
        dir_for_creating_folder = os.getcwd()
        folder_to_move_to = os.path.join(os.getcwd(),rowFolder_colFolder)
        
        numFileReorg = copy_and_rename_files_in_tile4terastitcher(tileOrientation[i],tileNumDigit,original_dir,folder_to_move_to,z_move_microns)
        totalNumFileReorg += numFileReorg
        i += 1
        os.chdir(dir_for_creating_folder)
        # continue making folder hierachy
        colFolder = colFolder + int(round(stage_move_microns,1)*10)
    rowFolder = rowFolder + int(round(stage_move_microns,1)*10)
    os.chdir(TeraStitcher_dir)

toc = timeit.default_timer()
timelapse = toc - tic
print('')
print('%s files were reorganized in %s s' %(totalNumFileReorg, timelapse)


# In[8]:

raw_input('Press Enter to close this window...')


# In[ ]:



