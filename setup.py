from setuptools import setup, find_packages


# Lee el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webscraping_project",
    version="0.1.0",
    author="Ing. Alejandro Gamboa",
    author_email="agamboacj@gmail.com",
    description="a webscrapping project with python to collect data from CNU profile carriers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gamboaalejandro/web-scrapping-python.git",
    packages=find_packages(),  # Encuentra y lista todos los paquetes automáticamente
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Tipo de licencia
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    install_requires=[  # Dependencias del proyecto
        "beautifulsoup4>=4.9.3",
        "requests>=2.25.1",
        "scrapy>=2.4.1",
        "selenium>=3.141.0",
        "pandas>=1.1.5",
        "lxml>=4.6.2",
        "pyquery>=1.4.0",
        "fake-useragent>=0.1.11",
        "psycopg2>=2.9.9",
    ],
    entry_points={  # Puntos de entrada para crear scripts ejecutables
        'console_scripts': [
            'webscrape=scripts.scraper:main',
        ],
    },
)