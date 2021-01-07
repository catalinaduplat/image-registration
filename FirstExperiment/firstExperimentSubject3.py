import SimpleITK as sitk
import numpy as np

## Non-rigid transform


rotation_center = (100, 100, 100)
axis = (0,0,1)
angle = np.pi/2.0
translation = (1,2,3)
scale_factor = 2.0
similarity = sitk.Similarity3DTransform(scale_factor, axis, angle, translation, rotation_center)


## Affine
affine = sitk.AffineTransform(3)
affine.SetMatrix(similarity.GetMatrix())
affine.SetTranslation(similarity.GetTranslation())
affine.SetCenter(similarity.GetCenter())

## Scale
scale = sitk.ScaleTransform(3, (0.5,2,0))


# fixed_image = sitk.ReadImage('data/FirstExperiment/subject3/Normal003-MRA.mha', sitk.sitkFloat32)
fixed_image = sitk.ReadImage('data/FirstExperiment/subject3/Normal003-DTI.mha', sitk.sitkFloat32)

# moving_image = sitk.ReadImage('data/FirstExperiment/subject3/Normal003-T1-Flash.mha', sitk.sitkFloat32)
moving_image = sitk.ReadImage('data/FirstExperiment/subject3/Normal003-T2.mha', sitk.sitkFloat32)

initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      affine,
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())


# Registration
registration_method = sitk.ImageRegistrationMethod()

# Similarity metric settings.
registration_method.SetMetricAsCorrelation()
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.1)

registration_method.SetInterpolator(sitk.sitkLinear)

# Optimizer settings.
registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
registration_method.SetOptimizerScalesFromPhysicalShift()

# Setup for the multi-resolution framework.            
registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

# Don't optimize in-place, we would possibly like to run this cell multiple times.
registration_method.SetInitialTransform(initial_transform, inPlace=False)

final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32), 
                                               sitk.Cast(moving_image, sitk.sitkFloat32))

# Plot
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
sitk.WriteImage(moving_resampled, 'Output/subject3/resultImage1-003.mha')