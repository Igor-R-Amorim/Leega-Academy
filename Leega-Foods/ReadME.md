<h3 align=center><strong> Fundamentação </strong></h3>

<p align="justify">
Dentro da política de expansão e geração de negócios, o Board de acionistas
da Leega decidiu investir no setor de Varejo e Ecommerce. <br>
Para isto decidiu adquirir uma empresa que opera globalmente, a SupremEats, 
e após fechado o negócio, definiram que o novo nome será Leega Foods. <br> 
</p>

<p align="justify">
A nossa equipe de dados formada por analistas, engenheiros e
cientistas de dados foi chamada para várias reuniões. Nelas tivemos
oportunidade de conhecer esta operação e como estão montadas as
soluções de tecnologia, mas, durante as reuniões percebemos que
antiga empresa não tinha uma solução de Analytics, e muito menos
de ciência de dados, portanto, para que possamos crescer ainda mais, teremos que
criar uma solução capaz de suportar a operação desta nova empresa e gerar
importantes insights para nossos acionistas. <br> 
</p>

<p align="justify">
Toda operação está apoiada por um “ERP Caseiro” desenvolvido em Microsoft Access
que foca em transações operacionais. Esta solução possui as seguintes bases: <br>
</p>

1. Categoria dos Produtos
2. Clientes
3. Funcionários
4. Pedidos
5. Detalhes dos Pedidos
6. Produtos
7. Transportadoras
8. Fornecedores
9. Países <br>

E, a modelagem relacional que existe nesta aplicação é:
<br><br> <p align=center><img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ea8e94d5beab59a46e9b6da175e4f65c3bb0d551/Leega-Foods/Imagens/Modelagem%20Leega_Foods.png" width=84%></p>

<br>
  
Com base nestas informações, o nosso trabalho será aplicar tudo o que
aprendemos nos módulos e “operacionalizar” a solução de Analytics e Data
Science da Leega Foods.

<br>
<h3 align=center><strong> Arquitetura de implantação </strong></h3>
Após a divisão dos Grupos, foi levantado a arquitetura esquemática da operação.
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/032ff14f73d3585618844bc90f57244a6fd6ae88/Leega-Foods/Imagens/Arquitetura.png width=84%></p>

A solução deveria contar com uma Data Staging Area a qual seria responsavel por armazenar a ODS (operational data store)
seu ciclo de vida seria de 1 ano de dados.

Entre a Data Staging Area e o DW (Data Warehouse) deveria ser feito ETL para agregar as informações. Pois o DW deve conter: 
- Estrutura analitica e modelagem dimensional, otimizada para leitura e consulta (OLAP) 
- Ciclo de vida das informaçoes de 3 anos
- Informaçoes em granulação maior (mes e ano) 

Por fim, a infraestrutura deve ser capaz de segmentar as visões em diferentes DataMarts a fim de democratizar o acesso as informaçoes conforme o nivel de privacidade e acesso de cada setor.

<br>
<h3 align=center><strong> WorkFlow </strong></h3>
Levando em consideração o custo de aquisição do seguimento de Ecommerce, a equipe optou por seguir com ferramentas OpenSource e/ou com licencas community disponiveis.
Portanto o workflow que seria desenvolvido seria:
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/22aca8f4f640ade90d37168146ef86920e4b9c0c/Leega-Foods/Imagens/WorkFlow.jpg width=84%></p>
