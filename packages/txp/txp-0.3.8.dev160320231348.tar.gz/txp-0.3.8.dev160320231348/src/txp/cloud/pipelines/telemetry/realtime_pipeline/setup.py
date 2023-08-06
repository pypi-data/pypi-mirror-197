import setuptools

setuptools.setup(
    name='pub_sub_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "dynaconf",
        "txp[cloud]==0.3.8.dev160320231310"
    ],
    packages=setuptools.find_packages()
)
