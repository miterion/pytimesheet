from setuptools import setup, find_packages

setup(
        name='pytimesheet',
        version='0.0.2',
        license='GPL',
        install_requires =['Jinja2'],
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'timetrack=pytimesheet.cli:main',
            ],
        }
)
