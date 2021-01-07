import SimpleITK as sitk


iterationNumbers = 6000
spatialSamples = 6000

simpleElastix = sitk.ElastixImageFilter()
simpleElastix.SetParameter("Registration","MultiMetricMultiResolutionRegistration")
simpleElastix.SetParameter( "Metric", ("NormalizedMutualInformation", "CorrespondingPointsEuclideanDistanceMetric",))
simpleElastix.SetParameter("Metric0Weight", "0.0")

simpleElastix.LogToConsoleOn()
simpleElastix.SetParameterMap(sitk.GetDefaultParameterMap('translation'))
simpleElastix.AddParameterMap(sitk.GetDefaultParameterMap('affine'))

simpleElastix.SetParameter("MaximumNumberOfIterations" , str(iterationNumbers))
simpleElastix.SetParameter("NumberOfSpatialSamples" , str(spatialSamples))

simpleElastix.PrintParameterMap()

fixImage = sitk.ReadImage("data/FirstExperiment/Normal001-DTI.mha",sitk.sitkFloat32)
movingImage = sitk.ReadImage("data/FirstExperiment/Normal001-MRA.mha",sitk.sitkFloat32)

simpleElastix.SetFixedImage(fixImage)
simpleElastix.SetMovingImage(movingImage)

simpleElastix.SetFixedPointSetFileName("fixpoint.txt")
simpleElastix.SetMovingPointSetFileName("movpoint.txt")
simpleElastix.Execute()

img = simpleElastix.GetResultImage()