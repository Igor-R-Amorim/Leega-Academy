# hands-on_Composer-Dataproc
Neste repositório serão armazenados os scripts e os procedimentos a serem seguidos para construir o hands-on.
<br> <br>
## INTRODUÇÃO
<br><br>
A ideia do laboratório é simular a extração dos dados de um e-commerce.  
<br>
<img src="https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/Processo%20Lab%20hands-on.jpg">
<br><br>
A extração acontece em 3 fontes de dados diferentes.
  - extração de 3 tabelas do dataset publico da google.
  - extração das trends e dos dados de 3 concorrentes do nosso e-commerce
  - e, por fim, a extração da situação geral da nossa economia para podermos tomar decições futuras.

<br>
O processamento é realizado, através das pipelines em pyspark, no cluster do dataproc, o qual irá carregar os dados em uma camada de dados brutos no bigquery.
Após o carregamento da camada de dados brutos, devemos remover o cluster do dataproc e transferir os dados da camada de dados brutos para uma camada de dados consolidados através de rotinas (procedures) do proprio bigquery.<br>
Todo esse processo requer uma ordem, que coordenamos através do Apache Airflow, no nosso caso a versão gerenciada no Google Cloud Compose.

## PREPARAÇÃO DO AMBIENTE

Antes de mais nada, é necessario acessar a sua plataforma na GCP e abrir o Cloud Shell.<br>

**[*Cloud Shell*](https://console.cloud.google.com/)** : <br>

Esses comandos serão criados no Cloud Shell e não nos operadores do airflow, pois não são operações cíclicas. Eles devem ser criados apenas uma vez assumindo o papel da infraestrutura necessária para rodar o airflow/composer.<br><br>
Para a realização do lab é necessário criar 2 buckets:<br>
a) Um primeiro, onde serão armazenados os dados do dataproc.<br>
b) E, um segundo, onde as pipelines e as bibliotecas a serem baixadas no ambiente python do cluster temporario do dataproc serão armazenadas.
<br><br>
Para tanto usaremos os comandos:
```
gsutil mb gs://[NOME_DO_SEU_BUCKET_DA_PIPELINE]
gsutil mb gs://[NOME_DO_SEU_BUCKET_DO_DATAPROC]
```
``` diff
- exemplo:
# gsutil mb gs://dataproc-pipeline-storage-bucket
# gsutil mb gs://dataproc-leega-storage-bucket
```
<kbd>Lembre-se que os buckets devem ter um nome único.</kbd><br>

Com os buckets criados, precisamos agora inserir os arquivos das pipelines nele. <br>
Primeiramente vamos criar uma pasta para os nossos arquivos, vou chama-la de 
airflow, mas podem chamar do que preferirem, basta lembrar o nome depois.
```
mkdir airflow
cd airflow/
```
Nessa pasta é onde clonaremos o nosso repositório do github.
```
token_cassic="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"
git clone https://${token_cassic}@github.com/SSTDevs/hands-on_Composer-Dataproc.git
```
Mova-se para dentro da pasta clonada do github.
```
cd hands-on_Composer-Dataproc/
ls
```
Com os arquivos clonados do github, podemos agora, copiá-los para o bucket
```
gsutil cp -r Dataproc_Pipelines/ gs://[NOME_DO_SEU_BUCKET_DA_PIPELINE]
```
``` diff
- exemplo: 
# gsutil cp -r Dataproc_Pipelines/ gs://dataproc-pipeline-storage-bucket
```
Verifique se os dados foram copiados para o bucket através do comando:
```
gsutil ls gs://[NOME_DO_SEU_BUCKET_DA_PIPELINE]/Dataproc_Pipelines/
```
``` diff
- exemplo: 
# gsutil ls gs://dataproc-pipeline-storage-bucket/Dataproc_Pipelines/
```
Por fim, vamos baixar o arquivo variables.json para a nossa maquina, e renomea-lo como variables.json
```
https://raw.githubusercontent.com/SSTDevs/hands-on_Composer-Dataproc/main/DAG_Folder/variables.json?token=GHSAT0AAAAAACIYWL7G4RPOOGBXGAQJSQRUZJG6PEQ
```
Ou tambem pode ser baixada diretamente do diretorio no atalho com icone de download: 
```
https://github.com/SSTDevs/hands-on_Composer-Dataproc/blob/main/DAG_Folder/variables.json
```
<hr/>

