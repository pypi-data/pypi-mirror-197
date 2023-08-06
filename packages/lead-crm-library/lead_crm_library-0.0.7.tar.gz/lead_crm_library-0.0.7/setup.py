from setuptools import setup, find_packages

setup(
    name='lead_crm_library',
    version='0.0.7',
    description='A library for managing generic leads in CRMs',
    author='Matias Nuñez',
    author_email='matiasne45@gmail.com',
    url='https://github.com/matiasnu/lead_crm_library',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'simple_salesforce',
        'hubspot',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
