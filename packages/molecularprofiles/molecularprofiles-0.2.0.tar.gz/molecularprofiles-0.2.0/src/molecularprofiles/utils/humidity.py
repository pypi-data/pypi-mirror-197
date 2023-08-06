"""
Calculates the properties of moist air, including:
* density
* compressibility
* enhancement factor
* saturation vapor pressure
* molar fraction from relative humidity
* partial pressure from relative humidity

Adapted from MHumidity, written by Markus Gaug <markus.gaug@uab.cat>, 04/2013
"""

from math import exp, sqrt, log10
import numpy as np
from molecularprofiles.utils.constants import GAS_CONSTANT, MOLAR_MASS_WATER_VAPOR


def compressibility(pressure, temp, x_w):
    """
    Calculates the compressibility of moist air, according to:
    R.S. Davis, "Equation for the determination of the density of moist air"
    Metrologia, 29 (1992) 67-70

    See also Eq. 16 in:
    C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
    "Improved algorithm for calculations of Rayleigh-scattering optical depth
    in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320

    Parameters
    ----------
    pressure : float
        Pressure in hPa
    temp : float
        Temperature in K
    x_w : float
        Molar fraction of water vapor

    Returns
    -------
    float
        compressibility of moist air (dimensionless constant, 0 < Z < 1)
    """
    temp_celsius = temp - 273.15  # temperature in deg. C
    pressure_temp_ratio = (
        100 * pressure / temp
    )  # ratio of pressure to temperature, with pressure in Pascals
    a_0 = 1.58123e-6  # K Pa^-1
    a_1 = -2.9331e-8  # Pa^-1
    a_2 = 1.1043e-10  # K^-1 Pa^-1
    b_0 = 5.707e-6  # K Pa^-1
    b_1 = -2.051e-8  # Pa^-1
    c_0 = 1.9898e-4  # K Pa^-1
    c_1 = -2.376e-6  # Pa^-1
    d_0 = 1.83e-11  # K^2 Pa^-2
    d_1 = -7.65e-9  # K^2 Pa^-2
    moist_air_compressibility = (
        1
        - pressure_temp_ratio
        * (
            a_0
            + a_1 * temp_celsius
            + a_2 * temp_celsius * temp_celsius
            + b_0 * x_w
            + b_1 * x_w * temp_celsius
            + c_0 * x_w * x_w
            + c_1 * x_w * x_w * temp_celsius
        )
        + pressure_temp_ratio * pressure_temp_ratio * (d_0 + d_1 * x_w * x_w)
    )
    return moist_air_compressibility


def enhancement_factor(pressure, temp):
    """
    Calculates the enhancement factor of water vapor in air.

    Calculated according to Eq. 14 of:
    C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
    "Improved algorithm for calculations of Rayleigh-scattering optical depth
    in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320

    Parameters
    ----------
    pressure : float
        Pressure in Pa
    temp : float
        Temperature in K

    Returns
    -------
    float
        Enhancement factor (dimensionless constant)
    """
    temp_celsius = temp - 273.15  # temparture in deg. C
    factor = 1.00062 + 3.14e-8 * pressure + 5.6e-7 * pow(temp_celsius, 2)
    return factor


# TODO: This function needs a simple unit test to check which function is called
def saturation_vapor_pressure(temp):
    """Define which function will be called depending on temperature"""
    if temp > 273.15:
        return saturation_vapor_pressure_davis(temp)
    else:
        return saturation_vapor_pressure_goff_gratch(temp)


def saturation_vapor_pressure_davis(temp):
    """
    Calculates the vapor pressure at saturation, according to:
    R.S. Davis, "Equation for the determination of the density of moist air"
    Metrologia, 29 (1992) 67-70

    See also Eq. 15 in:
    C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
    "Improved algorithm for calculations of Rayleigh-scattering optical depth
    in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320

    Parameters
    ----------
    temp : float
        Temperature in K

    Returns
    -------
    float
        Saturation vapor pressure in hPa
    """
    psv_davis = np.exp(
        1.2378847e-5 * temp * temp - 1.9121316e-2 * temp + 33.93711047 - 6343.1645 / temp
    )
    return psv_davis / 100  # divide by 100 for hPa


# TODO: Goff-Gratch doesn't seem to be as good as Buck, or maybe Wexler
def saturation_vapor_pressure_goff_gratch(temp):
    """
    Calculates the vapor pressure at saturation, according to:
    Smithsonian Tables (1984); after Goff and Gratch (1946).
    See here: http://cires.colorado.edu/~voemel/vp.html

    This equation is recommended for temperatures below 0 deg. C.

    Parameters
    ----------
    temp : float
        Temperature in K

    Returns
    -------
    float
        Saturation vapor pressure in hPa
    """
    theta = 373.16 / temp  # ratio of steam point (100 deg C) to temperature
    c = [
        -7.90298 * (theta - 1),
        5.02808 * log10(theta),
        -1.3816e-7 * (pow(10, 11.344 * (1 - 1 / theta)) - 1),
        8.1328e-3 * (pow(10, -3.49149 * (theta - 1)) - 1),
        log10(1013.246),
    ]
    log10_ew = np.sum(c)
    psv_goff_gratch = pow(10, log10_ew)
    return psv_goff_gratch


