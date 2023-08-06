# meteorologicalData
==============================

### Atraves desse pacote, o usuario podera visualizar os dados meteorologicos e a localizacao exata de uma determinada cidade.

## Instalacao

Para instalar o pacote, basta executar o comando abaixo:

<pre><code>pip install meteorologicalData</code></pre>

## Uso

<pre><code>
from meteorologicalData import main
md = main.MD(cidade, tipo) """ tipo == 'visualizar' or 'retornar' """
md.retorna_dados()

Se tipo for igual a 'retornar', use uma variavel para receber a lista com os dados meteorologicos.

lista = md.retorna_dados()
</code></pre>


