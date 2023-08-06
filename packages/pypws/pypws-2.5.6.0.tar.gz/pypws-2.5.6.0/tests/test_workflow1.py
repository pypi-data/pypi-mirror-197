from pypws.entities import *
from pypws.calculations import *
from pypws.enums import *

def test_workflow1():

    print('DEBUG: API platform: %s' % getAnalyticsApiTarget())
    print('DEBUG: Client alias: %s' % getClientAliasId())

    # Declare the entities required by the vesselLeakCalculation instance.
    dischargeParameters = DischargeParameters()
    leak = Leak()
    state = State()
    material = Material()
    vessel = Vessel()

    # Set the data for items with data mappings to the vesselLeakCalculation instance.
    # Set data for the dischargeParameters property.
    dischargeParameters.flashAtOrifice = FlashAtOrifice.DISALLOW_LIQUID_FLASH

    # Set data for the leak property.
    leak.releaseAngle = 0.0
    leak.timeVaryingOption = TimeVaryingOption.TIME_VARYING_RATE
    leak.holeDiameter = 0.05
    leak.holeHeightFraction = 0.0

    # Set data for the state property.
    state.pressure = 500000.0
    state.temperature = 280.0
    state.liquidFraction = 0.0
    state.flashFlag = FluidSpec.TP

    # Set data for the material property.
    material.name = "NATURAL GAS"
    material.componentCount = 2
    materialComponent = MaterialComponent()
    materialComponent.name = "METHANE"
    materialComponent.moleFraction = 0.85
    material.components.append(materialComponent)

    materialComponent = MaterialComponent()
    materialComponent.name = "ETHANE"
    materialComponent.moleFraction = 0.15
    material.components.append(materialComponent)

    material.propertyTemplate = PropertyTemplate.PHAST_MC

    # Set data for the vessel property.
    vessel.location.x = 0.0
    vessel.location.y = 0.0
    vessel.location.z = 0.0
    vessel.scope = Scope.GLOBAL
    vessel.state = state
    vessel.diameter = 5.0
    vessel.height = 0.0
    vessel.length = 12.0
    vessel.width = 0.0
    vessel.shape = VesselShape.HORIZONTAL_CYLINDER
    vessel.material = material
    vessel.vesselConditions = VesselConditions.PURE_GAS
    vessel.liquidFillFractionByVolume = 0.0

    # Declare the vesselLeakCalculation.
    vesselLeakCalculation = VesselLeakCalculation()

    vesselLeakCalculation.vessel = vessel
    vesselLeakCalculation.leak = leak
    vesselLeakCalculation.dischargeParameters = dischargeParameters

    # Run the vesselLeakCalculation instance.
    print('.... Running vessel leak calculation')
    resultCode = vesselLeakCalculation.run()

    vesselLeakCalculation.print_messages()
    assert resultCode == ResultCode.SUCCESS, f'Errors encountered running vesselLeakCalculation. Result Code: {resultCode}.'
    print('>>>> Vessel leak calculation ran successfully')

    # Declare the entities required by the jetFireCalculation instance.
    weather = Weather()
    substrate = Substrate()

    # Set the data for items with data mappings to the jetFireCalculation instance.
    # Set data for the weather property.
    weather.windSpeed = 5.0
    weather.stabilityClass = AtmosphericStabilityClass.STABILITY_B
    weather.temperature = 283.0
    weather.relativeHumidity = 0.7
    weather.mixingLayerHeight = 800.0
    weather.solarRadiation = 500.0

    # Set data for the substrate property.
    substrate.surfaceRoughness = 0.1
    substrate.surfaceType = SurfaceType.LAND
    substrate.poolSurfaceType = PoolSurfaceType.CONCRETE

    # Declare the jetFireCalculation.
    jetFireCalculation = JetFireCalculation()

    jetFireCalculation.material = vesselLeakCalculation.vessel.material
    jetFireCalculation.dischargeRecords = vesselLeakCalculation.dischargeRecords
    jetFireCalculation.dischargeResult = vesselLeakCalculation.dischargeResult
    jetFireCalculation.substrate = substrate
    jetFireCalculation.weather = weather

    # Run the jetFireCalculation instance.
    print('.... Running jet fire calculation')
    resultCode = jetFireCalculation.run()

    jetFireCalculation.print_messages()
    assert resultCode == ResultCode.SUCCESS, f'Errors encountered running jetFireCalculation. Result Code: {resultCode}.'
    print('>>>> Jet fire calculation ran successfully')

    # Declare the entities required by the radiationContourCalculation instance.
    flammableParameters = FlammableParameters()
    flammableOutputConfig = FlammableOutputConfig()

    # Set the data for items with data mappings to the radiationContourCalculation instance.
    # Set data for the flammableParameters property.
    flammableParameters.maxExposureDuration = 20.0
    flammableParameters.radiationRelativeTolerance = 0.001
    flammableParameters.poolFireType = PoolFireType.EARLY

    # Set data for the flammableOutputConfig property.
    flammableOutputConfig.position.x = 0.0
    flammableOutputConfig.position.y = 0.0
    flammableOutputConfig.position.z = 0.0
    flammableOutputConfig.radiationType = RadiationType.INTENSITY
    flammableOutputConfig.contourType = ContourType.FOOTPRINT
    flammableOutputConfig.radiationLevel = 4000.0
    flammableOutputConfig.radiationResolution = Resolution.MEDIUM
    flammableOutputConfig.overpressureLevel = 2068.0
    flammableOutputConfig.transect.transectStartPoint.x = 0.0
    flammableOutputConfig.transect.transectStartPoint.y = 0.0
    flammableOutputConfig.transect.transectStartPoint.z = 0.0
    flammableOutputConfig.transect.transectEndPoint.x = 0.0
    flammableOutputConfig.transect.transectEndPoint.y = 0.0
    flammableOutputConfig.transect.transectEndPoint.z = 0.0

    # Declare the radiationContourCalculation.
    radiationContourCalculation = RadiationContourCalculation()

    radiationContourCalculation.flameResult = jetFireCalculation.flameResult
    radiationContourCalculation.flameRecords = jetFireCalculation.flameRecords
    radiationContourCalculation.weather = weather
    radiationContourCalculation.flammableOutputConfig = flammableOutputConfig
    radiationContourCalculation.flammableParameters = flammableParameters

    # Run the radiationContourCalculation instance.
    print('.... Running radiation contour calculation')
    resultCode = radiationContourCalculation.run()

    radiationContourCalculation.print_messages()
    assert resultCode == ResultCode.SUCCESS, f'Errors encountered running radiationContourCalculation. Result Code: {resultCode}.'
    print('>>>> Radiation contour calculation ran successfully')
