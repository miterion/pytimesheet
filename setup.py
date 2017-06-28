from setuptools import setup, find_packages

setup(
        name='pytimesheet',
        version='0.0.3',
        license='GPL',
        description='timetracking for hiwis at tu darmstadt',
        install_requires =['Jinja2'],
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'timesheet=pytimesheet.cli:main',
            ],
        }
)
