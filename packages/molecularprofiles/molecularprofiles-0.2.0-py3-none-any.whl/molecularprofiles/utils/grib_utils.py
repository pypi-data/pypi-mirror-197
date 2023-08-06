"""
Set of utilities for decoding and analysing grib files.
"""

import os
import logging
import logging.config
import multiprocessing
import numpy as np
import pygrib as pg
import astropy.units as u
from astropy.coordinates import Angle, Latitude, Longitude
from astropy.time import Time
from astropy.table import Table, join, vstack
from molecularprofiles.utils.constants import (
    STD_NUMBER_DENSITY,
    STD_AIR_PRESSURE,
    STD_AIR_TEMPERATURE,
    DENSITY_SCALE_HEIGHT,
    STD_GRAVITATIONAL_ACCELERATION,
    STD_EARTH_RADIUS,
)

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def get_altitude_from_geopotential_height(geopotential_height, latitude):
    """
    Function to compute the real altitude from the geopotential value at
    a certain coordinate on Earth.
    Uses expression 20 from http://dx.doi.org/10.1029/2002JB002333

    Parameters
    ----------
    geopotential : Quantity [u.m]
        Geopotential height
    latitude : Latitude
        Geographical latitude of interest.

    Returns
    -------
    Quantity [u.m]
        Real altitude as fGeoidOffset.
    """
    return (1.0 + 0.002644 * np.cos(2 * latitude)) * geopotential_height + (
        1 + 0.0089 * np.cos(2 * latitude)
    ) * geopotential_height**2 / STD_EARTH_RADIUS


def get_gribfile_variables(filename):
    """
    Returns all the different variable names in a grib file.

    Parameters
    ----------
    filename : str
       Path to the grib file.

    Returns
    -------
    list
        varname (str): variable names.
    list
        varshortname (str): variable short names.
    """
    logger.debug("Opening %s grib file", filename)
    with pg.open(filename) as grib_file:
        varshortname = []
        varname = []
        grib_file.read(10)[0]
        while True:
            v = grib_file.read(1)[0]
            variable_name = v.name.replace(" ", "")
            variable_short_name = v.shortName
            if variable_name not in varname:
                varname.append(variable_name)
                varshortname.append(variable_short_name)
            else:
                break
    return varname, varshortname


def get_plevels(atmo_parameter):
    """
    The measurements of atmospheres parameters are taking place in various pressure levels.
    This functions returns the indices of these levels where we have measurements
    for the given atmospheric parameter.
    E.g. for GDAS data that should be a range of values [1, 23].

    Parameters
    ----------
    atmo_parameter : str FIXME: this description doesn't
        Atmospheric parameter from grib file.

    Returns
    -------
    list
        List (int) with the indices of the pressure levels
    """

    plevels = []
    index = []
    for i in range(len(atmo_parameter)):
        pressure_level = atmo_parameter[i].level
        if pressure_level not in plevels:
            plevels.append(pressure_level)
            index.append(i + 1)
        else:
            break
    return index


def create_table(grib_var):
    """
    Create astropy.table.Table from grib record

    Parameters
    ----------
    grib_var :
        Grib data record

     Returns
     -------
     astropy.table.Table
         Table with the different measurables together with their dimensions
    """
    res = Table()
    for v in grib_var:
        unit = u.Unit(v.units)
        timestamp = Time(
            {"year": v.year, "month": v.month, "day": v.day, "hour": v.hour}, scale="utc"
        )
        pressure_level = v.level * u.hPa
        latitudes = Latitude(v.latlons()[0].ravel() * u.deg)
        longitudes = Longitude(v.latlons()[1].ravel() * u.deg, wrap_angle=180 * u.deg)
        if isinstance(v.values, float):
            vals = np.array([v.values]) * unit
        else:
            vals = v.values.ravel() * unit
        t = Table([latitudes, longitudes], names=["Latitude", "Longitude"])
        t["Timestamp"] = timestamp
        t["Pressure"] = pressure_level
        t[v.name] = vals
        res = vstack([res, t])
    return res


def get_grib_file_data(filename):
    """
    This function opens a grib file, selects the parameters
    (all available: Temperature, Geopotential, RH, ...),
    and creates an astropy.table.Table with them.
    Parameters
    ----------
    filename : str
        Path to the grib file.

    Returns
    -------
    astropy.table.Table
        Table with grib file data gridded in isobaric levels
    """

    logger.debug("Working with %s", filename)
    logger.debug("Getting all variable names...")
    variable_names, variable_short_names = get_gribfile_variables(filename)
    logger.info("Indexing the file %s (this might take a while...)", filename)
    grib_file = pg.index(filename, "shortName", "typeOfLevel")
    logger.debug(
        "Selecting the parameters information for %s (this might take a while...)", filename
    )
    gpm = u.def_unit("gpm", u.m**2 / (STD_GRAVITATIONAL_ACCELERATION * u.s**2))
    u.add_enabled_units([gpm])
    data = Table()
    for short_name in variable_short_names:
        if short_name == "unknown":
            continue
        var = grib_file.select(shortName=short_name, typeOfLevel="isobaricInhPa")
        try:
            t = create_table(var)
        except ValueError:
            logger.warning("Grib message can't be parsed, skipping")
            continue
        if len(data) == 0:
            data = t
        else:
            data = join(data, t, join_type="outer")
    return data


