import SimpleITK as sitk

fixedImage = sitk.ReadImage('data/FirstExperiment/sub-2117-T1.nii')
movingImage = sitk.ReadImage('data/FirstExperiment/sub-2117-T2.nii')
parameterMap = sitk.GetDefaultParameterMap('translation')

elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)
elastixImageFilter.SetMovingImage(movingImage)
elastixImageFilter.SetParameterMap(parameterMap)
elastixImageFilter.Execute()

resultImage = elastixImageFilter.GetResultImage()
transformParameterMap = elastixImageFilter.GetTransformParameterMap()