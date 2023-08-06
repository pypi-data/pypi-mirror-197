from setuptools import find_packages, setup
setup(
    name='updateMondayItemLib',
    packages=find_packages(),
    version='0.1.1',
    description='Update the existing items on monday board',
    author='Bilal Ashraf',
    license='MIT',
    long_description="This package allows you to update columns against item on monday.com board.It takes following parameters apiKey,apiUrl,board_id,item_id, **columnValuesDict. Columns ID and their values are passed as key value pair in dictionary.",
    long_description_content_type='text/markdown'
)