from setuptools import setup, find_packages


setup(
    name="easyGPT",
    version="0.0.1",
    author="Sanjin",
    description="A short description of easyGPT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "easyGPT = easyGPT.easyGPT:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)