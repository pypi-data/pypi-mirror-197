"""
Module containing functionality allows to get observatory's coordinates
and select meteorological data depending on the season for the South and North hemisphere

"""

import math
import logging
import os
from datetime import date, timedelta
from calendar import monthrange, month_abbr
import numpy as np

import astropy.units as u
from astropy.coordinates import angular_separation, Longitude, Latitude


ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Season:
    """
    Class, describing nature seasons.
    """

    def __init__(self, name, start_month, stop_month, start_day=None, stop_day=None):
        """
        Initialize Season object with the name and start/stop dates.

        Parameters
        ----------
        name : str
            Season name
        start_month : int
            Index of start month
        stop_month: int
            Index of stop month
        start_day : [Optional] int
            Start day of the month (optional, defaults to 1)
        stop_day : [Optional] int
            Stop day of the month (optional, defaults to last day of the stop month)
        """
        self._leap_year = (
            2000  # Arbitrary leap year. Do not change unless you know what you're doing.
        )
        self._name = name.upper()
        start = date(year=self._leap_year, month=start_month, day=start_day or 1)
        stop = date(
            year=self._leap_year,
            month=stop_month,
            day=stop_day or monthrange(self._leap_year, stop_month)[1],
        )
        if start > stop:
            logger.warning(
                "Seasons's start date is greater than its stop date, "
                "rolling back start date year..."
            )
            try:
                start = start.replace(year=start.year - 1)
            except ValueError:
                logger.warning("29/02 is used as the season start date, changing it to 28/02...")
                start = start.replace(year=start.year - 1, day=start.day - 1)
            self._months = list(range(start_month, 13)) + list(range(1, stop_month + 1))
            self._carry_on = True
        else:
            self._months = list(range(start_month, stop_month + 1))
            self._carry_on = False
        self._start = start
        self._stop = stop

    def __contains__(self, timestamp):
        cast_date = timestamp.replace(year=self._leap_year)
        if self._carry_on:
            return (
                self._start <= cast_date.replace(year=self._leap_year - 1)
                or cast_date <= self._stop
            )
        return self._start <= cast_date <= self._stop

    def __repr__(self):
        return (
            f"Season {self.name}: "
            f"from {month_abbr[self.start[0]]}, {self.start[1]} "
            f"to {month_abbr[self.stop[0]]}, {self.stop[1]}."
        )

    @property
    def name(self):
        """
        Season's name
        """
        return self._name

    @property
    def start(self):
        """
        Start of the season.

        Returns
        -------
        tuple(int, int)
            Season start (month, day)
        """
        return (self._start.month, self._start.day)

    @property
    def stop(self):
        """
        End of the season.

        Returns
        -------
        tuple(int, int)
            Season stop (month, day)
        """
        return (self._stop.month, self._stop.day)

    @property
    def months(self):
        """
        List of months in the season

        Returns
        -------
        list(int)
            List of month numbers in the season.
        """
        return self._months

    @property
    def reference_dates(self):
        """
        Reference season start and stop dates based on internal leap year.

        Returns
        -------
        tuple(date, date)
            Tuple of datetime.date objects (start, stop)
        """
        return (self._start, self._stop)