def extend_grib_data(data):
    """
    Extends grib data table by filling the gaps in data and calculating additional quantities:
        - altitude
        - density
        - exponential density
        - wind direction

    Parameters
    ----------
    astropy.table.Table
        Table with grib data
    Returns
    -------
    astropy.table.Table
        Extended table with grib data and additional quantities
    """
    logger.debug("Check for gaps in relative humidity and fill them if neccessary")
    data["Relative humidity"] = data["Relative humidity"].filled(0)
    logger.debug("Compute altitude from geopotential")
    if "Geopotential Height" in data.keys():
        data["Altitude"] = get_altitude_from_geopotential_height(
            data["Geopotential Height"], data["Latitude"]
        )
    else:
        data["Altitude"] = get_altitude_from_geopotential_height(
            data["Geopotential Height"] / STD_GRAVITATIONAL_ACCELERATION, data["Latitude"]
        )
    logger.debug("Compute density")
    data["Density"] = (
        STD_NUMBER_DENSITY
        * data["Pressure"]
        / STD_AIR_PRESSURE
        * STD_AIR_TEMPERATURE
        / data["Temperature"]
    )
    logger.debug("Compute exponential density")
    data["Exponential Density"] = (
        data["Density"] / STD_NUMBER_DENSITY * np.exp(data["Altitude"] / DENSITY_SCALE_HEIGHT)
    )
    logger.debug("Compute wind speed")
    data["Wind Speed"] = np.sqrt(
        data["U component of wind"] ** 2 + data["V component of wind"] ** 2
    )
    logger.debug("Compute wind direction")
    data["Wind Direction"] = Angle(
        np.array(np.arctan2(-data["V component of wind"].value, -data["U component of wind"].value)),
        unit=u.rad,
    ).wrap_at(360 * u.deg)
    return data


def save_grib_table(data, filename, fmt="ecsv"):
    """
    Save grib data in a file according to provided format.

    Parameters
    ----------
    data: astropy.table.Table
        Grib data in astropy table
    filename: str
        Path to the file
    fmt: str
        Desired format
    """
    if fmt == "ecsv":
        data.write(filename, format="ascii.ecsv", overwrite=True)
    elif fmt == "magic":
        raise NotImplementedError("Magic txt format writing is not implemented yet")
    else:
        raise ValueError("Not recognized format")


def read_grib_file_to_magic(
    file_name, gridstep, observatory=None, lat=None, lon=None
):  # FIXME this function requires further  refactoring, is broken for the moment!!!

    raise NotImplementedError("MAGIC txt writing is not yet supported")
    """
    This function opens a grib file, selects all parameters
    and finally creates a txt file where these parameters, together with date, year, month,
    day, hour, pressure level, real height and density, are written.
    Input: file_name (string)
           observatory (string). Possible values are 'north' or 'south'
           gridstep (float): grid spacing (0.75 degrees for ECMWF and 1.0 degrees for GDAS)
    Output: a txt file with the exact name as the input file name,
            but with .txt as extension in a format that can be read by MARS
    if os.path.exists(os.path.splitext(file_name)[0] + ".txt"):
        logger.critical(
            f"Output file {os.path.splitext(file_name)[0]}.txt already exists. Aborting."
        )
        sys.exit()

    vn, datadict = get_grib_file_data(file_name)

    pressure_level_index = get_plevels(datadict["Temperature"])
    new_pressure_level_index = pressure_level_index[::-1] * int(
        (len(datadict["Temperature"]) / len(pressure_level_index))
    )

    if observatory:
        latitude_obs, longitude_obs = get_observatory_coordinates(observatory)
    else:
        latitude_obs, longitude_obs = lat, lon

    lat_gridpoint, lon_gridpoint = get_closest_gridpoint(latitude_obs, longitude_obs, gridstep)

    # We create the table file and fill it with the information stored in
    # the above variables, plus the height and density computed form them.

    logger.info("creating the txt file containing the selected data...")
    table_file = open(file_name.split(".")[0] + "MAGIC_format.txt", "w")

    for j in np.arange(len(datadict["Temperature"])):

        if (type(datadict["Temperature"][j].values) == float) or (
            len(datadict["Temperature"][j].values) == 1
        ):
            if new_pressure_level_index[j] == 1:
                print(str([0.00] * 34)[1:-1].replace(",", " "), file=table_file)
            if "GeopotentialHeight" in vn:
                height = get_altitude_from_geopotential_height(
                    datadict["GeopotentialHeight"][j].values, latitude_obs
                )
            else:
                height = get_altitude_from_geopotential_height(
                    datadict["Geopotential"][j].values / STD_GRAVITATIONAL_ACCELERATION,
                    latitude_obs,
                )

            fields = (
                datadict["Temperature"][j].year - 2000,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                new_pressure_level_index[j],
                height,
                datadict["Temperature"][j].values,
                datadict["Ucomponentofwind"][j].values,
                datadict["Vcomponentofwind"][j].values,
                # RH[j],  FIXME this variable is not defined, the function is broken!
            )
            row_str = "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
            row_str = row_str.format(*fields)
            table_file.write(row_str + "\n")

        else:  # this is just in case the grib file contains more than one grid point
            if new_pressure_level_index[j] == 1:
                print(str([0.00] * 34)[1:-1].replace(",", " "), file=table_file)
            if "GeopotentialHeight" in vn:
                height = np.float(
                    datadict["GeopotentialHeight"][j].values[
                        (datadict["GeopotentialHeight"][j].data()[1] == lat_gridpoint)
                        & (datadict["GeopotentialHeight"][j].data()[2] == lon_gridpoint)
                    ]
                )
            else:
                height = get_altitude_from_geopotential_height(
                    datadict["Geopotential"][j].values / STD_GRAVITATIONAL_ACCELERATION,
                    latitude_obs,
                )

            temperature = np.float(
                datadict["Temperature"][j].values[
                    (datadict["Temperature"][j].data()[1] == lat_gridpoint)
                    & (datadict["Temperature"][j].data()[2] == lon_gridpoint)
                ]
            )

            fields = (
                datadict["Temperature"][j].year - 2000,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                new_pressure_level_index[j],
                height,
                temperature,
                datadict["Ucomponentofwind"][j].values,
                datadict["Vcomponentofwind"][j].values,
                # RH[j],  FIXME this variable is not defined, the function is broken!
            )
            row_str = "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
            row_str = row_str.format(*fields)
            table_file.write(row_str + "\n")
    table_file.close()
    """


