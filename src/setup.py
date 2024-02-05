from setuptools import setup, find_packages

setup(
    name='AnimalExpedition',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            "git update-index --assume-unchanged auth/client_secrets.json"
        ],
    },
    author='Ian Sohan',
    author_email='iangsohan@gmail.com',
    description='A short description of your project',
    url='https://github.com/yourusername/your-repo',
)
