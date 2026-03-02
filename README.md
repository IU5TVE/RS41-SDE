# RS41-SDE Serial Data Extractor
RS41-SDE is a script developed as part of the LuniSpace project, a school initiative that aims to launch weather radiosondes alongside real-time image transmission systems, as a simple solution to a practical need: obtaining and managing data from a radiosonde. It was created as part of a larger script that will be published shortly on my GitHub profile. 

This is a basic but functional tool that allows you to extract meteorological data serially from the radiosonde via a USB TTL adapter.

The code is deliberately basic, lightweight and easy to understand: its purpose is not to process or analyse the data, but to reliably perform the fundamental task of acquiring it. In other words, it simply extracts altitude, temperature, humidity and atmospheric pressure from the radiosonde and makes them available to the user, who can then manage, analyse or integrate them into other projects according to their needs.

# Requirements and Installation
The script is written in Python, so you need to verify that Python is installed on your system by running the command:
```bash
python --version
```
If Python is not installed, you will need to download and install it from the official website: https://www.python.org/downloads/
#
Next, you need to install the `pip` library, Python's package manager, because it allows you to easily add all the necessary external libraries. In this case, in the next step, we will install “pyserial.” You can download it and find installation instructions here: https://pip.pypa.io/en/stable/installation/
#
Next, you need to install the `pyserial` library, which allows the script to communicate with the radiosonde via the serial port. To install it, run the command:
```bash
pip install pyserial
```

# How to use
![](img/settings.png)

The image shows the first lines of the script, where you can configure some settings. Here you can choose whether to save the extracted data to a .txt file, set the output file path, and enter the serial communication port of the USB-TTL adapter.