class Observatory:
    """
    Class, defining observatory object.
    """

    def __init__(self, name, lon, lat, seasons):
        """
        Parameters
        ----------
        name : str
            Observatory name.
        lon : astropy.coordinates.Longitude
            Observatory longitude.
        lat : astropy.coordinates.Latitude
            Observatory latitude.
        seasons : list(Season)
            List of observatory seasons.
        """
        self._name = name
        self._longitude = lon
        self._latitude = lat
        self._seasons = seasons
        self.__check_seasons()

    def __check_seasons(self):
        """
        Check if provided seasons provide no-gaps and no-overlaps full coverage of a year.

        Raises
        ------
        ValueError
            If the seasons overlap, if there's a gap between the seasons or they don't cover a year.
        """
        dates = sorted([season.reference_dates for season in self.seasons], key=lambda x: x[0])
        # check that there's one year between the first start and last end
        if dates[0][0] + timedelta(days=365) != dates[-1][1]:
            raise ValueError("The seasons don't cover a year")
        diffs = [j[0] - i[1] for i, j in zip(dates[:-1], dates[1:])]
        if not all(x == timedelta(days=1) for x in diffs):
            raise ValueError("The season coverage has gaps or overlaps!")

    @property
    def name(self):
        """
        Returns
        -------
        str
            Observatory's name
        """
        return self._name

    @property
    def coordinates(self):
        """
        Returns
        -------
        astropy.coordinates.Longitude
            Observatory's longitude
        astropy.coordinates.Latitude
            Observatory's latitude
        """
        return self._longitude, self._latitude

    @property
    def seasons(self):
        """
        Returns
        -------
        list(str)
            List of season names
        """
        return [season.name for season in self._seasons]

    def get_near_gridpoints(self, gridstep=1):
        """
        Get closest meteorological data point and a grid box, surrounding the observatory.

        The interpolation grids of the meteorological systems is assumed to start at (0,0) and be defined w.r.t. WGS84.

        Parameters
        ----------
        gridstep : float
            Meteorological data collection system grid step in degrees.

        Returns
        -------
        nearest_grid_point : tuple(float, float)
            Longitude and latitude of the nearest grid point.
        box_coordinates : list(tuple(float, float))
            List of coorinates (longitude, latitude) of four grid points forming a box around the observatory location.
        """
        box_coordinates = [
            (
                math.floor(self._longitude / gridstep) * gridstep,
                math.floor(self._latitude / gridstep) * gridstep,
            ),
            (
                (math.floor(self._longitude / gridstep) + 1) * gridstep,
                math.floor(self._latitude / gridstep) * gridstep,
            ),
            (
                math.floor(self._longitude / gridstep) * gridstep,
                (math.floor(self._latitude / gridstep) + 1) * gridstep,
            ),
            (
                (math.floor(self._longitude / gridstep) + 1) * gridstep,
                (math.floor(self._latitude / gridstep) + 1) * gridstep,
            ),
        ]

        distances = [
            angular_separation(self._longitude, self._latitude, *grid_point)
            for grid_point in box_coordinates
        ]

        nearest_grid_point = box_coordinates[np.argmin(distances)]

        return nearest_grid_point, box_coordinates

    def select_season_data(self, data, season_name):
        """
        Select data that belongs to a given season.

        Parameters
        ----------
        data : pandas.DataFrame with atmospheric data. Must contain column
        """
        if season_name.upper() not in self.seasons:
            logger.error(
                "Requested season (%s) is not defined for the observatory %s\n" "%s's seasons:\n%s",
                season_name,
                self.name,
                self.name,
                self.seasons,
            )
            raise RuntimeError(f"{season_name} is not present in {self.name}'s seasons.")
        return data.loc[
            data.apply(
                lambda x: date(year=int(x.year), month=int(x.month), day=int(x.day))
                in self.seasons[season_name.upper()],
                axis=1,
            )
        ]


# Define commonly used seasons and observatories

cta_north_winter = Season(name="cta-north-winter", start_month=11, stop_month=4, start_day=16)
cta_north_spring = Season(
    name="cta-north-spring", start_month=5, stop_month=6, start_day=1, stop_day=20
)
cta_north_summer = Season(
    name="cta-north-summer", start_month=6, stop_month=10, start_day=21, stop_day=4
)
cta_north_fall = Season(
    name="cta-north-fall", start_month=10, stop_month=11, start_day=5, stop_day=15
)
cta_south_winter = Season(
    name="cta-south-winter", start_month=5, stop_month=10, start_day=16, stop_day=14
)
cta_south_summer = Season(
    name="cta-south-summer", start_month=10, stop_month=5, start_day=15, stop_day=15
)

cta_north = Observatory(
    name="CTA North Site",
    lon=Longitude(angle=(-17, 53, 26.525), unit=u.deg, wrap_angle=180 * u.deg),
    lat=Latitude(angle=(28, 45, 42.462), unit=u.deg),
    seasons=[cta_north_spring, cta_north_summer, cta_north_fall, cta_north_winter],
)
cta_south = Observatory(
    name="CTA South Site",
    lon=Longitude(angle=(-24, 40, 24.8448), unit=u.deg, wrap_angle=180 * u.deg),
    lat=Latitude(angle=(-70, 18, 58.4712), unit=u.deg),
    seasons=[cta_south_summer, cta_south_winter],
)
