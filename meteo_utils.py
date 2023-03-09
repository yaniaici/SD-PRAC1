import random
import time

from numpy import linspace, searchsorted
from scipy.stats import norm

# Approximated realistic ranges for air condition parameters
MIN_TEMPERATURE = -10
MAX_TEMPERATURE = 45
MIN_CO2 = 300
MAX_CO2 = 500
MIN_HUMIDITY = 20
MAX_HUMIDITY = 70

# Approximated optimal values for air condition parameters
OPTIMAL_TEMPERATURE = 20
OPTIMAL_CO2 = 400
OPTIMAL_HUMIDITY = 40


MIN_PROCESS_TIME = 0.5
MAX_PROCESS_TIME = 3.5


class MeteoDataDetector:
    """
    Simulates an air conditions detector.
    Detects temperature, co2 concentration and humidity percentage.

    ...

    Attributes
    ----------
    min_temperature : float
        minimum temperature returnable by the detector (ºC)
    max_temperature : float
        maximum temperature returnable by the detector (ºC)
    min_co2 : float
        minimum co2 concentration returnable by the detector (ppm)
    max_co2 : float
        maximum co2 concentration returnable by the detector (ppm)
    min_humidity : float
        minimum humidity percentage returnable by the detector (%)
    max_humidity : float
        maximum humidity percentage returnable by the detector (%)
    """

    def __init__(self):
        """
        Initializes the detector with random ranges for air condition parameters.
        """

        temperature_range = [random.uniform(MIN_TEMPERATURE, MAX_TEMPERATURE) for _ in range(2)]
        self.min_temperature = min(temperature_range)
        self.max_temperature = max(temperature_range)

        co2_range = [random.uniform(MIN_CO2, MAX_CO2) for _ in range(2)]
        self.min_co2 = min(co2_range)
        self.max_co2 = max(co2_range)

        humidity_range = [random.uniform(MIN_HUMIDITY, MAX_HUMIDITY) for _ in range(2)]
        self.min_humidity = min(humidity_range)
        self.max_humidity = max(humidity_range)

    def gen_temperature(self):
        """
        Returns a random temperature value within the detectors range.
        :return: a temperature value.
        """
        return round(random.uniform(self.min_temperature, self.max_temperature), 2)

    def gen_co2(self):
        """
        Returns a random co2 concentration value within the detectors range.
        :return: a co2 concentration value.
        """
        return round(random.uniform(self.min_co2, self.max_co2), 2)

    def gen_humidity(self):
        """
        Returns a random humidity percentage value within the detectors range.
        :return: a humidity percentage value.
        """
        return round(random.uniform(self.min_humidity, self.max_humidity), 2)

    def analyze_air(self):
        """
        Returns random air condition parameter values within the detector's ranges.
        :return: { "temperature" : t (float), "humidity" : h (float) }
        """
        return {
            "temperature": self.gen_temperature(),
            "humidity": self.gen_humidity()
        }

    def analyze_pollution(self):
        """
        Returns random air condition parameter values within the detector's ranges.
        :return: { "co2" : c (float) }
        """
        return { "co2": self.gen_co2() }