Além dos buckets precisaremos, também, criar os datasets que irão representar nossa camada de dados brutos e a de dados consolidados.
<br><br>
Para isso usaremos os comandos:
```
bq --location=us mk raw_MyEcommerce
bq --location=us mk trusted_MyEcommerce
bq --location=us mk wordcount_dataset
```
```
gcloud services enable dataproc.googleapis.com
```

<br><hr/>

**[*Console*](https://console.cloud.google.com/)** :<br>

Aproveitando o contato com o console, certifique-se de que a sua _service account_ tem as permissões necessárias para criar e operar tanto o composer como o dataproc. <br>
  - Se você estiver usando a _service account padrão de Compute Engine_, a permissão de editor deve ser o suficiente. <br><br>
  - Caso você esteja fazendo uma _service account_ exclusivamente para operar o composer/airflow, certifique-se de ter as roles:
<table>
  <tr>
    <td>BigQuery Data Editor :</td>
    <td>Permissão para ler e escrever dados em vários datasets o que é necessário para as nossas procedures</td>
  </tr>
  <tr>
    <td>BigQuery Job User :</td>
    <td>Permissão para service account poder criar jobs no bigquery</td>
  </tr>
  <tr>
    <td>Cloud Build Service Account :</td>
    <td>Permissão para recursos e triggers nosa serviços da cloud</td>
  </tr>
  <tr>
    <td>Cloud Composer v2 API Service Agent Extension :</td>
    <td>Permissão extra para que a conta de serviço do composer se comunique 
      com a conta de serviço do kubernetes autopilot, esse papel da permissão 
      de alterar o IAM de outra service accont </td>
  </tr>
  <tr>
    <td>Composer Worker :</td>
    <td>Permissão necessária para executar as VM do ambiente do Cloud Composer</td>
  </tr>
  <tr>
    <td>Dataproc Hub Agent :</td>
    <td>Permissão para a criação de clusters no dataproc </td>
  </tr>
  <tr>
    <td>Dataproc Service Agent :</td>
    <td>Permissão para  iniciar jobs no dataproc </td>
  </tr>
  <tr>
    <td>Environment and Storage Object Administrator :</td>
    <td>Permissão para que um usuário possa visualizar, criar, atualizar, fazer upgrade, 
      excluir ambientes, gerenciar objetos (como arquivos DAG) nos buckets do ambiente, 
      ou executar comandos CLI do Airflow</td>
  </tr>
</table>

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-01.png)

## CRIANDO O AMBIENTE DO COMPOSER

Agora sim, <br>
com todas as permissões devidamente concedidas, criaremos o nosso ambiente composer 2. Na barra de busca digite composer. <br>
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-02.png)

Ao se deparar com a janela do composer haverá, logo de cara, um botão CREATE com uma setinha para baixo, 
o qual abre um pop-up para selecionar o ambiente desejado. <br>
As opções de ambiente serão o composer 1 ou o composer 2. <br>
Selecione o composer 2. <br>
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-03.png)

Na janela que se abrirá digite o nome do seu composer, selecione o local (de preferência o com maior cotas de disponibilidade) e a _service account_ que você usará para orquestrar os serviços do airflow. <br>
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-04.png)

<kbd>Lembre-se, caso necessário clique no checkbox para conceder o papel V2 API Service Agent para a sua _service account_. </kbd><br><br>
Quanto aos recursos do ambiente vamos escolher as seguintes configurações baseadas no ambiente small: <br>
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-05.png)

Observe que diferentemente do ambiente small vamos usar apenas 1 worker no total, a fim de economizar com o valor do cluster. [sacrificando, assim, a escalabilidade do cluster]

Siga para o fim da página, clique em create, e aguarde. (o processo de criação leva entre 20 e 40 minutos)

