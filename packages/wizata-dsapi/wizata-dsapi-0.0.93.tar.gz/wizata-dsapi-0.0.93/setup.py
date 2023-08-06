from setuptools import setup

setup(
    name='wizata-dsapi',
    version='0.0.93',
    description='Wizata Data Science Toolkit',
    author='Wizata S.A.',
    author_email='info@wizata.com',
    packages=['wizata_dsapi'],
    install_requires=[
        'flask',
        'pandas',
        'numpy',
        'dill'
    ]
)
