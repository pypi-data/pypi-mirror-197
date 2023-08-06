from setuptools import setup, find_packages


setup(
    name="simpleGPT",
    version="0.0.2",
    author="Sanjin",
    description="A short description of your package",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "simpleGPT = simpleGPT.simpleGPT:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)