> [!NOTE]
>  _no meu ambiente essa configuração usou 10 vcpu de cota, caso não esteja conseguindo fazer com o ambiente composer 2, 
>  teste com o ambiente do composer 1 com maquinas e2-small ou e2-medium o qual deve usar apenas 4-5 cotas.<br>
>  e lembre-se que ainda será necessário, pelo menos, mais 3 maquinas para o cluster de dataproc._ <br><br>

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-06.png)

**[*Configurar Composer*](https://console.cloud.google.com/composer/environments)** :<br>

Após a conclusão da criação do ambiente, deve aparecer a seguinte tela: 
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-07.png)

Nessa tela podemos ver se os serviços desejados estao todos saudáveis, assim como conferir os logs de criação e execução, 
a configuração do nosso ambiente e muito mais. <br>
Atente-se aos dois primeirs icones abaixo da barra de pesquisa: OPEN AIRFLOW UI e OPEN DAGS FOLDER.
Vamos clicar em OPEN AIRFLOW UI primeiro.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-08.png)

A pagina principal do WebServer do Airflow se abrirá essa pagina é onde podemos acompanhar de forma resumida como cada DAG esta rodando quais Taks foram concluidas quais estao rodando e quais falharam.<br>
Porem a primeira coisa que vamos fazer aqui é carregar as variaveis do ambiente. <br>
Passe o mouse sobre a opção _Admin_ do menu principal e clique em _Variables_.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-09.png)

Agora na pagina de variaveis vamos carregar o arquivo .json que baixamos agora pouco a alguns passos atrás. <br>
Selecione variables.json <br>
Em seguida click em _import variables_

As variaveis do ambiente que vamos usar, devem aparecer em sua tela agora.<br>

Confira se estão todas corretas, pois as variáveis foram, inicialmente, pré-definidas para o meu projeto, lembre-se de mudar o valor do projeto, do bucket e do storage. <br> 
Use o icone da caneta sobre uma lousa que fica entre o icone da lupa e da lixeira para editar o valor da variavel. <br>
  - o gce_region é a região de criação do cluster do Dataproc. <br>
  - o gcp_project é o ***ID do projeto*** da GCP ao qual você deseja rodar o dataproc, deve ser o mesmo projeto que esta rodando o airflow afim de evitar a necessidade abrir novas permissões. <br> 
  - o gcs_bucket é o Bucket que armazena as Pipilines do Dataproc. <br>
  - já o storage_bucket é o Bucket de dados temporários para a criação do Dataproc e de outros arquivos temparios da spark session. <br>
<kbd>Observe que a variavel storage_bucket não possui o prefixo 'gs://' diferentemente do gcs_bucket que necessita desse prefixo.</kbd><br>

<hr>
Vamos voltar agora para a pagina do ambiente do composer e clickar na opção OPEN DAGS FOLDER.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-10.png)

Esse Botão vai te jogar para a pagina do Cloud Storage, na pasta padrão de dags do seu airflow 

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-11.png)

Aqui temos 2 opçoões. <br>
  1. subir os arquivos pelo console <br>
  ou <br>
  2. subir os ambientes pela linha de comando do cloud shell
<br><br>

OPÇÃO 1:

  &emsp; Baixe a DAG para a sua maquina e a renomeie para 'DAG_dataproc_tutorial.py':
  ```
  https://raw.githubusercontent.com/SSTDevs/hands-on_Composer-Dataproc/main/DAG_Folder/DAG_dataproc_tutorial.py?token=GHSAT0AAAAAACIYWL7GS2JVNO5J36L5JRYQZJG7JGQ
  ```
  &emsp; ou
  ```
  https://github.com/SSTDevs/hands-on_Composer-Dataproc/blob/main/DAG_Folder/DAG_dataproc_tutorial.py
  ```
  &emsp; Com o arquivo baixado na sua maquina, suba-o para a pasta dags no Cloud Storage aberto pelo composer.
  e aguarde a DAG aparecer na pagina home do seu airflow-webserver

