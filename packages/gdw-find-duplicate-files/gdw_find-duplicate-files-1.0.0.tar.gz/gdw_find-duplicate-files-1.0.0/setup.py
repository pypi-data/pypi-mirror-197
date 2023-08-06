from setuptools import setup, find_packages

setup(
    name='gdw_find-duplicate-files',
    version='1.0.0',
    description='A command-line utility for finding duplicate files on your hard drive',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/your_username/your_project',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'find-duplicate-files = find_duplicate_files:main'
        ]
    }
)
