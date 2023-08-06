from setuptools import setup

def readme():
    with open(r"C:\Users\grewa\Desktop\ \UCS654\Topsis-Harjot-102017126\README.md") as f:
        README = f.read()
    return README

setup(
    name="Topsis-Harjot-102017126",
    version="1.0.2",
    description="A Python package implementing TOPSIS for MCDM",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Harjot tSingh",
    url = 'https://github.com/HarryGrewal9/Topsis-Harjot-102017126',
    download_url = 'https://github.com/HarryGrewal9/Topsis-Harjot-102017126/archive/refs/tags/v_02.tar.gz',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    
    install_requires=['numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=topsis:main",
        ]
     },
     keywords=['python', 'TOPSIS', 'MCDM', 'MCDA',
              'statistics', 'prescriptive analytics', 'cli'],
)