OPÇÃO 2:

  &emsp; Abra o Cloud Shell novamente conforme a indicação amarela e digite o seguintes códigos.
  ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-12.png)
  ```
  cd ~
  cd airflow/hands-on_Composer-Dataproc/DAG_Folder
  ```
  &emsp; Agora copie o caminho da sua pasta dags conforme a indicação laranja e cole apos o 'gs://' no codigo abaixo
  ```
  gsutil cp DAG_dataproc_tutorial.py gs://[SEU_CAMINHO_DAG]
  gsutil ls gs://[SEU_CAMINHO_DAG]
  ```
  
  ``` diff
  - exemplo:
  # gsutil cp DAG_dataproc_tutorial.py gs://us-central1-testando-compos-a46de1ac-bucket/dags
  # gsutil ls gs://us-central1-testando-compos-a46de1ac-bucket/dags
  ```

<hr>

Vamos voltar para a pagina home do webserver do nosso airflow, e verificar se a DAG agora aparece.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-14.png)
<kbd>Após a inserção da DAG na pasta de dags do airflow, ela deve aparecer no webserver entre 2 a 5 minutos.</kbd>

Nessa janela é possivel acompanhar as ações que acontecem com as nossas DAGS, quais estao executando no momento, quais falharam ou concluiram.<br>
É possivel ver tambem de forma abreviada, quais tarefas foram concluidas, quais ainda nao foram iniciadas, quais foram bem sucedidas e quais falharam. <br>
Para visualizar de forma mais detalhada clique no nome da nossa DAG (composer_dataproc_tutorial).

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-15.png)

Na aba de grid, A DAG selecionada abre mais detalhes de cada tarefa. Épossivel tambem clicar em cada tarefa e verificar mais detalhes, bem como o log de cada tarefa.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-16.png)

Vamos clicar agora na aba Graph, onde poderemos ver de forma visual o relacionamento entre as tarefas.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-17.png)

Note que além do relacionamento é possivel ter mais informações sobre cada tarefa clicando em cima da mesma, assim como fizemos na aba Grid. 

## ENTENDO A DAG

Certo, entendi como adicionar e monitorar a minha DAG no airflow, mas o que exatamente a minha DAG esta fazendo? <br>
Para entender mais a fundo a nossa DAG, vamos entrar no codigo da DAG e explorar um pouco as suas funcionalidades. <br>
Temos 2 formas de acessar o codigo da DAG nesse exemplo.

OPÇÃO 1: Por um editor externo (CLI) <br>
  &emsp; Para aqueles que baixaram o arquivo no passo anterior através de algum dos dois links:
  ```
  https://raw.githubusercontent.com/SSTDevs/hands-on_Composer-Dataproc/main/DAG_Folder/DAG_dataproc_tutorial.py?token=GHSAT0AAAAAACIYWL7GS2JVNO5J36L5JRYQZJG7JGQ
  ```
  &emsp; ou
  ```
  https://github.com/SSTDevs/hands-on_Composer-Dataproc/blob/main/DAG_Folder/DAG_dataproc_tutorial.py
  ```
  &emsp; Basta abrir o arquivo 'DAG_dataproc_tutorial.py' em seu editor preferido. (VS code, PyCharm, notepad++,...)
  
  &emsp; ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-18.png)

OPÇÃO 2: Pelo editor da google <br>
  &emsp; Dessa forma vamos abrir o arquivo clonado do github em nosso ambiente do Cloud Shell. <br>
  &emsp; Ao abrir o Cloud Shell vamos ver em seu menu superior a opção editor e clicar nele. <br>
  ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-19.png)
  <kbd>É claro que você pode usar um editor de texto simples como vi, vim, nano. Porem, acredito ser mais interessante usar um editor que possua ferramentas de auto-completar e de destacar fragmentos do codigo como os ide possuem</kbd> <br><br>
  &emsp; Ao terminar de se conectar ao editor, você poderá encontrar a sua pasta no ficheiro lateral (Explorer). <br>
  &emsp; Expanda o conteudo da pasta clicando no simbolo '>'(collapse) em frente ao nome da pasta até encontrar <br>
  &emsp; o arquivo 'DAG_dataproc_tutorial.py' no endereço. ( ~/airflow/hands-on_Composer-Dataproc/DAG_Folder/ )
  ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-20.png)
  &emsp; Ao der um duplo clique no arquivo, você podera visualizar o codigo com o editor Theia dentro da propria GCP.
