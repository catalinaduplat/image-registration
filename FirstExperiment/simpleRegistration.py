from __future__ import print_function

import SimpleITK as sitk
import sys
import os
OUTPUT_DIR = 'Output'

def command_iteration(method) :
    print("{0:3} = {1:10.5f} : {2}".format(method.GetOptimizerIteration(),
                                   method.GetMetricValue(),
                                   method.GetOptimizerPosition()))

# if len ( sys.argv ) < 4:
#     print( "Usage: {0} <fixedImageFilter> <movingImageFile> <outputTransformFile>".format(sys.argv[0]))
#     sys.exit ( 1 )


fixed = sitk.ReadImage("data/CT_2D_head_fixed.mha", sitk.sitkFloat32)
moving = sitk.ReadImage("data/CT_2D_head_moving.mha", sitk.sitkFloat32)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsMeanSquares()
R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200 )
R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
R.SetInterpolator(sitk.sitkLinear)

R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )

outTx = R.Execute(fixed, moving)

print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))

# sitk.WriteImage(R.GetResultImage())

resampler = sitk.ResampleImageFilter()
resampler.SetReferenceImage(fixed)
resampler.SetInterpolator(sitk.sitkLinear)
resampler.SetDefaultPixelValue(100)
resampler.SetTransform(outTx)

out = resampler.Execute(moving)
simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)
sitk.Show( cimg, "ImageRegistration1 Composition" )

# sitk.WriteTransform(outTx,  sys.argv[3])

# if ( not "SITK_NOSHOW" in os.environ ):

#     resampler = sitk.ResampleImageFilter()
#     resampler.SetReferenceImage(fixed)
#     resampler.SetInterpolator(sitk.sitkLinear)
#     resampler.SetDefaultPixelValue(100)
#     resampler.SetTransform(outTx)

#     out = resampler.Execute(moving)
#     simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
#     simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
#     cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)
#     sitk.Show( cimg, "ImageRegistration1 Composition" )

# import SimpleITK as sitk

# elastixImageFilter = sitk.ElastixImageFilter()
# elastixImageFilter.SetFixedImage(sitk.ReadImage("data/CT_2D_head_fixed.mha"))
# elastixImageFilter.SetMovingImage(sitk.ReadImage("data/CT_2D_head_moving.mha"))
# elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
# elastixImageFilter.Execute()
# sitk.WriteImage(elastixImageFilter.GetResultImage())