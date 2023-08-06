import setuptools

#Adding code for packaging
setuptools.setup(
    include_package_data=True, 
    name='yopycalc', 
    version='0.0.3.2', 
    description='yopycalc python module',
    url='https://github.com/ravindra-rao/setuptoolsdemo.git',
    author='yobro',
    author_email='contact@yobro.com',
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'pytest'
    ], 
    long_description='yopycalc python module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)