from distutils.core import setup
setup(
    name = 'seins',
    packages = ['seins'], # this must be the same as the name above
    version = '0.3',
    description = 'A small command line utility to show you when the next train to your desired location is arriving',
    author = 'Kai',
    author_email = 'kai@woistbier.de',
    install_requires = [ 'colorama', 'requests', ' beautifulsoup4' ],
    url = 'https://github.com/mackaiver/sEins-Server',   # use the URL to the github repo
    download_url = 'https://github.com/mackaiver/sEins-Server/archive/master.zip', # I'll explain this in a second
    keywords = ['traffic', 'scrapping', 'utility', 'transportation', 's1', 'DB'], # arbitrary keywords
    license = 'MIT',
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts':
            ['seins = seins.seins:main',
             ]}
)