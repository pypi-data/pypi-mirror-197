import astropy.units as u

# standard atmosphere thermodynamic values
STD_NUMBER_DENSITY = (
    2.546899e19 / u.cm**3
)  # [cm^-3] molecular number density for standard air conditions
STD_AIR_PRESSURE = 1013.25 * u.hPa  # [hPa]   standard air pressure
STD_AIR_TEMPERATURE = 288.15 * u.K  # [K]     standard air temperature
DENSITY_SCALE_HEIGHT = 9500.0 * u.km  # [km]    density scale hight for La Palma Winter
STD_RELATIVE_HUMIDITY = 45.9 * u.percent  # [%]     standard air rel. humidity
# atmospheric composition
NITROGEN_RATIO = 0.78084 * u.dimensionless_unscaled
OXYGEN_RATIO = 0.20946 * u.dimensionless_unscaled
ARGON_RATIO = 0.00934 * u.dimensionless_unscaled
GAS_CONSTANT = 8.31451 * u.J / (u.K * u.mol)  # gas constant [J/mol/K]
MOLAR_MASS_WATER_VAPOR = 0.018015 * u.kg / u.mol  # molar mass of water vapor [kg/mol]
# misc physics constants
STD_GRAVITATIONAL_ACCELERATION = (
    9.80665 * u.m / u.s**2
)  # standard acceleration of free fall [m/s^2]
STD_EARTH_RADIUS = 6245 * u.km  # Earth radius for geopotential height conversion [km]
