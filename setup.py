from setuptools import find_packages, setup

requirements = [
    'speedtest-cli',
    'python-crontab',
]

setup(
    name='speed_analysis',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'speed_analysis = connection_speed_analysis.app:main'
        ]
    })
