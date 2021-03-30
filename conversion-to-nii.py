#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 12:43:43 2021

@author: duplacat
"""

import os
import SimpleITK as sitk
import sys
import re

# nii_path = root_path + '/data.nii'
# mha_path = root_path + '/data.mha'

# img = sitk.ReadImage(nii_path)
# sitk.WriteImage(img, mha_path)

if len ( sys.argv ) < 2:
    print( "usage: {0} <rootDir>".format(sys.argv[0]))
    sys.exit ( 1 )

for subdir, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if re.search("mha", file, re.IGNORECASE):
            MHA_FILENAME = os.path.join(subdir, file)
            NII_FILENAME = MHA_FILENAME .split('.')[0] + '.nii'
            img = sitk.ReadImage(MHA_FILENAME)
            sitk.WriteImage(img, NII_FILENAME)