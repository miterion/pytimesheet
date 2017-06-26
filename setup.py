from setuptools import setup, find_packages

setup(
        name='timetrack',
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'timetrack=timetrack.cli:main',
            ],
        }
)
