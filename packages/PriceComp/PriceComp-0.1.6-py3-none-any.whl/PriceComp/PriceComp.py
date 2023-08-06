
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt

class PriceComparison():
    def __init__(self):
        pass

    def get_price(self, link):
        """
        Recupera o preço de todos os produtos de uma pagina da amazon, e mostra um gráfico de barras com todos os preços encontrados na página.

        param link: Uma string contendo o link para a página dos produtos.
        retorno: None
        """
        # cria uma instância do driver do Chrome e navega até o link fornecido
        driver = webdriver.Chrome('/path/to/chromedriver')
        driver.get(link)

        # recupera o código-fonte HTML da página
        html = driver.page_source

        # fecha o driver
        driver.quit()

        # cria uma instância da classe BeautifulSoup com a fonte HTML e analisa com o 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')

        # encontra todos os containers contendo o preço do produto
        price_containers = soup.find_all('div', attrs={'class': 'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'})

        # inicializa uma lista vazia para armazenar os preços
        product_price = []

        # se recipientes de preços forem encontrados
        if price_containers is not None:
            for price_container in price_containers:
               # encontra o preço do produto
                price = price_container.find('span', attrs={'class': 'a-offscreen'})

                # se o preço é encontrado
                if price is not None:
                    forma = price.text.replace('\xa0', '')
                    forma2 = forma.replace('R$', '')
                    forma3 = forma2.replace('.', '')
                    forma4 = forma3.replace(',', '.')

                   # converte o preço em float e o anexa à lista de preços
                    product_price.append(float(forma4))
                else:
                    print('Price could not be found.')
        else:
            print('Price container not found.')

        # cria uma lista de números de 0 até o comprimento da lista de preços para colocar no eixo X
        lista = []
        for i in range(0,len(product_price)):
            lista.append(i)

        # cria um gráfico de barras com os preços de todos os produtos de determinada página de produtos da amazon
        plt.bar(lista, product_price)
        plt.title('Price change')
        plt.xlabel('Product')
        plt.ylabel('Price')
        plt.show()
