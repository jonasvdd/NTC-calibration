# NTC calibration

# [🍾 documentation](https://jonasvdd.github.io/NTC-calibration/)

## Table of contents

* [Introduction](#introduction)
* [Running the application](#running-it)
* [Other methods to retrieve the voltage from the ADC signal](#other-method-to-retrieve-the-voltage-from-the-adc-signal)
* [Calibration results](#calibration-results)
* [Contributing](#contributing)


## Introduction

Makes use of the [**Steinhart-Hart**](https://www.wikiwand.com/en/Steinhart%E2%80%93Hart_equation) equation to calibrate thermistors. This is achieved by:

* Retrieving an analog to digital converted signal via an microcontroller, This value stands in relation with the resistance of the micro controller.
* Fetching the resistance of the [Thorlabs TSP01]() temperature logger.

Afterwards, these values are feeded into the [Steinhart-Hart class](desktop/SteinhartHart.py) and will be used to calibrate the coefficients.

## Running it

Make sure that you've installed the requirements

```bash
pip install -r desktop/requirements.txt
```

Just run with your python3 interpreter:
```
python main.py
```

>**NOTE**: Some users will not be able to detect the torlabs TSP01 sensor, this can be caused by:
> * Not having the [pyusb](https://pypi.org/project/pyusb/) library installed (see link for install instructions)
> * The current user on you desktop is not able to see the devices
>   * Try adding your current user to the dialout group
>   * run [main.py](desktop/main.py) with superuser permissions


## Other method to retrieve the voltage from the ADC signal

If your circuit doesn't make use of a (simple) voltage devider, you will need another conversion method. This can be achieved by: **Creating a method in [config.py](desktop/config.py)**

## Calibration results

Al the values (reference temperature, ntc_resistor value, predicted temperature, the coefficients, ...) will be stored in a .csv file.
This can be used in e.g. Jupyter Notebook to analyse the quality of the calibration.

The succeeding table gives an overview which data elements are stored


RNTC | Tprobe | Tcalc | A | B | C | T1 | R1 | T2 | R2 | T3| R3
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
Ω | °C | °C | \ | \ | \ | °C | Ω | °C | Ω | °C | Ω

Column | description
|:--:|:--|
RNTC | The calculated resistance (via the retrieved ADC value) of the thermistor
Tprobe | The temperature of the TSP01 temperature probe
Tcalc | The calculated temperature of the termistor, based on RNTC and the Steinhart-Hart coefficients
A | Steinhart-Hart coefficient A 
B | Steinhart-Hart coefficient B
C | Steinhart-Hart coefficient C
T1 | The first reference temperature used for calculating the coefficients
R1 | The first resistance used to calculate the Steinhart-Hart coefficients
T2 | The second reference temperature used for calculating the coefficients
R2 | The second resistance used to calculate the Steinhart-Hart coefficients
T3 | The third reference temperature used for calculating the coefficients
R3 | The third resistance used to calculate the Steinhart-Hart coefficients

## Contributing
If you have some amazing ideas, just create a pull request `¯\_(ツ)_/¯`. 
