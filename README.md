# Siliconmeasure Package

![siliconmeasure]https://github.com/sabari-saravanan-m/siliconmeasure

Siliconmeasure makes easy to set up and run. The package contains a repository of instrument classes and a system for running experiment procedures.
It is currently under active development, so please report any issues you experience to this Issues page.

Siliconmeasure runs on Python 3.6, 3.7, 3.8 and 3.9, and is tested with continous-integration Windows.


## Install

```bash
$ pip install C:\..\Downloads\siliconmeasure
```

## Simple Demo

```python
from siliconmeasure.Agilent import agilentE3631A
from siliconmeasure.Keysight import keysight34461A
from siliconmeasure.Tektronix import tektronixMSO4000B
from siliconmeasure.NI8452 import i2c, spi, spistream, dio
from siliconmeasure.Chroma import chroma6314A
from siliconmeasure.Keithley import keithley2200, keithleyN6700

agilent = agilentE3631A.AgilentE3631A()
agilent.open("")
agilent.close()
```

## Development

### Contributing

Long-term discussion and bug reports are maintained via GitHub Issues.
Code review is done via GitHub Pull Requests.
