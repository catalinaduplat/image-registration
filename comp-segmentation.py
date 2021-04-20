#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:35:43 2021

@author: duplacat
"""

import os
import SimpleITK as sitk
import sys


if len ( sys.argv ) < 6:
    print( "usage: {0} <fixedImage> <registrationImage> <seedX> <seedY> <seedZ>".format(sys.argv[0]))
    sys.exit ( 1 )

OUTPUT_DIR = 'OutputSegmentation'
original_image = sitk.ReadImage(sys.argv[1], sitk.sitkFloat32)
registration_image = sitk.ReadImage(sys.argv[2], sitk.sitkFloat32)

original_255 = sitk.Cast(sitk.RescaleIntensity(original_image), sitk.sitkUInt8)
registration_255 = sitk.Cast(sitk.RescaleIntensity(registration_image), sitk.sitkUInt8)

seed_x = int(sys.argv[3])
seed_y = int(sys.argv[4])
seed_z = int(sys.argv[5])
seed = (seed_x,seed_y,seed_z)

pink= [255,105,180]
red = [128, 19, 73]

def run_segmentation(image, res_image, multiplier, color, filename):
    seg = sitk.Image(image.GetSize(), sitk.sitkUInt8)
    seg.CopyInformation(image)
    seg[seed] = 1
    seg = sitk.BinaryDilate(seg, [3]*seg.GetDimension())
    
    stats = sitk.LabelStatisticsImageFilter()
    stats.Execute(image, seg)
    
    factor = multiplier
    lower_threshold = stats.GetMean(1)-factor*stats.GetSigma(1)
    upper_threshold = stats.GetMean(1)+factor*stats.GetSigma(1)
    print(lower_threshold,upper_threshold)
    
    init_ls = sitk.SignedMaurerDistanceMap(seg, insideIsPositive=True, useImageSpacing=True)
    
    lsFilter = sitk.ThresholdSegmentationLevelSetImageFilter()
    lsFilter.SetLowerThreshold(lower_threshold)
    lsFilter.SetUpperThreshold(upper_threshold)
    lsFilter.SetMaximumRMSError(0.02)
    lsFilter.SetNumberOfIterations(1000)
    lsFilter.SetCurvatureScaling(.5)
    lsFilter.SetPropagationScaling(1)
    lsFilter.ReverseExpansionDirectionOn()
    ls = lsFilter.Execute(init_ls, sitk.Cast(image, sitk.sitkFloat32))
    print(lsFilter)
    
    segmented_image = sitk.LabelOverlay(res_image, ls>0, colormap=color)
    sitk.WriteImage(segmented_image, os.path.join(OUTPUT_DIR, filename+".nii"))
    return segmented_image


original_seg = run_segmentation(original_image, original_255, 1, pink, "fixed-img-segmented")
registration_seg = run_segmentation(registration_image, registration_255, 1.5, red, "registration-img-segmented")

checkerboard = sitk.CheckerBoard(original_seg, registration_seg, (20,20,20))     
sitk.WriteImage(checkerboard, os.path.join(OUTPUT_DIR, "comp-segmentation.nii"))
