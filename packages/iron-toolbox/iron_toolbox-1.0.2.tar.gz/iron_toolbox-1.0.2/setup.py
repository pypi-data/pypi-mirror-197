import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setuptools.setup(
    name='iron_toolbox',
    packages=['iron_toolbox'],
    version='1.0.2',
    license='MIT',
    description='Functions to be used by Iron Data Analytics Team',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Luciano Siqueira',
    author_email='lucianosiqueira@iron.fit',
    url='https://github.com/IronTrainers/iron_data_toolbox',
    project_urls={
        "Bug Tracker": "https://github.com/IronTrainers/iron_data_toolbox/issues"
    },
    install_requires=[
                    'awswrangler',
                    'boto3',
                    'duckdb',
                    'fsspec',
                    'numpy',
                    'pandas',
                    'paramiko',
                    'pyarrow',
                    'pydomo',
                    'pymongo',
                    's3fs',
                    'tqdm',
                    'Unidecode',
                    'pysftp'],
    keywords=['python',
              'mongodb',
              'aws',
              'domo',
              'iron_toolbox'],
    download_url="https://github.com/IronTrainers/iron_data_toolbox/archive/refs/tags/iron_data_toolboox.tar.gz",
)
