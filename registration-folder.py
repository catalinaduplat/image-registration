#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:35:43 2021

@author: duplacat
"""

import os
import SimpleITK as sitk
import time
import sys
import re

DTI_filename = ''
T2_filename = ''
OUTPUT_DIR = 'Output'

if len ( sys.argv ) < 4:
    print( "usage: {0} <rootDir> <fixedImageType> <movingImageType>".format(sys.argv[0]))
    sys.exit ( 1 )

for subdir, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if re.search(sys.argv[2], file, re.IGNORECASE):
            DTI_filename = os.path.join(subdir, file)
        if re.search(sys.argv[3], file, re.IGNORECASE):
            T2_filename = os.path.join(subdir, file)
    subdir_basename = os.path.basename(os.path.normpath(subdir))
    
    if DTI_filename and T2_filename:
        start_time = time.time()
        def command_iteration(method, bspline_transform):
            if method.GetOptimizerIteration() == 0:
                # The BSpline is resized before the first optimizer
                # iteration is completed per level. Print the transform object
                # to show the adapted BSpline transform.
                print(bspline_transform)
        
            print(f"{method.GetOptimizerIteration():3} = {method.GetMetricValue():10.5f}")
        
        
        def command_multi_iteration(method):
            # The sitkMultiResolutionIterationEvent occurs before the
            # resolution of the transform. This event is used here to print
            # the status of the optimizer from the previous registration level.
            if R.GetCurrentLevel() > 0:
                print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
                print(f" Iteration: {R.GetOptimizerIteration()}")
                print(f" Metric value: {R.GetMetricValue()}")
        
            print("--------- Resolution Changing ---------")
        
        
        fixed = sitk.ReadImage(DTI_filename, sitk.sitkFloat32)
        
        moving = sitk.ReadImage(T2_filename, sitk.sitkFloat32)
        
        transformDomainMeshSize = [2] * fixed.GetDimension()
        
        tx = sitk.BSplineTransformInitializer(fixed,
                                              transformDomainMeshSize)
        
        print(f"Initial Number of Parameters: {tx.GetNumberOfParameters()}")
        
        R = sitk.ImageRegistrationMethod()
        R.SetMetricAsMattesMutualInformation(numberOfHistogramBins=32)
        R.SetMetricSamplingStrategy(R.RANDOM)
        R.SetMetricSamplingPercentage(0.1)
        
        R.SetOptimizerAsGradientDescentLineSearch(5.0,
                                                  100,
                                                  convergenceMinimumValue=1e-4,
                                                  convergenceWindowSize=5)
        
        R.SetInterpolator(sitk.sitkLinear)
        
        R.SetInitialTransformAsBSpline(tx,
                                        inPlace=True,
                                        scaleFactors=[1, 2, 8])
        R.SetShrinkFactorsPerLevel([4, 2, 1])
        R.SetSmoothingSigmasPerLevel([4, 2, 1])
        
        R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R, tx))
        R.AddCommand(sitk.sitkMultiResolutionIterationEvent,
                      lambda: command_multi_iteration(R))
        
        outTx = R.Execute(fixed, moving)
        
        print("-------")
        print(tx)
        print(outTx)
        print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
        print(f" Iteration: {R.GetOptimizerIteration()}")
        print(f" Metric value: {R.GetMetricValue()}")
        
        f = open(os.path.join(OUTPUT_DIR, subdir_basename+'-results.txt'),"a+")
        f.write(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
        f.write(f"Iteration: {R.GetOptimizerIteration()}")
        f.write(f"Metric value: {R.GetMetricValue()}")
        
        sitk.WriteTransform(tx, os.path.join(OUTPUT_DIR, subdir_basename+'-BSplineImportant.txt'))
        sitk.WriteTransform(outTx, os.path.join(OUTPUT_DIR, subdir_basename+'-BSpline.txt'))
        
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(100)
        resampler.SetTransform(outTx)
    
        out = resampler.Execute(moving)
        rescaled_img1 = sitk.RescaleIntensity(fixed)
        rescaled_img2 = sitk.RescaleIntensity(out)
        simg1 = sitk.Cast(rescaled_img1, sitk.sitkUInt8)
        simg2 = sitk.Cast(rescaled_img2, sitk.sitkUInt8)
        cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
        sitk.WriteImage(cimg, os.path.join(OUTPUT_DIR, subdir_basename+"-RESULT-IMAGE.mha"))
        
        print(time.time() - start_time, "seconds")
        
        f.write(f"Time elapsed in seconds: {time.time() - start_time}")
        
        original_checkerboard = sitk.CheckerBoard(rescaled_img1, rescaled_img2, [4,4,4])
        transformed_checkerboard = sitk.CheckerBoard(simg1, simg2, (10,10,4))
        
        sitk.WriteImage(original_checkerboard, os.path.join(OUTPUT_DIR, subdir_basename+"-CHECKERBOARD1.mha"))
        sitk.WriteImage(transformed_checkerboard, os.path.join(OUTPUT_DIR, subdir_basename+"-CHECKERBOARD2.mha"))