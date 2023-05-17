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
que foca em transações operacionais.
<p align=center><img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/access%20gif.gif" width=84%></p>  
Esta solução possui as seguintes bases: <br>
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
<br>-Ferramenta de ETL: Pentaho 9.3
<br>-Ambiente da ODS: Pasta Drive (simulando uma pasta em servidor interno, com controle de acesso)[Liberando apenas os emails dos envolvidos]
<br>-Ambiente DW: MySQL Community Edition
<br>-Ambiente Relatorios: PowerBI Desktop 

<br> Portanto o workflow que seria desenvolvido seria:
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/22aca8f4f640ade90d37168146ef86920e4b9c0c/Leega-Foods/Imagens/WorkFlow.jpg width=84%></p>

<br>
<h3 align=center><strong> ETL1: Geração da ODS </strong></h3>

Para a geração da ODS optou-se por mantê-la em arquivo de texto (csv ou avro ou parquet) em um ambiente no servidor interno com acesso apenas interno devido ao nivel de detalhamento das tabelas funcionarios e clientes. 
A necessidade de manter a ODS se dá devido a necessidade do cliente em acessar detalhes dos pedidos em menor granulação através de um drill na visão. (funcionalidade ainda a ser desenvolvida no projeto)

Para obter uma ODS completa conforme a modelagem foi necessário enriquecer alguns elementos e/ou remover alguns campos.
As tabelas com transformaçoes foram: Detalhes_Pedidos, Pedidos, Funcionarios, Clientes. O restante das tabelas foram apenas carregadas e exportadas em csv.

- Modelagem da ODS
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/ODS.png width=84%></p>

- ETL Pedidos
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/ODS_Pedido.png width=84%></p>

- ETL Funcionarios
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/ODS_Funcionario.png width=84%></p>

- ETL Clientes
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/ODS_Cliente.png width=84%></p>

- JOB Carga_ODS
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/463844d7ec08233447efa2329ed78220e6245eb6/Leega-Foods/Imagens/Carga_ODS.png width=84%></p>

<br>
<h3 align=center><strong> ETL2: Carregamento Dimensional </strong></h3>

Procurando responder o maior numero de perguntas gerenciais possiveis, foi-se estudado qual seria o melhor schema para a proposta do Leega Foods, O star Schema nos geraria uma performance melhor que o modelo snow-flake ou o modelo pai-filho. 

- Modelagem Dimensional
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/bab88ec3da3bf4b5c45c67f0875c8d6de22f2355/Leega-Foods/Imagens/Dim.png width=84%></p>

Para atender algumas exigencias do Leega foods foi necessario desenvolver algumas lógicas para verificar:
1) Se os transportadores eram globais ou locais;
2) Quais eram as equipes dos funcionarios (Alpha, Beta, Coyote, Delta ou Figma)
3) O tipo de Cliente conforme o gasto em pedidos, se ele é classificação A B ou C (A >= 100k > B > 30k > C)
4) O tipo de Fornecedor conforme o gasto em pedidos, se ele é classificação A B ou C

Assim como na ODS Para obter resultados condizentes com a modelagem foi necessário enriquecer alguns elementos e/ou remover alguns campos.
As tabelas com transformações foram: DIM_transportadora, DIM_Funcionarios, DIM_Cliente, DIM_Fornecedor, FT_Pedidos. O restante foi apenas carregado no MySQL.
 
- ETL DIM_transportadora
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/b84f3ed5d2e4678c4454d76e1186a0677abc0ce2/Leega-Foods/Imagens/DIM_Transportador.png width=84%></p>

- ETL DIM_Funcionarios
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/bab88ec3da3bf4b5c45c67f0875c8d6de22f2355/Leega-Foods/Imagens/DIM_Funcionario.png width=84%></p>

- ETL DIM_Cliente
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/bab88ec3da3bf4b5c45c67f0875c8d6de22f2355/Leega-Foods/Imagens/DIM_Cliente.png width=84%></p>