<hr>

Visto como acessar o código da nossa DAG vamos ver alguns pontos interessantes dela:
Sobre a construção da DAG ela foi partida em 6 blocos
  - Logo após a declaração e importação das bibliotecas e dependências, o primeiro bloco é o ajuste de argumentos, variáveis e caminhos e nomes de arquivos a serem usados na execução da DAG.
  ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-21.png)

  - Seguindo, após instanciar a DAG, nesse Bloco tempos os codigos resposáveis pelas operações de criar e deletar o cluster Dataproc.
    ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-22.png)
  
  - Após a criação do cluster, achei interessante trazer diferentes formas de operar no seu cluster. A titulo de curiosidade temos 3 exemplos:
     - Um exemplo classico de word_count da google usando hadook, oude o job le um arquivo e escreve no bucket o resultado.
     - Outro exemplo fazendo a mesma coisa usando o pyspark
     - E por fim um Job fazendo o mesmo word_count em pyspark a partir da leitura de uma tabela no bigquery e escrita do resultado em um dataset.
  - Alem dos exemplos apresentados, o cluster de dataproc aceita jobs de:
     - hadoop_job	
     - spark_job	
     - pyspark_job	
     - hive_job	
     - pig_job	
     - spark_R_job	
     - spark_Sql_job	
     - presto_job	
     - flink_job
       
  ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-23.png)
    <kbd>Os exemplos trazidos nessa DAG são automaticamente desprezados durante o funcionamento</kbd><br>
  
  - O bloquinho com os operadores mais esperado, os pipelines:   
    ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-24.png)
  
  - Fechando com a chamada dos procedures no BigQuery:
    ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-25.png)
  
  - E finalizando com a ordenação de cada uma das tarefas:   
    ![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-26.png)

Vamos relembrar: <br>
O problema porposta era rodar várias pipelines em Dataproc e algumas procedures em BigQuery para atualizar a nossa camada de dados consolidados.
Inicialmente essa DAG precisa de 4 variáveis básicas que nos já adicionamos anteriormente.
<table>
  <tr>
    <td>#gcs_bucket</td>
    <td>Bucket das Pipilines do Dataproc</td>
  </tr>
  <tr>
    <td>#gce_region</td>
    <td>Região de criação do cluster do Dataproc</td>
  </tr>
  <tr>
    <td>#gcp_project</td>
    <td>Projeto da GCP ao qual você deseja rodar o dataproc, deve ser o mesmo projeto que esta rodando o airflow</td>
  </tr>
  <tr>
    <td>#storage_bucket</td>
    <td>Bucket de dados temporários para a criação do Dataproc</td>
  </tr>
</table>

Para atender a esses requisitos, foi construido a DAG pensando-se em quais operadores seriam necessários:
<table>
  
  <thead>
    <tr>
      <th colspan="2">Operando o Cluster</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DataprocCreateClusterOperator:</td>
      <td>Operador responsável por criar o cluster do dataproc na regiao desejada, com as várias configurações que necessitamos</td>
    </tr>
    <tr>
      <td>DataprocDeleteClusterOperator:</td>
      <td>Operador responsável por deletar o cluster do dataproc ao final do trabalho</td>
    </tr>
  </tbody>
  
  <thead>
    <tr>
      <th colspan="2">Exemplos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DataProcHadoopOperator:</td>
      <td>Operador responsável por criar um job hadoop no cluster dataproc desejado</td>
    </tr>
    <tr>
      <td>DataProcPySparkOperator:</td>
      <td>Operador responsável por criar um job em pyspark no cluster dataproc desejado</td>
    </tr>
    <tr>
      <td>DataprocSubmitJobOperator:</td>
      <td>Operador responsável por criar qualquer job no cluster dataproc desejado. 
        
  _Esse operador é mais novo que os demais especificos._
      </td>
    </tr>
  </tbody>
  
  <thead>
    <tr>
      <th colspan="2">Pipelines</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DataprocSubmitPySparkJobOperator:</td>
      <td> Toda a pipeline é feita em pyspark, potanto como já apresentado, este é o operador responsável por criar um job em pyspark no cluster dataproc desejado</td>
    </tr>
    <tr>
      <td>BigQueryInsertJobOperator:</td>
      <td>Operador responsável por executar um job no BigQuery, o qual pode ser uma DML, DQL ou DDL</td>
    </tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2">Procedures</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BigQueryOperator:</td>
      <td>Operador depreciado para chamar uma query no BigQuery</td>
    </tr>
    <tr>
      <td>BigQueryInsertJobOperator:</td>
      <td>Operador atual responsável por executar um job no BigQuery, o qual pode ser uma DML, DQL ou DDL</td>
    </tr>
  </tbody>