def read_grib_file_to_magic_from_txt(txt_file):
    raise NotImplementedError("MAGIC txt writing is not yet supported")
    """
    :param txt_file:
    :return:
    input_f = open(txt_file, "r")
    output_f = open(txt_file + "MAGIC_format.txt", "w")

    date, year, month, day, hour, mjd, p, T, h, n, U, V, RH = np.loadtxt(
        input_f, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13), unpack=True, skiprows=1
    )

    pl = np.unique(p)[::-1]
    pl_index = (np.arange(len(pl)) + 1).tolist()
    new_pl_index = pl_index * int((len(T) / len(pl_index)))
    remaining_index = len(p) - len(new_pl_index)
    new_pl_index = new_pl_index + pl_index[:remaining_index]

    for j in np.arange(len(T)):
        if new_pl_index[j] == 1:
            print(str([0.00] * 34)[1:-1].replace(",", " "), file=output_f)

        fields = (
            int(year[j] - 2000),
            int(month[j]),
            int(day[j]),
            int(hour[j]),
            int(new_pl_index[j]),
            h[j],
            T[j],
            U[j],
            V[j],
            RH[j],
        )
        row_str = (
            "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
        )
        row_str = row_str.format(*fields)
        output_f.write(row_str + "\n")
    """


def run_in_paraller(function_name, file_list, gridstep, observatory=None, lat=None, lon=None):
    """
    Converts in parallel a list of grib files.
    :param function_name: The function to convert the grib files. It can be either read_grib_file_to_magic or
    read_grib_file_to_text
    :type function_name: string
    :param file_list: name of the file containing the list of grib files to process
    :type file_list: string
    :param gridstep: DAS  granularity - distance between the grid points where we have data from DAS
    :type gridstep: float
    :param observatory: The location of the observatory, north or south
    :type observatory: string
    :param lat: The geographical latitude of the observatory
    :type lat: float
    :param lon: The geographical longitude of the observatory
    :type lon: float
    """

    fname = open(file_list)
    line = fname.readline()
    list_of_gribfiles = []
    while line:
        list_of_gribfiles.append(line[:-1])
        line = fname.readline()

    p = multiprocessing.Pool()
    for grib_file in list_of_gribfiles:
        p.map(function_name, [grib_file, gridstep, observatory, lat, lon])

    p.close()
    p.join()


def merge_txt_from_grib(txtfile, output_file="merged_from_grib.txt"):
    """Merges text files created from different grib2 files to one text file"""
    # FIXME broken with ecsv, requires refactoring
    raise NotImplementedError("TXT merging requires discussion and refactoring. N/A at the moment")
    """

    lf = open(txtfile, "r")
    outfile = open(output_file, "w")

    line = lf.readline()
    first = True
    while line:
        datafile = open(line[:-1], "r")
        if first:
            dataline = datafile.readline()
        else:
            datafile.readline()
            dataline = datafile.readline()

        while dataline:
            print(dataline[:-1], file=outfile)
            dataline = datafile.readline()
        first = False
        datafile.close()
        line = lf.readline()
    lf.close()
    outfile.close()
    """
