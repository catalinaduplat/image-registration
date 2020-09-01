import SimpleITK as sitk

p = sitk.ParameterMap()

p['Registration'] = ['MultiResolutionRegistration']

# The affine transform allows for shearing and scaling in addition to the rotation and translation
p['Transform'] = ['AffineTransform']

p['Metric'] = ['AdvancedMattesMutualInformation']

p['MaximumNumberOfIterations'] = ['256']