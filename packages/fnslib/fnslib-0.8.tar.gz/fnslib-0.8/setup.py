from setuptools import setup, find_packages
setup(
    name='fnslib',
    version='0.8',
    author='KeyDevS',
    author_email='rumaevvadim@gmail.com',
    packages=find_packages(),
    description='FNSLib',
    long_description=open('README.md').read(),
    install_requires=[
        'openai',
        'colorama',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
