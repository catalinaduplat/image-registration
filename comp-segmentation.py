#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:35:43 2021

@author: duplacat
"""

import os
import SimpleITK as sitk
import sys


if len ( sys.argv ) < 3:
    print( "usage: {0} <originalImage> <registrationImage>".format(sys.argv[0]))
    sys.exit ( 1 )

OUTPUT_DIR = 'Segmentation/Output'
originalImage = sitk.ReadImage(sys.argv[1], sitk.sitkFloat32)
registrationImage = sitk.ReadImage(sys.argv[2], sitk.sitkFloat32)
checkerboard = sitk.CheckerBoard(originalImage, registrationImage, (20,20,20))
        
sitk.WriteImage(checkerboard, os.path.join(OUTPUT_DIR, "comp-segmentation.nii"))
