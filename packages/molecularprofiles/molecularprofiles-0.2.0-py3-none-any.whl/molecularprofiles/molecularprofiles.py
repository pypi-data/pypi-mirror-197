"""
This is a class that offers a set of functions to work with meteorological data
in txt table format, separated with spaces.

It makes use of the pandas dataframe objects in order to be more efficient


Created by Pere Munar-Adrover
email: pere.munaradrover@gmail.com

"""

import os
import sys
import logging

from astropy.table import Table
import numpy as np
from scipy.interpolate import interp1d

from molecularprofiles.utils.grib_utils import get_grib_file_data, extend_grib_data
from molecularprofiles.utils.constants import DENSITY_SCALE_HEIGHT
from molecularprofiles.utils.dataframe_ops import (
    compute_averages_std,
    avg_std_dataframe,
)
from molecularprofiles.utils.humidity import (
    compressibility,
    density_moist_air,
    molar_fraction_water_vapor,
    partial_pressure_water_vapor,
)
from molecularprofiles.utils.rayleigh import Rayleigh

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/utils/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MolecularProfile:
    """
    This class provides a series of functions to analyze the quality of the data for both
    CTA-North and CTA-South.

    Methods within this class:

    get_data:                   it retrieves the data from the input file. If the input file
                                is a grib file and there is no file in the working directory
                                with the same name but with .txt extension the program extracts
                                the data from the grib file through the grib_utils program. If
                                there is such a txt file, it reads it directly
    write_corsika:              pints the data into a txt file which format is compliant with the input card
                                for the CORSIKA air shower simulation software
    """

    def __init__(self, data_file, data_server="server", observatory="north"):
        """
        Constructor

        :param data_file: txt file containing the data (string)
        :param data_server: label to be put in some of the output plots (string)
        :param observatory: valid options are: "north", "south", "other"

        """

        self.data_file = data_file
        self.data_server = data_server
        self.observatory = observatory

    # =============================================================================================================
    # Private functions
    # =============================================================================================================
    def _interpolate_simple(self, x_param, y_param, new_x_param):
        func = interp1d(x_param, y_param, kind="cubic", fill_value="extrapolate")
        return func(new_x_param)

    def _interpolate_param_to_h(self, param, height):
        interpolated_param = []
        group_mjd = self.dataframe.groupby("MJD")

        logger.info("Computing the extrapolation of the values of density:")
        logger.info("(This is to make it easier to compare ECMWF and GDAS, or any other")
        logger.info("weather model)")

        for mjd in self.dataframe.MJD.unique():
            h_at_mjd = group_mjd.get_group(mjd)["h"].tolist()
            param_at_mjd = group_mjd.get_group(mjd)[param].tolist()
            func = interp1d(h_at_mjd, param_at_mjd, kind="cubic", fill_value="extrapolate")

            if isinstance(height, int) or isinstance(height, float):
                interpolated_param.append(np.float(func(height)))
            else:
                interpolated_param.append(func(height))
        interpolated_param = np.array(interpolated_param)
        if isinstance(height, float) or isinstance(height, int):
            interpolated_param = np.array(interpolated_param)
            return interpolated_param
        else:
            interpolated_param_avgs = compute_averages_std(interpolated_param)
            return (
                interpolated_param,
                interpolated_param_avgs[0],
                interpolated_param_avgs[1],
                interpolated_param_avgs[2],
                interpolated_param_avgs[3],
            )

    def _compute_mass_density(self, air="moist", co2_concentration=415, interpolate=False):
        """
        Uses the functions density_moist_air, molar_fraction_water_vapor and compressibility
        from the LIDAR_analysis module humidity.py
        input:
            air: (str, optional) must be 'moist' or 'dry'

        :return: density [kg/m^3], std_dev(density) [kg/m^3], peak2peak_minus, peak2peak_plus
        """
        # C :  CO2 average global concentration in ppm taken from Keeling curve
        C = co2_concentration
        rho_s = 1.225  # kg/m^3 standard air mass density (sea level, 15 degrees C)
        rho = []

        for i in np.arange(len(self.dataframe.P)):
            if air == "moist":
                Xw = molar_fraction_water_vapor(
                    self.dataframe.P.iloc[i], self.dataframe.Temp.iloc[i], self.dataframe.RH.iloc[i]
                )
                Z = compressibility(self.dataframe.P.iloc[i], self.dataframe.Temp.iloc[i], Xw)
                rho.append(
                    density_moist_air(
                        self.dataframe.P.iloc[i] * 100.0, self.dataframe.Temp.iloc[i], Z, Xw, C
                    )
                )

            elif air == "dry":
                Z = compressibility(self.dataframe.P.iloc[i], self.dataframe.Temp.iloc[i], 0.0)
                rho.append(
                    density_moist_air(
                        self.dataframe.P.iloc[i] * 100.0, self.dataframe.Temp.iloc[i], Z, 0.0, C
                    )
                )
            else:
                logger.critical('Wrong air condition. It must be "moist" or "dry". Aborting!')
                sys.exit()

        self.dataframe["n_mass_" + air] = rho
        self.dataframe["nexp_mass_" + air] = (
            self.dataframe["n_mass_" + air]
            / rho_s
            * np.exp(self.dataframe.h / DENSITY_SCALE_HEIGHT)
        )

    def _compare_models(self, model_1, model_2):
        """
        Compares two atmospheric models and returns statistical difference between them
        """
        pass
        """
        Reference content of removed similar function:
        diff_with_magic = []
        diff_with_prod3 = []

        interpolated_density = self._interpolate_param_to_h("n_exp", self.x)[0]

        self._get_prod3sim_data()
        x = np.linspace(1000.0, 25000.0, num=15, endpoint=True)

        logger.info("Computing the differences of the values of density:")
        for i in np.arange(len(interpolated_density))):
            diff_with_magic.append(
                (interpolated_density[i] - self.func_magic(x)) / interpolated_density[i]
            )
            diff_with_prod3.append(
                (interpolated_density[i] - self.func_prod3(x)) / interpolated_density[i]
            )

        self.diff_with_magic = np.asarray(diff_with_magic)
        self.diff_with_prod3 = np.asarray(diff_with_prod3)
        logger.info("DIFF PROD3", self.diff_with_prod3)
        self.diff_MAGIC = compute_averages_std(self.diff_with_magic)
        self.diff_PROD3 = compute_averages_std(self.diff_with_prod3)
        """

    # =============================================================================================================
    # Main get data function
    # =============================================================================================================
    def get_data(
        self,
        select_good_weather=False,
        RH_lim=100.0,
        W_lim=10000.0,
        filter_by_density=False,
        n_exp_minvalue=0.0,
        n_exp_maxvalue=1.0,
    ):

        """
        Function that reads ECMWF or GDAS txt input files and returns quantities ready to plot.
        If the input filename does not exist, the program searches for the same
        input name with .grib extension and extracts the data from it

               select_good_weather: (bool) if True it uses RH_lim and W_lim parameters to filter the
                                    data by good weather conditions
               RH_lim: (float) if select_good_weather is True, this is the RH upper limit value to use
                       to filter the data
               W_lim: (float) if select_good_weather is True, this is the Wind speed upper limit value
                      to use to filter the data
               filter_by_density: (bool) if set to True it filters the data by density values instead of
                                  filtering by epoch

        :return:
            self.dataframe
            self.h_avgs
            self.n_avgs
            self.Temp_avgs
            self.wind_speed_avgs
            self.wind_direction_avgs
            self.RH_avgs
            self.n_exp_avgs
        """
        file_ext = os.path.splitext(self.data_file)[1]
        if file_ext == ".grib" or file_ext == ".grib2":
            data = get_grib_file_data(self.data_file)
            data = extend_grib_data(data)
        elif file_ext == ".ecsv":
            data = Table.read(self.data_file, format="ascii.ecsv")
        else:
            raise NotImplementedError(
                f"Only grib (1,2) and ecsv formats are supported at the moment. Requested format: {file_ext}"
            )

        self.dataframe = data.to_pandas()

        # Various averaged values obtained after filtering (if no filter, averages are made over the whole dataframe)
        self.group_by_p = self.dataframe.groupby("Pressure")
        self.h_avgs = avg_std_dataframe(self.group_by_p, "Altitude")
        self.n_avgs = avg_std_dataframe(self.group_by_p, "Density")
        self.Temp_avgs = avg_std_dataframe(self.group_by_p, "Temperature")
        self.wind_speed_avgs = avg_std_dataframe(self.group_by_p, "Wind Speed")
        self.wind_direction_avgs = avg_std_dataframe(self.group_by_p, "Wind Direction")
        self.RH_avgs = avg_std_dataframe(self.group_by_p, "Relative humidity")
        self.n_exp_avgs = avg_std_dataframe(self.group_by_p, "Exponential Density")

    def _refractive_index(self, P, T, RH, wavelength, C):
        """Wrapper for Rayleigh.calculate_n()."""
        rayleigh = Rayleigh(wavelength, C, P, T, RH)
        return rayleigh.refractive_index

    # =======================================================================================================
    # printing functions:
    # =======================================================================================================

    def write_corsika(self, outfile, co2_concentration):
        """
        Write an output file in the style of a CORSIKA atmospheric configuration file:

        alt (km)     rho (g/cm^3)   thick (g/cm^2)   (n-1)
        """
        mbar2gcm2 = 1.019716213  # conversion from mbar (pressure in SI) to g/cm^2 (pressure in cgs)
        # Loschmidt constant: number density of particles in an ideal gas at STP in m^-3
        N0 = 2.079153e25  # Na divided by molar mass of air: 0.0289644
        height = np.array(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,
                19.0,
                20.0,
                21.0,
                22.0,
                23.0,
                24.0,
                25.0,
                26.0,
            ]
        )

        with open(outfile, "w") as f:

            f.write("# Atmospheric Model ECMWF year/month/day   hour h\n")  # .format(**datedict))
            f.write(
                "#Col. #1          #2           #3            #4        [ #5 ]        [ #6 ]       [ # 7 ]\n"
            )
            f.write(
                "# Alt [km]    rho [g/cm^3] thick [g/cm^2]    n-1        T [k]       p [mbar]      pw / p\n"
            )

            density = self.n_avgs[0].sort_index(ascending=False).values
            density /= N0 * 1.0e-3
            P = self.dataframe.Pressure.unique()[::-1]

            # height = self.h_avgs[0].sort_index(ascending=False).values / 1.e3
            # Temp = self.Temp_avgs[0].sort_index(ascending=False).values
            # RH = self.RH_avgs[0].sort_index(ascending=False).values

            T0 = float(
                self._interpolate_simple(
                    self.h_avgs[0].sort_index(ascending=False).values / 1e3,
                    self.Temp_avgs[0].sort_index(ascending=False).values,
                    0.0,
                )
            )
            RH0 = float(
                self._interpolate_simple(
                    self.h_avgs[0].sort_index(ascending=False).values / 1e3,
                    self.RH_avgs[0].sort_index(ascending=False).values,
                    0.0,
                )
            )
            P0 = float(
                self._interpolate_simple(
                    self.h_avgs[0].sort_index(ascending=False).values / 1e3, P, 0.0
                )
            )
            density0 = float(
                self._interpolate_simple(
                    self.h_avgs[0].sort_index(ascending=False).values / 1e3, density, 0.0
                )
            )
            thick0 = P0 * mbar2gcm2

            pw0 = partial_pressure_water_vapor(T0, RH0) / P0

            Temp = self._interpolate_simple(
                self.h_avgs[0].sort_index(ascending=False).values / 1.0e3,
                self.Temp_avgs[0].sort_index(ascending=False).values,
                height,
            )
            RH = self._interpolate_simple(
                self.h_avgs[0].sort_index(ascending=False).values / 1.0e3,
                self.RH_avgs[0].sort_index(ascending=False).values,
                height,
            )
            RH[RH < 0.0] = 1.0e-4
            Pressure = self._interpolate_simple(
                self.h_avgs[0].sort_index(ascending=False).values / 1.0e3, P, height
            )
            density = self._interpolate_simple(
                self.h_avgs[0].sort_index(ascending=False).values / 1.0e3, density, height
            )
            thick = Pressure * mbar2gcm2
            pwp = partial_pressure_water_vapor(Temp, RH) / Pressure

            nm0 = self._refractive_index(P0, T0, RH0, 350.0, co2_concentration) - 1.0
            outdict = {
                "height": 0.000,
                "rho": density0,
                "thick": thick0,
                "nm1": nm0,
                "T": T0,
                "p": P0,
                "pw/p": pw0,
            }
            f.write(
                "  {height:7.3f}     {rho:5.5E}  {thick:5.5E}  {nm1:5.5E}  {T:5.5E}  {p:5.5E}  {pw/p:5.5E}\n".format(
                    **outdict
                )
            )

            for i in np.arange(len(height)):
                nm1 = (
                    self._refractive_index(Pressure[i], Temp[i], RH[i], 350, co2_concentration) - 1
                )

                outdict = {
                    "height": height[i],
                    "rho": density[i],
                    "thick": thick[i],
                    "nm1": nm1,
                    "T": Temp[i],
                    "p": Pressure[i],
                    "pw/p": pwp[i],
                }
                f.write(
                    "  {height:7.3f}     {rho:5.5E}  {thick:5.5E}  {nm1:5.5E}  {T:5.5E}  {p:5.5E}  {pw/p:5.5E}\n".format(
                        **outdict
                    )
                )

            # concatenate the dummy values of MagicWinter starting from 50.0 km
            f.write(
                "   27.000     2.96567e-05  1.96754e+01  6.84513e-06  223.70  1.90428e+01  0.00000e+00\n"
            )

            f.write(
                "   28.000     2.52913e-05  1.69341e+01  5.83752e-06  225.69  1.63842e+01  0.00000e+00\n"
            )

            f.write(
                "   29.000     2.15935e-05  1.45949e+01  4.98403e-06  227.75  1.41164e+01  0.00000e+00\n"
            )

            f.write(
                "   30.000     1.84554e-05  1.25967e+01  4.25972e-06  229.92  1.21798e+01  0.00000e+00\n"
            )

            f.write(
                "   32.000     1.35171e-05  9.42594e+00  3.11990e-06  234.75  9.10824e+00  0.00000e+00\n"
            )

            f.write(
                "   34.000     9.93769e-06  7.09977e+00  2.29374e-06  240.36  6.85638e+00  0.00000e+00\n"
            )

            f.write(
                "   36.000     7.35111e-06  5.38483e+00  1.69672e-06  246.30  5.19717e+00  0.00000e+00\n"
            )

            f.write(
                "   38.000     5.47808e-06  4.11190e+00  1.26441e-06  252.24  3.96630e+00  0.00000e+00\n"
            )

            f.write(
                "   40.000     4.11643e-06  3.15961e+00  9.50121e-07  257.79  3.04599e+00  0.00000e+00\n"
            )

            f.write(
                "   42.000     3.12126e-06  2.44097e+00  7.20424e-07  262.51  2.35189e+00  0.00000e+00\n"
            )

            f.write(
                "   44.000     2.38908e-06  1.89362e+00  5.51429e-07  265.91  1.82354e+00  0.00000e+00\n"
            )

            f.write(
                "   46.000     1.84598e-06  1.47276e+00  4.26075e-07  267.52  1.41753e+00  0.00000e+00\n"
            )

            f.write(
                "   48.000     1.43779e-06  1.14626e+00  3.31858e-07  267.20  1.10275e+00  0.00000e+00\n"
            )

            f.write(
                "   50.000     1.09738e-06  8.72656e-01   2.53289e-07   266.34   8.38955e-01  0.00000e+00\n"
            )
            f.write(
                "   55.000     5.99974e-07  4.61036e-01   1.38481e-07   257.19   4.42930e-01  0.00000e+00\n"
            )
            f.write(
                "   60.000     3.25544e-07  2.36175e-01   7.51395e-08   242.81   2.26896e-01  0.00000e+00\n"
            )
            f.write(
                "   65.000     1.70152e-07  1.15918e-01   3.92732e-08   227.93   1.11324e-01  0.00000e+00\n"
            )
            f.write(
                "   70.000     8.43368e-08  5.45084e-02   1.94660e-08   215.90   5.22651e-02  0.00000e+00\n"
            )
            f.write(
                "   75.000     3.95973e-08  2.48012e-02   9.13953e-09   208.66   2.37169e-02  0.00000e+00\n"
            )
            f.write(
                "   80.000     1.79635e-08  1.10899e-02   4.14618e-09   205.11   1.05760e-02  0.00000e+00\n"
            )
            f.write(
                "   85.000     8.03691e-09  4.91583e-03   1.85502e-09   202.12   4.66284e-03  0.00000e+00\n"
            )
            f.write(
                "   90.000     3.59602e-09  2.15599e-03   8.30003e-10   196.26   2.02583e-03  0.00000e+00\n"
            )
            f.write(
                "   95.000     1.59871e-09  9.21029e-04   3.69000e-10   187.55   8.60656e-04  0.00000e+00\n"
            )
            f.write(
                "  100.000     6.73608e-10  3.82814e-04   1.55477e-10   185.38   3.58448e-04  0.00000e+00\n"
            )
            f.write(
                "  105.000     2.69097e-10  1.61973e-04   6.21108e-11   197.19   1.52311e-04  0.00000e+00\n"
            )
            f.write(
                "  110.000     1.09021e-10  7.37110e-05   2.51634e-11   224.14   7.01416e-05  0.00000e+00\n"
            )
            f.write(
                "  115.000     4.71300e-11  3.70559e-05   1.08782e-11   268.51   3.63251e-05  0.00000e+00\n"
            )
            f.write(
                "  120.000     2.23479e-11  2.05900e-05   5.15817e-12   333.43   2.13890e-05  0.00000e+00\n"
            )

    def create_mdp(self, mdp_file):
        """
        Write an output file with the molecular number density per height
        """

        height = np.arange(
            1.0, 27.0, 1
        )  # FIXME: The hardcoded value 27 reflects the current ceiling of GDAS data (26km a.s.l.). Shouldn't be hardcoded and in general the binning and limits should be considered.
        with open(mdp_file, "w") as f:

            number_density_exp = self._interpolate_simple(
                self.h_avgs[0].sort_index(ascending=False).values / 1.0e3,
                self.n_exp_avgs[0].sort_index(ascending=False).values,
                height,
            )

            for i in np.arange(len(height)):
                file_line = [str(height[i]), "\t", str(number_density_exp[i]), "\n"]
                f.writelines(file_line)
