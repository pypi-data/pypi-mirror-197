from setuptools import setup,find_packages 
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cyberonix",
    version="2.0.14",
    author="Metaxone",
    author_email="admin@metaxonesolution.com",
    description="Cyberonix is a complete resource hub for Cyber Security Community.",
    url='https://github.com/TeamMetaxone/Cyberonix',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
    ],
    install_requires=[
        "beautifulsoup4",
        "requests",
        "ipwhois",
        "dnspython==2.3.0",
        "selenium==4.7.2",
    ],
    entry_points={
        'console_scripts': [
            'cyberonix = cyberonix.cyberonix:starting'
        ]
    }
)

