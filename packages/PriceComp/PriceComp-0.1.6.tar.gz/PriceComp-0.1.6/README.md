PriceComp
===================
#### esse pacote mostra os preços dos produtos de uma página da amazon em um gráfico de barras

## Instalação

` pip install PriceComp `

## Uso

```
import PriceComp as PC
link = 'https://www.amazon.com.br/link_pagina_produtos'
pc = PriceComparison()
pc.get_price(link)
```