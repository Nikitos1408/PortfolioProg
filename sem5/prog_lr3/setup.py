from setuptools import setup, find_packages

setup(
    name='weatherUN',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'weatherUN=weatherUN.getweatherdata:main',
        ],
    },
    author='Ugarin Nikita',
    author_email='ugarinna@mail.ru',
    description='package using OpenWeather API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nikitos1408',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
