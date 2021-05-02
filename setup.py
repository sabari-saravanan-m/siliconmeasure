from setuptools import setup
setup(name='siliconmeasure',
version='0.1.1',
description='Installation Package of Agilent, Keysight, Chroma, Keithley, Tektronix',
url='#',
author='SABARI SARAVANAN M',
author_email='saravana.braven@gmail.com',
license='SN',
packages=["siliconmeasure.Agilent", "siliconmeasure.Chroma",
          "siliconmeasure.Keithley", "siliconmeasure.Keysight",
          "siliconmeasure.Tektronix"
          ],
zip_safe=False)
