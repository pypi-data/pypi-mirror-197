from setuptools import setup, find_packages

setup(
    name='rna_seq_normalization',
    version='0.3.0',
    description='Python package used for performing RNA-Seq normalization. It contains the three most popular techniques: TPM, RPKM and CPM.',
    author='Sergio Vazquez Montes de Oca',
    author_email='sergiovazquezmontesdeoca@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['rna-seq', 'rna', 'tpm', 'normalization', 'rpkm', 'cpm', 'rna-sequencing', 'statistics', 'bioinformatics'
              'data analysis', 'data science'],
    install_requires=[],
    python_requires='>=3.6',
)
