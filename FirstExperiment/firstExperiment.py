import SimpleITK as sitk


fixed_image = sitk.ReadImage('data/FirstExperiment/Normal001-DTI.mha', sitk.sitkFloat32)
fixedImage2d = sitk.Cast(fixed_image, sitk.sitkFloat32)
# fixedImage2d = sitk.Extract(fixedImage3d, (fixedImage3d.GetWidth(), fixedImage3d.GetHeight(), 0), (0, 0, 0))

moving_image = sitk.ReadImage('data/FirstExperiment/Normal001-MRA.mha', sitk.sitkFloat32)
# movingImage2d = sitk.Extract(movingImage3d, (movingImage3d.GetWidth(), movingImage3d.GetHeight(), 0), (0, 0, 0))

movingImage2d = sitk.Cast(moving_image, sitk.sitkFloat32)

# initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
#                                                       moving_image, 
#                                                       sitk.Euler2DTransform(), 
#                                                       sitk.CenteredTransformInitializerFilter.GEOMETRY)

parameterMap = sitk.GetDefaultParameterMap('affine')
parameterMap["FixedImagePyramid"] = ["FixedShrinkingImagePyramid"] 
parameterMap["MovingImagePyramid"] = ["MovingShrinkingImagePyramid"] 

elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage2d)
elastixImageFilter.SetMovingImage(movingImage2d)
elastixImageFilter.SetParameterMap(parameterMap)
elastixImageFilter.Execute()

resultImage = elastixImageFilter.GetResultImage()
sitk.WriteImage(resultImage, "resultImage2117.nii")
transformParameterMap = elastixImageFilter.GetTransformParameterMap()