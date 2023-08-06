from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ngram_ml',
    version='0.1.0',
    description='Basic python package for creating n-gram language models from text files',
    long_description_content_type  = 'text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/anil-gurbuz/ngram_ml',
    author='Anil Gurbuz',
    author_email='anlgrbz91@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['NLP', 'ngram', 'MLE', 'Simple Language Model', 'Neural Network'],
    packages=find_packages(),
    install_requires=['requests','numpy']
)