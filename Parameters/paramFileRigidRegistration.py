import SimpleITK as sitk

p = sitk.ParameterMap()

p['Registration'] = ['MultiResolutionRegistration']

# Rigid transform
p['Transform'] = ['EulerTransform']

p['Interpolator'] = ['LinearInterpolator']

p['Metric'] = ['AdvancedMattesMutualInformation']

p['MaximumNumberOfIterations'] = ['256']