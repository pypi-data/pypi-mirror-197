import setuptools

setuptools.setup(
    name="workforcesim",
    version="0.4.22",
    url="https://github.com/NeuraXenetica/synaptans-workforcesim",
    author="Matthew E. Gladden",
    author_email="matthew.gladden@neuraxenetica.com",
    description="Synaptans WorkforceSim is a free open-source web app for simulating the complex dynamics of a factory workforce – including workers’ daily job performance, personal interactions with their peers and supervisors, and attrition. The simulated activity is analyzed visually and outputted in a CSV file whose format is designed for use with predictive analytics packages like Comport_AI.",
    packages=['workforcesim'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'fastapi',
        'uvicorn',
        'jinja2',
        'matplotlib',
        'python-multipart',
        'seaborn'
    ],
)