- ETL DIM_Fornecedor
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/bab88ec3da3bf4b5c45c67f0875c8d6de22f2355/Leega-Foods/Imagens/DIM_Fornecedor.png width=84%></p>

- ETL FT_Pedidos
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/bab88ec3da3bf4b5c45c67f0875c8d6de22f2355/Leega-Foods/Imagens/FT_Pedido.png width=84%></p>

A fim de conseguir rodar as Cargas Historicas é necessario que o DataBase (DB) esteja criado, portanto para a carga historica foi necessario desenvolver um script em SQL para a criação do DB

- Script SQL
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/b84f3ed5d2e4678c4454d76e1186a0677abc0ce2/Leega-Foods/Imagens/SQL.png width=84%></p>

- Carga Historica
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/af709987d752b1ebda415deaa395fb3ba46ed27a/Leega-Foods/Imagens/Carga_Historica.png width=84%></p>

Para Finalizar, foi conectado o PowerBI ao Mysql a fim de gerar alguns insights e levar para a gestão avaliar o valor das visões levantadas pela equipe de Dados.
Durante as reuniões rascunhamos rapidamente as solicitações do cliente. [A dinamica aqui é anotar o maximo de detalhe enquanto o cliente pensa o que ele deseja como produto] 

- Visão 1
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%201.png width=84%></p>
Uma Visão identica a desenhada pela antiga SupremEats 

- Visão 2
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%202.png width=84%></p>
Solicitação: "Tenho uma hipotese que o valor total do pedido e o valor do desconto tem uma correlação por produto" <br>
Queria em um grafico, em uma visualização, por categoria, e por produto. Se a hipotese total pedido vs valor desconto é verdadeira. Toda vez que aumenta o desconto, os clientes pedem mais produtos dentro da nossa empresa? Isso realmente acontece?
 
- Visão 3
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%203.png width=84%></p>
Solicitação: "Um sistema de semaforo, totais do produto por categoria" <br>
Além do total do produto, quero a visao da quantidade comprada, do valor do frete, valor desconto, valor total produto, sinalizando aqueles totais que estão abaixo, media ou acima, alem de seleção periodo acima.

- Visão 4
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%204.png width=84%></p>
Solicitação: "Ao longo do ano, sementre, trimestre, mes, uma visao por fornecedor, por categoria, das quantidades vendidas, e valores totais dos produtos" <br>
Desejo selecionar a categoria do produto e selecionar o produto que quiser.

- Visão 5
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%205.png width=84%></p>
Solicitação: "Visão geográfica" <br>
Visão geográfica pra identificar os locais que mais compraram, o valor do desconto dado e também o total do produto comprado, e que esta região, o tamanho da compra, defina o tamanho da bolha ou símbolo que preferir.

- Visão 6
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%206.png width=84%></p>
Solicitação: "Transportadora x Frete" <br>
Quanto esta sendo pagando de frete pra transportadora, por tipo de transportadora, por trasnportadora, ao longo do tempo, quais os paises e regiões que mais gastamos com frete. a visão deve ser do maior pro menor.

- Visão 7
<br><br> <p align=center><img src=https://github.com/Igor-R-Amorim/Leega-Academy/blob/0e3ae557c43d112461bb3abbc1f8100711939ce5/Leega-Foods/Imagens/Visao%207.png width=84%></p>
Não Solicitado. <br>
Trouxemos uma visao extra para responder questoes mais basicas utilizando as dimensoes não participantes das perguntas do cliente.
Sobre quais paises o vendedor que mais fatura atua.
O vendedor que mais fatura é o que atende o maior numero de pedidos? ele é o que dá mais descontos?
O Cliente que gasta mais com a gente é o que mais faz pedidos? é o que paga mais caro em frete?

Perguntas futuras.
Qual seria o ticket medio de clientes por categoria?
A Categoria A tem um ticket medio maior que a média geral?

Devido ao tempo do projeto, algumas perguntas ficaram em aberto para a proxima etapa do projeto.
Com elas, o desenvolvimento das ETLs agendadas no pentaho/crontab.
