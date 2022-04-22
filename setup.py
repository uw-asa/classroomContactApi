from setuptools import find_packages, setup

setup(
    name='classroomContactApi',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'pyodbc',
        'flask_caching',
    ],
)
