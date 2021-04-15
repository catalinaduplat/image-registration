#!/usr/bin/env python

import os
import SimpleITK as sitk
import time

def run_registration(dtiFilename, t2Filename):
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
    
    
    fixed = sitk.ReadImage(dtiFilename, sitk.sitkFloat32)
    
    moving = sitk.ReadImage(t2Filename, sitk.sitkFloat32)
    
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
                                   scaleFactors=[1, 2, 7])
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
    
    sitk.WriteTransform(outTx, 'Output/BSpline.txt')
    
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
    sitk.WriteImage(cimg, 'Output/REGISTRATION-IMAGE.nii')
    
    with open(os.path.join('Output', 'results.txt'),"a+") as f:
        print("-------", file=f)
        print(outTx, file=f)
        print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}", file=f)
        print(f"Iteration: {R.GetOptimizerIteration()}", file=f)
        print(f"Metric value: {R.GetMetricValue()}", file=f)
        print(f"Time elapsed in seconds: {time.time() - start_time}", file=f)

    print(time.time() - start_time, "seconds")
    
    original_checkerboard = sitk.CheckerBoard(rescaled_img1, rescaled_img2, [4,4,4])
    transformed_checkerboard = sitk.CheckerBoard(simg1, simg2, (10,10,4))
    
    sitk.WriteImage(original_checkerboard, 'Output/check1.nii')
    sitk.WriteImage(transformed_checkerboard, 'Output/check2.nii')
    
