from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='systemdlogger',
    version='0.2.0',
    description='Exports systemd logs to cloudwatch/elasticsearch.',
    long_description=long_description,
    url='https://github.com/techjacker/systemdlogger',
    license='MIT',
    author='Andrew Griffiths',
    author_email='mail@andrewgriffithsonline.com',
    packages=['systemdlogger'],
    entry_points={
        'console_scripts': [
            'systemdlogger = systemdlogger.systemdlogger:main'
        ]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
)
