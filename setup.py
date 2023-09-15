from setuptools import setup, find_packages

setup(
    name='unblockedGPT',
    version='0.3.2',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
        'openai',
        'pycryptodome',  # This provides the Crypto module
    ],
    entry_points={
        'console_scripts': [
            'unblockedGPT = unblockedGPT.run_app:run',
        ],
    },
)

def run():
    os.system('streamlit run app.py')

