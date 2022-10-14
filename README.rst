Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_ShadowWatcher/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_ShadowWatcher/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython helper class to detect a shadow cast over an analog light sensor
such as the ALS-PT19 phototransistor.

ShadowWatcher is a CircuitPython helper class to detect a shadow cast over an
analog light sensor such as the ALS-PT19 phototransistor used in the Adafruit
PyPortal, PyGamer, PyBadge, CircuitPlayground Express, CircuitPlayground
Bluefruit, and the ALS-PT19 breakout board. Incorporates a low-pass filter to
reduce sensitivity to flickering light levels which may be caused by power line
frequency or light dimmer PWM passthrough. Useful as a simple gesture detector.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

* Analog light sensor hardware such as the ALS-PT19 phototransistor with an output value directly in proportion to the light intensity.

The ShadowWatcher was primarily built for and tested on the PyPortal, but
should be able to function reliably on other microcontrollers with similar
sensors. The automatic samples mode will test the microcontroller's analog
acquision latency and adjust the internal low-pass filter's sample size to
maintain the ~25 Hz cutoff frequency.

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_shadowwatcher

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import board
    import time
    from shadowwatcher import ShadowWatcher
    # Instantiate detector class and establish background level
    gesture = ShadowWatcher(pin=board.LIGHT, auto=True)
    while True:
        if gesture.detect():
            print(f"SHADOW DETECTED")
            while gesture.detect():
                # Wait until the shadow is gone
                time.sleep(1)
            # Rebaseline the background level
            gesture.refresh_background()
            print(f"background: {gesture.background:6.0f}")

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://github.com/CedarGroveStudios/CircuitPython_ShadowWatcher/blob/main/media/pseudo_readthedocs_shadowwatcher.pdf>`_.

The ShadowWatcher helper class was tested on the PyPortal, but should be able to
function reliably on other microcontrollers with similar sensors. The automatic
samples mode will test the microcontroller's analog acquisition latency and
adjust the internal low-pass filter's sample size to maintain the ~25 Hz cutoff
frequency.

The left oscilloscope image shows the sampled sensor light level value in a room
with a dimmed LED light source (yellow trace). Note that the primary frequency
of the signal is 120Hz (purple frequency spectrum graph). The right image shows
the sampled sensor light level value after filtering.

.. image:: https://github.com/CedarGroveStudios/CircuitPython_ShadowWatcher/blob/main/media/FIR_boxcar_filter_pyportal.png

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_ShadowWatcher/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
