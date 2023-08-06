import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='vemseg',
    version='0.0.5',
    packages=['vemseg'],
    url='https://github.com/MatousE/vemseg',
    license='BSD 3-Clause License',
    author='MatousE',
    author_email='matous.elphick@gmail.com',
    description='A python package for the segmentation of organelles in volume electron microscopy data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=['numpy',
                      'apoc',
                      'scipy',
                      'scikit-image',
                      'scikit-learn',
                      'matplotlib',
                      'xgboost',
                      'setuptools'
                      ]
)