class MeteoDataProcessor:
    """
        Simulates an air wellness calculator.
        Calculates the overall wellness of the air based on temperature, co2 concentration and humidity percentage.
        For wellness calculation, it projects each air condition parameter into a skewed gaussian distribution of
        their accepted ranges of values, centered in their respective optimal value.

        ...

        Attributes
        ----------
        temperature_space : list
            1000 equidistant values covering the accepted temperature range.
        temperature_vals : list
            Normalize wellness values for each of the temperature space values.
        co2_space : list
            1000 equidistant values covering the accepted co2 concentration range.
        co2_vals : list
            Normalize wellness values for each of the co2 space values.
        humidity_space : list
            1000 equidistant values covering the accepted humidity concentration range.
        humidity_vals : list
            Normalize wellness values for each of the humidity space values.
        """

    def __init__(self):
        """
        Initializes distributions (space and values) for each of the air wellness parameters (temperature,
        co2 concentration and humidity percentage).
        """

        self.temperature_space, self.temperature_vals = _gen_distribution(MIN_TEMPERATURE, MAX_TEMPERATURE,
                                                                          OPTIMAL_TEMPERATURE)
        self.co2_space, self.co2_vals = _gen_distribution(MIN_CO2, MAX_CO2, OPTIMAL_CO2)
        self.humidity_space, self.humidity_vals = _gen_distribution(MIN_HUMIDITY, MAX_HUMIDITY, OPTIMAL_HUMIDITY)

    def process_meteo_data(self, meteo_data):
        """
        Processes meteorological data parameters (temperature, and humidity percentage) to return
        an air wellness value.
        Air wellness is calculated as the harmonic mean of the wellness values of the two parameters.
        :param meteo_data: a class with the attributes "temperature", and "humidity" and
        their respective values within the accepted ranges.
        """


        # Get the wellness value of each parameter based on the processor's distributions.
        temperature_wellness = _value_from_distribution(self.temperature_space, self.temperature_vals,
                                                        meteo_data.temperature)
        humidity_wellness = _value_from_distribution(self.humidity_space, self.humidity_vals, meteo_data.humidity)

        # Harmonic mean
        air_wellness = round(2 / (1 / temperature_wellness + 1 / humidity_wellness), 2)

        self._simulate_execution_time()

        return air_wellness

    def process_pollution_data(self, pollution_data):
        """
        Processes a co2 quantification to return an air pollution value.
        :param meteo_data: a class with the attribute "co2" and its respective value within the accepted ranges.
        """

        co2_wellness = _value_from_distribution(self.co2_space, self.co2_vals, pollution_data.co2)

        co2_wellness = round(co2_wellness, 2)

        self._simulate_execution_time()

        return co2_wellness


    def _simulate_execution_time(self):
        time.sleep(random.uniform(MIN_PROCESS_TIME, MAX_PROCESS_TIME))



def _gen_distribution(min_val, max_val, opt_val):
    """
    Generate a skewed gaussian distribution.
    :param min_val: lower limit of the space.
    :param max_val: upper limit of the space.
    :param opt_val: center of the space.
    :return: list of equidistant values within the space, probabilities of each of the values in the distribution
    """

    location = opt_val
    scale = _get_scale(min_val, max_val)
    x = linspace(min_val, max_val, 1000)

    p = _skew_norm_pdf(x, location, scale)

    return x, _normalize_data(p)


def _skew_norm_pdf(x, center, scale):
    """
    Generates a skewed gaussian distribution based on values x, centered on l and scale s.
    :param x: linear space for the distribution.
    :param center: center of the skewed distribution.
    :param scale: scale of the distribution.
    :return: frequencies for the skewed gaussian distribution in space x.
    """
    t = (x - center) / scale
    return 2.0 * center * norm.pdf(t) * 0.5


def _get_scale(min_val, max_val):
    """
    Calculate the scale of a distribution based on its minimum and maximum values.
    (parameters have been adjusted empirically for the use case).
    :param min_val: lower limit of the space.
    :param max_val: upper limit for the space.
    :return: scale of the distribution.
    """
    scale = ((max_val - min_val) / 25) * 8
    return scale


def _normalize_data(data):
    """
    Normalize a list of values to their range.
    :param data: list of values.
    :return: normalized values for data.
    """
    min_val = min(data)
    max_val = max(data)
    return [(d - min_val) / (max_val - min_val) for d in data]


def _value_from_distribution(space, values, x):
    """
    Get the probability of a certain position in a distribution.
    :param space: list of equidistant values within the space of the distribution.
    :param space: list of probabilities for each of the entries in the space.
    :param x: a value within the space of the distribution.
    :return: probability of value x in the distribution.
    """
    position = searchsorted(space, [x])[0]
    if position == len(space):
        position -= 1
    value = values[position]
    if value == 0:
        value = 0.001
    return value