</table>

<br><hr><br> 

Entendendo agora o funcionamento da nossa DAG vamos detalhar os passos a serem coordenados e suas tarefas. 

    create_dataproc_cluster \                                   
    >> [ex_dataproc_hadoop, ex_dataproc_pyspark] \              # exemplo salvando em bucket
    >> ex_dataproc_JobOperator \                                # exemplo usando BQ
    >> [p1_spark, p2_spark, p3_spark] \                         # extrai os dados do e-commerce
    >> dummy_intermediate \                                     # Operação intermediaria necessaria entre listas
    >> [p4_spark, p5_spark, p6_spark, p7_spark] \               # extrai dados dos concorrentes e do cenario economico
    >> p8_bigquery \                                            # executa query para salvar em tabela as trends
    >> p9_spark \                                               # geração da word_cloud a partir da tabela P8
    >> [prc_transformTrusted_layer, pcr_loadTrusted_layer] \    # execução das procedures do BQ
    >> delete_dataproc_cluster

<table>
  
  <thead>
    <tr>
      <th colspan="2"><i>Primeiro Passo: create_dataproc_cluster</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>create_dataproc_cluster</td>
      <td>Antes de qualquer operação de extração, o Cluster deve estar criado e funcionando para receber as tarefas</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>
  
  <thead>
    <tr>
      <th colspan="2"><i>Passo 2 e 3 em paralelo: [ex_dataproc_hadoop, ex_dataproc_pyspark]</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ex_dataproc_hadoop:</td>
      <td>exemplo de um job em hadoop salvando o resultado em bucket</td>
    </tr>
    <tr>
      <td>ex_dataproc_pyspark:</td>
      <td>exemplo de um job em pyspark salvando o resultado em bucket</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>
  
  <thead>
    <tr>
      <th colspan="2"><i>Passo 4: ex_dataproc_JobOperator</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ex_dataproc_JobOperator:</td>
      <td> exemplo de um job em pyspark salvando o resultado em bucket </td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 5, 6 e 7 em paralelo: [p1_spark, p2_spark, p3_spark]</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>p1_spark:</td>
      <td>Extracting your e-commerce operational table order_items</td>
    </tr>
    <tr>
      <td>p2_spark:</td>
      <td>Extracting your e-commerce operational table inventory_items</td>
    </tr>
    <tr>
      <td>p3_spark:</td>
      <td>Extracting your e-commerce operational table events</td>
    </tr>
  </tbody>
  <tr><td> </td><td> </td></tr>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 7, 8, 9 e 10 em paralelo: [p4_spark, p5_spark, p6_spark, p7_spark]</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>p4_spark</td>
      <td>Dollar variation price in Brazil</td>
    </tr>
    <tr>
      <td>p5_spark</td>
      <td>Extracting Brazil inflational informations</td>
    </tr>
    <tr>
      <td>p6_spark</td>
      <td>Extracting Brazil's basic interest rate information</td>
    </tr>
    <tr>
      <td>p7_spark</td>
      <td>Extracting your e-commerce rivals market informations</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 11: p8_bigquery</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>p8_bigquery</td>
      <td>Criar uma tabela temporária com o periodo e o local desejado para ser capturado as trends</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 12: p9_spark</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>p9_bigquery</td>
      <td>Conta e agrega as palavras da tabela temporária</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 13 e 14 em paralelo: [prc_transformTrusted_layer, pcr_loadTrusted_layer]</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>prc_transformTrusted_layer</td>
      <td>Executa a correção de números vazios e faltantes para zero antes de transferir os dados para a camada consolidada</td>
    </tr>
    <tr>
      <td>pcr_loadTrusted_layer</td>
      <td>Transfere as tabelas com dados corretos da camada raw para a camada consolidada</td>
    </tr>    
    <tr><td> </td><td> </td></tr>
  </tbody>

  <thead>
    <tr>
      <th colspan="2"><i>Passo 15: delete_dataproc_cluster</i></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>delete_dataproc_cluster</td>
      <td>Deleta o cluster independente de alguma ação anterior ter falhado ou não</td>
    </tr>
    <tr><td> </td><td> </td></tr>
  </tbody>
