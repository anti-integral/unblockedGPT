from setuptools import setup, find_packages

setup(
    name='unblockedGPT',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'unblockedGPT = unblockedGPT.run_app:run',
        ],
    },
)
