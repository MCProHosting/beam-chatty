# beam-client-python [![](https://badges.gitter.im/WatchBeam/beam.png)](https://gitter.im/WatchBeam/developers)

This is a basic chat bot framework for Beam, built to serve as a basic example of a Beam chat bot.

## Usage

We've built a chat bot that logs incoming messages to the console, no longer sends "Hi!" to the channel every second.
!ping command has been added

To use it, ensure Python 3 is installed on your system. Then:

* install dependencies
  * Windows : `python setup.py install`
  * Linux   : `python3 setup.py install`
* copy `config.example.py` to `config.py` and add your authentication information
* run the example chatbot 
  * Windows : Launch `run.bat` (fixes issues with certain font types)
  * Linux   : `python3 example.py`

 ## Tested Platforms
 
* Windows 10 with Python 3.4.2
* Rasbian with Python 3.4.2 (Raspberry Pi)
* Ubuntu 16.04 LTS with Python 3.5.2