</table>

<kbd> Como já mencionado, os exemplos trazidos nessa DAG são automaticamente desprezados durante o seu funcionamento </kbd>

Voltando para o seu webserver do airflow, agora você deve ver a seguinte sequência concluída:

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-27.png)

Note que os exemplos foram pulados e as pipelines seguiram normal.

Se visitarmos a pagina dos jobs do dataproc <a href="https://console.cloud.google.com/dataproc/jobs">https://console.cloud.google.com/dataproc/jobs</a> podemos ver exatamente os jobs que foram executados, bem como ler o log e a saida printada em codigo para cada job. Isso ajuda muito a debugar o código caso necessário.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-28.png)

Se visitarmos também a pagina do bigquery <a href="https://console.cloud.google.com/bigquery">https://console.cloud.google.com/bigquery</a> poderemos ver quais tabelas foram devidamente carregadas e transferidas da raw para a trusted.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-29.png)

## MONITORAMENTO E ALERTAS 

Já sabemos agora como monitorar o ciclo de atividades de extração e transformação que precisamos. Mas eu não queria ter a obrigação de olhar todo dia a pagina do airflow para saber se todas as tarefas deram certo. <br>
O que poderia ser feito para otimizar esse monitoramento?

Poderiamos nos argumentos da DAG escrever quais emails vão receber uma notificação em caso de falha ou nova tentativa. Mas imaginando um cenário com muitas e muitas DAGs, não seria simples o gerenciamento dessa lista de emails de notificação.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-30.png)

Portanto, uma forma um pouco mais interessante de gerenciar essas notificações pode ser através do cloud monitoring da google. (<a href="https://console.cloud.google.com/monitoring/alerting"> https://console.cloud.google.com/monitoring/alerting ) <br>

<hr>

**[*Composer Airflow - Fail Task*](https://console.cloud.google.com/monitoring/alerting/policies)** :<br>

O cloud monitoring vai permitir o controle sobre os avisos de qualquer tarefa, seja ela de qualquer DAG do seu workspace.
Vamos criar o nosso primeiro aleta. clique em CREATE POLICY.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-31.png)

Clique no SELECT A METRIC e digite workflow, clique no 'Cloud Composer Workflow > Workflow > Task Duration'

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-32.png)

Vamos adicionar um filtro, pois queremos alertar sobre todas as tasks que venham a falhar.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-33.png)

A janela de observação será de 1 minuto e vamos contar as ocorrencias acontecem nesse periodo.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-34.png)

Qualquer violação acima de 0.99 é uma tarefa que veio a falhar.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-35.png)
<kbd>Adicione o condition name de forma explicativa, pois no email padrão da google ele aparece logo no titulo da notificação.<\kbd>

Como pretendemos enviar um email, é fundamental adicionar o email nos canais de notificação. <br>
Você pode selecionar um ou mais emails para receber essa notificação de falha. (ex. Quero mandar para o responsável do setor e para a equipe responsável pela manutenção)

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-36.png)

Vamos finalizar com o nome do alerta e clicando em next para revisar e seguir com a criação da politica.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-37.png)

<hr>

