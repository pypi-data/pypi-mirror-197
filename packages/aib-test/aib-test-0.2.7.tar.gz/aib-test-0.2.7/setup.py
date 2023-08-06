from setuptools import setup, find_packages

setup(
    name='aib-test',
    version='0.2.7',
    description='',
    long_description='',
    author='',
    author_email='',
    url='',
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        "ray==2.2.0",
        "scikit-learn==1.2.1",
        "xgboost==1.7.3",
        "mysql-connector-python==8.0.32",
        "dill==0.3.6",
        "ipython==8.8.0",
        "pydantic==1.10.4",
        "pandas==1.5.2",
        "SQLAlchemy==1.4.46",
        "imbalanced-learn==0.10.1",
        "pyarrow==7.0.0"
    ],
    packages=find_packages()
)
