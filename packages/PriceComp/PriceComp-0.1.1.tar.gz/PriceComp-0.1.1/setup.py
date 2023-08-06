from setuptools import setup, find_packages

VERSION = '0.1.1' 
DESCRIPTION = 'Comparador de preços'
LONG_DESCRIPTION = 'Faz web scraping de uma pagina de produtos da amazon e mostra um gráfico de barras com todos os preços'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="PriceComp", 
        version=VERSION,
        author="Ueslei Ferreira",
        author_email="<ueslei392@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['bs4','selenium', 'matplotlib'], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]

)