**[*Dataproc Job - Long Duration*](https://console.cloud.google.com/monitoring/alerting/policies)** :<br>

Para a nossa DAG que usa outros recursos da cloud, como a criação de cluster no dataproc é interessante monitorar o tempo de atuação de cada job para que ele não fique rodando além do tempo esperado. <br>
Para a criação desse alerta, vamos clicar novamente em CREATE POLICY. Vamos digitar DATAPROC no filtro e abrir o seguinte caminho 'Cloud Dataproc Job > Job > Job state'

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-38.png)

Queremos capturar apenas os Jobs que estão em funcionamento, portanto vamos clicar em ADD A FILTER e selecionar apenas os Jobs em execução. <br>
A Janela será de 5 minutos e vamos contar as ocorrencias de cada job em execução nessa janela.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-39.png)

Após isso vamos acionar a nossa notificação acima de 4.99 minutos e clicar em NEXT.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-40.png)

Nessa janela vamos mais uma vez configurar um novo email para receber a notificação.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-41.png)

Vamos finalizar dando um nome ao nosso alerta, clicando em next para revisar e salvar a politica.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-42.png)

<hr>

**[*Dataproc Cluster - Long Running*](https://console.cloud.google.com/monitoring/alerting/policies)** :<br>

Devemos tambem nos certificarmos que o cluster não irá permanescer em funcionamento. Seja por um travamento (deadlock) inesperado, uma conexão que fica inesperadamente viva com o DB ou com o API, ou mesmo caso a tarefa de deletar o cluster dê algum erro. <br>
Portanto queremos um alerta para nos informar caso o cluster esteja funcionamento acima do tempo estipulado.<br><br>
Analogamente aos outros alertas vamos comecar clicando em CREATE POLICY e no quadro SELECT A METRIC. Vamos fintrar a busca por Dataproc e econtrar o caminho: 'Cloud Dataproc Cluster > Cluster > Running Nodes'

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-43.png)

O filtro será apenas sobre o nó mestre, pois o cluster pode ter diversos nós trabalhadores o que atrapalharia a contagem dos minutos na janela de tempo. <br>
vamos então definir a janela com 10 minutos para somar o tempo de funcinamento nesse periodo.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-44.png)

Após isso vamos acionar a nossa notificação acima de 9.99 minutos e clicar em NEXT.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-45.png)

Definir novamente um novo email para receber a notificação e dar o nome ao nosso alerta, por fim finalizar clicando em next para revisar e salvar a politica.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-46.png)

<hr>

**[*Testando os alertas*](https://console.cloud.google.com/monitoring/alerting/policies)** :<br>

Portanto a sua sessão de alerting deve ficar assim no final:

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-47.png)

Com todas as politicas construidas vamos testar os alertas. <br>
Volte a página home do seu webserver do airflow e clique no nome da nossa DAG (composer_dataproc_tutorial)

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-48.png)

Dentro da Aba grid, clique no icone de 'play', me seguida clique em 'Trigger DAG' para acinar a nossa DAG.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-49.png)

Acompanhe as tasks e observe que P6 irá demorar bastante para concluir, pois está configurada com o timmer de 5 minutos além do proprio tempo de processamento para ser concluida.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-50.png)

Antes do fim da execução da DAG clique em alguma task dos exemplos e clique no botão 'Mark Failed', para que possamos testar o alerta de TASK_FAILED.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-51.png)

Ao fim do ciclo com todas as tasks em verde escuro sinalizando que foram concluidas com sucesso, devemos receber os emails de notificação conforme o esperado.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-52.png)
![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-53.png)

Ao clicar em alguma das notificações observe que o email trará o gatilho de acionamento, o valor observado da notificação e o Job que esta ocorrendo esse problema.

![alt text](https://storage.googleapis.com/dataproc-storage-leega-bucket/Hands-on_Imagens/tutorial-54.png)
<kbd>É possivel manipular mais ainda o email, estilizar quais informações disponiveis no monitoring você deseja receber e fazer outros acinamentos caso ao inves de enviar o alerta parao  email, façamos o alerta acionar um topico do pub/sub</kbd>

<hr>

## Segregando grupos de acesso as nossas camadas de dados no BigQuery
