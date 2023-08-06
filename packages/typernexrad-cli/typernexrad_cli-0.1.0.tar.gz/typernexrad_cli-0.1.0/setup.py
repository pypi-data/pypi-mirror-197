from setuptools import setup, find_packages

with open ('mypackage_readme.txt', 'r') as f:
    long_description = f.read()

setup(
    name='typernexrad_cli',
    version='0.1.0',
    description= "CLI which helps to access several functionalities of NEXRAD",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Team 7',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [".env"],
    },
    py_modules=['team7_typer.typer_main'],
    install_requires=[
        'typer',
        'boto3',
        'python-dotenv',
        'pandas',
        'python-dotenv',
        'bcrypt',
        'python-jose',
        'fastapi',
        'requests',
        'pyOpenSSL',

                ],
entry_points={
    'console_scripts': [
        'typer_t7 =team7_typer.typer_main:app',
    ],
}
)
