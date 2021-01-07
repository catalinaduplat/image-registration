import SimpleITK as sitk

## Elastic transform

fixed_image = sitk.ReadImage('data/FirstExperiment/subject1/Normal001-T1-Flash.mha', sitk.sitkFloat32)
moving_image = sitk.ReadImage('data/FirstExperiment/subject1/Normal001-DTI.mha', sitk.sitkFloat32)

# fixed_image = sitk.ReadImage('data/FirstExperiment/subject1/Normal001-T1-Flash.mha', sitk.sitkFloat32)
# moving_image = sitk.ReadImage('data/FirstExperiment/subject1/Normal001-T2.mha', sitk.sitkFloat32)

# Determine the number of BSpline control points using the physical spacing we want for the control grid. 
grid_physical_spacing = [50.0, 50.0, 50.0] # A control point every 50mm
image_physical_size = [size*spacing for size,spacing in zip(fixed_image.GetSize(), fixed_image.GetSpacing())]
mesh_size = [int(image_size/grid_spacing + 0.5) \
                for image_size,grid_spacing in zip(image_physical_size,grid_physical_spacing)]

initial_transform = sitk.BSplineTransformInitializer(image1 = fixed_image, 
                                                        transformDomainMeshSize = mesh_size, order=3)

moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())


# Registration
registration_method = sitk.ImageRegistrationMethod()

# Similarity metric settings.
registration_method.SetMetricAsCorrelation()
# registration_method.SetMetricAsMeanSquares()
# registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
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
sitk.WriteImage(moving_resampled, 'Output/subject1/T1-DTI-SUBJECT001.mha')