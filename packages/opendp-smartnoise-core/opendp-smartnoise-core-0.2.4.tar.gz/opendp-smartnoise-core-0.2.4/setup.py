from setuptools import setup
import sys
import warnings

warnings.warn('SmartNoise-Core is deprecated. Please migrate to the OpenDP library: https://github.com/opendp/opendp, https://docs.opendp.org', DeprecationWarning)

deprecated_msg = '''
-----------------------------------
*** Deprecated ***
-----------------------------------

The SmartNoise Core package is deprecated. 

Please migrate to the OpenDP library:

Repository: https://pypi.org/project/opendp
Documentation: https://docs.opendp.org
PyPI package: https://pypi.org/project/opendp

-----------------------------------
'''

# Bad hack so package fails on install
from datetime import datetime
deprecated_day = datetime(year=2023, month=3, day=13, hour=14, minute=40)
if datetime.now() > deprecated_day:
    sys.exit(deprecated_msg)

setup()



"""
setup(
    extras_require={
        "plotting": [
            "networkx",
            "matplotlib"
        ],
        "test": [
            "pytest>=4.4.2",
            "pandas>=1.0.3"
        ]
    },
    package_data={
        "opendp.smartnoise": [
            os.path.join("core", "lib", filename) for filename in [
                "smartnoise_ffi.dll",
                "libsmartnoise_ffi.so",
                "libsmartnoise_ffi.dylib",
            ]
        ]
    }
)
"""
