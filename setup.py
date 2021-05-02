from setuptools import setup
setup(name='siliconmeasure',
version='0.1.1',
description='Installation Package of NI-USB8452, Agilent-E3631A, Keysight, Chroma, Keithley, Tektronix, TI',
url='#',
author='SABARI SARAVANAN M',
author_email='saravana.braven@gmail.com',
license='SN',
packages=["siliconmeasure.Agilent", "siliconmeasure.Chroma",
          "siliconmeasure.Keithley", "siliconmeasure.Keysight",
          "siliconmeasure.NI8452", "siliconmeasure.Tektronix",
          "siliconmeasure.TI"
          ],
zip_safe=False)