# TODO: Check this function and write unit test
def saturation_vapor_pressure_over_water(temp):
    """
    Calculates the vapor pressure at saturation over water, according to IAPWS:
    International Association for the Properties of Water and Steam,
    Peter H. Huang, "New equations for water vapor pressure in the temperature
    range -100 deg. C to 100 deg. C for use with the 1997 NIST/ASME steam tables"
    Papers and abstracts from the third international symposium on humidity and
    moisture, Vol. 1, p. 69-76, National Physical Laboratory, Teddington,
    Middlesex, UK, April 1998.
    See also: http://cires.colorado.edu/~voemel/vp.html

    Parameters
    ----------
    temp : float
        Temperature in K

    Returns
    -------
    float
        Saturation vapor pressure in hPa
    """
    omega = temp - 2.38555575678e-01 / (temp - 6.50175348448e02)
    omega2 = omega * omega
    A = omega2 + 1.16705214528e03 * omega - 7.24213167032e05
    B = -1.70738469401e01 * omega2 + 1.20208247025e04 * omega - 3.23255503223e06
    C = 1.49151086135e01 * omega2 - 4.82326573616e03 * omega + 4.05113405421e05
    water_psv = -B + sqrt(B * B - 4 * A * C)
    return 1e4 * pow(2 * C / water_psv, 4)


# TODO: Check this function and write unit test
def saturation_vapor_pressure_over_ice(temp):
    """
    Calculates the vapor pressure at saturation over ice, according to IAPWS:
    International Association for the Properties of Water and Steam,
    Peter H. Huang, "New equations for water vapor pressure in the temperature
    range -100 deg. C to 100 deg. C for use with the 1997 NIST/ASME steam tables"
    Papers and abstracts from the third international symposium on humidity and
    moisture, Vol. 1, p. 69-76, National Physical Laboratory, Teddington,
    Middlesex, UK, April 1998.
    See also: http://cires.colorado.edu/~voemel/vp.html

    Parameters
    ----------
    temp : float
        Temperature in K

    Returns
    -------
    float
        Saturation vapor pressure in hPa
    """
    theta = temp / 273.16
    ice_psv = -13.928169 * (1 - pow(theta, -1.5)) + 34.7078238 * (1 - pow(theta, -1.25))
    return 6.11657 * exp(ice_psv)


def molar_fraction_water_vapor(pressure, temp, relative_humidity):
    """
    Calculates the molar fraction of water vapor in moist air.

    See the text above Eq. 14 of:
    C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
    "Improved algorithm for calculations of Rayleigh-scattering optical depth
    in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320

    Parameters
    ----------
    pressure : float
        Pressure in hPa
    temp : float
        Temperature in K
    relative_humidity : float
        Relative humidity in percent

    Returns
    -------
    float
        Molar fraction of water vapor in moist air (dimensionless)
    """
    factor = enhancement_factor(100 * pressure, temp)
    psv = saturation_vapor_pressure(temp)
    x_w = factor * relative_humidity / 100 * psv / pressure  # x_w = f * h * E(temp)/pressure
    return x_w


def density_moist_air(pressure, temp, moist_air_compressibility, x_w, co2_bkg):
    """
    Density equation of moist air, according to:
    R.S. Davis, "Equation for the determination of the density of moist air"
    Metrologia, 29 (1992) 67-70

    Parameters
    ----------
    pressure : float
        Pressure in hPa (beware, different unit than in Davis!)
    temp : float
        Temperature in Kelvin
    moist_air_compressibility : float
        Compressibility (see compressibility() in this module)
    x_w : float
        Molar fraction of water vapor
    co2_bkg : float
        CO2 volume concentration in ppmv (different unit than in Davis!)

    Returns
    -------
    float
        Density of moist air (kg m^-3)
    """
    pressure *= 100  # convert pressure to Pa
    R = GAS_CONSTANT.to_value()
    m_w = MOLAR_MASS_WATER_VAPOR.to_value()
    m_a = 1e-3 * (28.9635 + 12.011e-6 * (co2_bkg - 400))  # molar mass of dry air [kg/mol]
    rho = (
        pressure * m_a / (moist_air_compressibility * R * temp) * (1 - x_w * (1 - m_w / m_a))
    )  # Tomasi eq. 12
    return rho


# TODO: This function has no unit test
def partial_pressure_water_vapor(temp, relative_humidity):
    """
    Calculates the partial pressure of water vapor in the air.

    Parameters
    ----------
    temp : float
        Temperature in K
    relative_humidity : float
        Relative humidity in percent

    Returns
    -------
    float
        Water vapor partial pressure in hPa
    """
    # water vapor pressure: e = h * E(temp)
    e_w = (relative_humidity / 100) * saturation_vapor_pressure_davis(temp)
    return e_w
