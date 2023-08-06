import setuptools

setuptools.setup(
    name="comport-ai",
    version="0.3.23",
    url="https://github.com/NeuraXenetica/comport_ai",
    author="Matthew E. Gladden",
    author_email="matthew.gladden@neuraxenetica.com",
    description="An HR predictive analytics tool that forecasts the likely range of a worker’s future job performance, using ANNs whose custom loss functions enable them to formulate prediction intervals that are as small as possible, while being just large enough to contain a worker’s actual future performance in most cases.",
    packages=['comport-ai'],
    entry_points={'console_scripts': ['comport-ai=comport_ai.run:main']},
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'numpy', 'pandas', 'fastapi', 'uvicorn', 'jinja2', 'matplotlib', 'python-multipart', 'seaborn', 'tensorflow<2.11', 'openpyxl', 'scikit-learn', 'tabulate'
    ],
)