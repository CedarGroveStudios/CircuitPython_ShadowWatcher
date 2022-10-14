# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_shadowwatcher`
================================================================================

A CircuitPython helper class to detect a shadow cast over an analog light sensor
such as the ALS-PT19 phototransistor.

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

* Analog light sensor hardware such as the ALS-PT19 phototransistor with an
output value directly in proportion to the light intensity.

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import time
from analogio import AnalogIn

__version__ = "0.0.0+auto.0"
__repo__ = (
    "https://github.com/CedarGroveStudios/CircuitPython_ShadowWatcher.git"
)


class ShadowWatcher:
    """A CircuitPython class to detect a shadow cast over an analog light sensor
    such as the ALS-PT19 phototransistor used in the Adafruit PyPortal, PyGamer,
    PyBadge, CircuitPlayground Express, CircuitPlayground Bluefruit, and the
    ALS-PT19 breakout board. Incorporates a low-pass filter to reduce
    sensitivity to flickering light levels which may be caused by power line
    frequency or light dimmer PWM passthrough.
    Useful as a simple gesture detector."""

    # pylint: disable=too-many-arguments
    def __init__(self, pin, threshold=0.9, samples=2000, decay=0.01, auto=False):
        """Class initializer. Instantiate the light sensor input and measure the
        initial background light level.

        :param board.pin pin: The analog input pin that connects to the light sensor.
        :param float threshold: The relative brightness threshold for shadow
          detection. Defaults to 0.9, 90% of the foreground-to-background
          brightness ratio. Range is 0.0 to 1.0.
        :param int samples: The number of samples needed for the _read method's
          low-pass filter. Default is 2000 for a cut-off frequency of
          approximately 25Hz when using a SAMD-51 (M4) clocked at 120MHz. Range
          is any positive non-zero integer value.
        :param float decay: The magnitude of the foreground-induced decay used to
          continuously adjust the background value each time the foreground
          value is read. The decay compensates for slowly changing background
          light levels. Default is 0.01, equivalent to a weight of 1 foreground
          sample per 99 background samples. Range is 0.0 to 1.0.
        :param bool auto: Enables automatic samples detection when True. If
          enabled, the samples parameter is replaced with a calculated value
          based upon measured acquisition time. This preserves the low-pass
          filter's cutoff frequency regardless of variations in microcontroller
          ADC latency. Defaults to False."""

        self._light_sensor = AnalogIn(pin)
        self._brightness_threshold = threshold
        self._decay = max(min(decay, 1.0), 0.0)
        self._auto = auto

        self._foreground = 0
        self._background = 0

        if self._auto:
            # Calculate sample interval for cutoff frequency
            cutoff_frequency = 25  # Hz
            samples_interval = 1 / (cutoff_frequency / 2)

            # List of number of samples to test
            test_samples = [1e3, 1e4]
            test_delays = []

            # Record elapsed time for each test
            for self._samples in test_samples:
                start_time = time.monotonic()
                self.refresh_background()
                test_delays.append(time.monotonic() - start_time)

            # Use slope intercept form to determine number of samples
            slope = (test_samples[1] - test_samples[0]) / (
                test_delays[1] - test_delays[0]
            )
            y_intercept = test_samples[1] - (slope * test_delays[1])
            # Apply slope, intercept; constrain sample value range from 1 to 100k
            self._samples = min(
                max(int((slope * samples_interval) + y_intercept), 1), 1e5
            )
        else:
            # Use samples parameter if auto=False
            self._samples = samples
        self.refresh_background()

    @property
    def background(self):
        """The most recent background measurement. Range is 0 to 65535. A value
        of 65535 is approximately 1100 Lux."""
        return self._background

    @property
    def foreground(self):
        """The most recent foreground measurement. Range is 0 to 65535. A value
        of 65535 is approximately 1100 Lux."""
        return self._foreground

    def _read(self):
        """Read and filter sensor level using a simple simple n-order finite
        impulse response (FIR) moving-average (boxcar) low-pass filter."""
        measurement = 0
        for _ in range(self._samples):
            measurement = measurement + (self._light_sensor.value / self._samples)
        return measurement

    def _get_foreground(self):
        """Read the filtered foreground sensor level and fractionally adjust the
        background level per the decay setting."""
        self._foreground = self._read()
        self._background = ((1.0 - self._decay) * self._background) + (
            self._decay * self._foreground
        )

    def refresh_background(self):
        """Read and update the filtered background sensor level."""
        self._background = self._read()

    def detect(self):
        """The fundamental ShadowWatcher function. Compares foreground to
        background light levels to detect a shadow. The function uses two
        thresholds, a lower one that indicates a shadow and an upper threshold
        that when exceeded, indicates an increased background light level.
        Returns True when the ratio of foreground to background is less than the
        threshold. A non-blocking method."""

        self._get_foreground()
        brightness_ratio = self._foreground / self._background
        if brightness_ratio < self._brightness_threshold:
            # Shadow detected; brightness ratio is less than threshold
            return True
        if brightness_ratio > 2 - self._brightness_threshold:
            # Background light level increased; refresh background measurement
            self.refresh_background()
        return False
