from setuptools import setup, find_packages


setup(
    name="ExpdMailService",
    version="0.3.0",
    license='MIT',
    author="greg he",
    author_email='greg.he@expeditors.com',
    description="Python Module for sending mail from Expeditors internal mail server",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='sending mail',
    install_requires=[
        'loguru', 'pandas'
    ],
)