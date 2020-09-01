import SimpleITK as sitk

p = sitk.ParameterMap()

p['Registration'] = ['MultiMetricMultiResolutionRegistration']

# Non-rigid transform
p['Transform'] = ['BSplineTransform']

p['Metric'] = ['AdvancedMattesMutualInformation']

p['Metric0Weight'] = ['1.0']

p['Metric1Weight'] = ['1.0']

p['MaximumNumberOfIterations'] = ['256']
