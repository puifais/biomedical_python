
# coding: utf-8

# # im_analysis_skeleton2.py
#
# This is written to serve as a skeleton for anyone who want to implement bioformats in Python2

# In[41]:

import Tkinter as Tk, tkFileDialog
import os, sys
import javabridge as jv
import bioformats as bf
import bioformats.omexml as ome
import matplotlib.pyplot as plt
import numpy as np
#from PIL import Image, ImagePath


# In[5]:

# debug
#get_ipython().system(u'python --version')
#get_ipython().system(u'which python')
#get_ipython().system(u'jupyter --version')
#get_ipython().system(u'which jupyter')


# ##### Start Java Virtual Machine.
# Note that if you try to do this in Python3, the Java Virtual Machine gives an error.
# Also, max_heap_size was set to be 3/4 of my computer's RAM

# In[6]:

jv.start_vm(class_path=bf.JARS, max_heap_size='12G')


# ##### User select image file to work with

# In[39]:

#hiding root alllows file diaglog GUI to be shown without any other GUI elements
root = Tk.Tk()
root.withdraw()
file_full_path = tkFileDialog.askopenfilename()
filepath, filename = os.path.split(file_full_path)
os.chdir(os.path.dirname(file_full_path))

print('opening:  %s' %filename)
im = bf.ImageReader(file_full_path)
md = bf.get_omexml_metadata(file_full_path)
o = ome.OMEXML()


# ##### Show image

# In[43]:

#implot = plt.imshow(im)


# ##### Show metadata

# In[46]:

print(o.image(0).AcquisitionDate)
print(o.image(0).Name)
print(o.image(0).Pixels)


# ##### Close Java Virtual Machine at the end

# In[6]:

jv.kill_vm()
