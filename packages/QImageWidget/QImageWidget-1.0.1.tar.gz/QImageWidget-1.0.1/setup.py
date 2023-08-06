from setuptools import setup, find_packages

setup(
    name='QImageWidget',
    version='1.0.1',
    description='A PyQt5/PySide2 widget for displaying images',
    author='Render666',
    author_email='hackermananonimous228666@gmail.com',
    url='https://github.com/RedEnder666/QImageWidget',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.4',
        'PySide2>=5.15.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
