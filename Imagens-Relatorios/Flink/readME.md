# Apache Flink - Quick Guide

O **Apache Flink** é um **framework de processamento de dados distribuído** e de código aberto, criado para lidar com grandes volumes de dados em **real-time** e em **batch**. Ele pertence à categoria de sistemas de processamento de dados em stream, o que significa que pode processar dados à medida que eles são gerados, em oposição ao processamento em batch, onde os dados são processados em blocos.

## Tipos de processamento
### > Processamento Batch
**Descrição:** O processamento em batch, ou em lote, refere-se à **execução de tarefas de processamento de dados estáticos** em grandes volumes, ***em um intervalo de tempo pré-determinado***. Os dados são coletados, armazenados e processados em lotes e suas operações são programadas para serem executadas em momentos específicos, como diariamente, semanalmente, mensalmente, assim por diante.<br>

**Principais características:** 
1. Realiza o ***processamento de grandes*** volumes de dados, permitindo otimizações e economias de escala no processamento de dados;
2. As tarefas de processamento são geralmente **planejadas e agendadas** para serem executadas em horários específicos, *muitas vezes fora do horário de pico de uso do sistema*, evitando impactos na operação do dia-a-dia.
3.  Extremamente útil em cenários onde a **coesão e a integridade dos dados** são críticas, já que são planejadas para executar seguindo uma ordem de dependências de dados.<br>

### > Processamento Real-time
**Descrição:** O processamento em real-time refere-se ao **processamento de dados conforme são gerados, sem atrasos significativos** fornecendo respostas em tempo hábil, muitas vezes em frações de segundo ou segundos, o que é crucial em cenários onde a tomada de decisões precisa ser rápida, como em sistemas de monitoramento, detecção de fraudes, streaming de mídia, entre outros.<br>
**Principais características:** 
1. O processamento em real-time é caracterizado pela necessidade de **baixa latência**, com o objetivo de fornecer **respostas rápidas**, quando não imediatas, à medida que os dados são gerados, para que sejam tomadas de decisões em tempo hábil;
2. Os dados são processados à medida que são recebidos, permitindo uma **visão em tempo real do estado do sistema** e continuam sendo alterados já que estão em um fluxo contínuo de dados;
3. É **orientado por eventos**, possibilitando que a execução de operações específicas, como atualizações de sensores, detecção de fraudes, transações financeiras, entre outros

## Ecossistema do Apache Flink:

### > Storage (Armazenamento)
&emsp; O Apache Flink oferece diversas alternativas para consumo e armazenamento de dados. Abaixo, apresentamos uma lista básica das opções disponíveis
  * HDFS (Hadoop Distributed File System)
  * Local File System
  * S3
  * RDBMS (MySQL, Oracle, MS SQL etc.)
  * MongoDB
  * HBase
  * Apache Kafka
  * Apache Flume

### > Deploy (Implantação)
&emsp; O Apache Flink pode ser implantado em modo local, em cluster ou em cloud.<br>
&emsp; Para as implantaçoes em clusters, existem os seguintes modos:

  * **Standalone mode** é adequado para pequenos clusters Spark, mas não é recomendado para clusters maiores (pois há uma sobrecarga ao executar daemons do Spark(master + slave) nos nós do cluster). Esses daemons exigem recursos dedicados, portanto, o modo Standalone não é recomendado para clusters de produção maiores. Para clusters de produção empresarial em grande escala, é recomendado escolher o YARN ou Mesos mode.
  
  * Ao adotar o **YARN mode**, o Spark opera como um aplicativo, eliminando a sobrecarga de daemons e proporcionando eficiência operacional. YARN é um gerenciador de recursos distribuídos versátil, projetado especialmente para cargas de trabalho Hadoop. Ideal para ambientes que já possuem um cluster Hadoop em execução (Apache/CDH/HDP), o YARN destaca-se como uma escolha otimizada, oferecendo integração sólida com o ecossistema Hadoop existente. Recomenda-se sua utilização ao considerar a implementação em clusters de produção empresariais em grande escala, garantindo desempenho consistente e adaptado às necessidades específicas do ambiente Hadoop.
  
  * Assim como o YARN mode, ao escolher o **Mesos mode**, o Spark também opera como um aplicativo. Por outro lado, o Mesos é uma escolha ideal para novos projetos ou ambientes que buscam suportar uma ampla variedade de cargas de trabalho, independentemente do ecossistema Hadoop. O Mesos mode é um gerenciador de recursos distribuídos abrangente, projetado para suportar todos os tipos de cargas de trabalho, desde MapReduce, Spark, Flink até Storm. Adicionalmente, existe a opção de usar ambos os modos YARN e Mesos ao mesmo tempo fazendo uso do projeto Apache Myriad, proporcionando uma abordagem combinada para atender a diferentes requisitos de implantação.
  
&emsp; já na cloud, existem opções de uso do flink gerenciado.
 
&emsp; -Na *AWS*, você pode usar o Flink através de um cluster hadoop no EMR: Elastic MapReduce;

&emsp; -Na *GCP*, você pode usar o Flink através de um cluster hadoop no Dataproc;
  
&emsp; -Na *Azure*, você pode usar o Flink através de um cluster hadoop no Azure HDInsight no AKS.

### > Kernel
&emsp; Esta é a camada de execução do software, é a que fornece o processamento distribuído, tolerância a falhas, confiabilidade, capacidade de processamento iterativo nativo e muito mais.

### > APIs & Libraries
&emsp; Esta é a camada superior e mais importante do Apache Flink. Possui o Dataset API, que cuida do processamento em lote, e Datastream API, que cuida do processamento de stream. Existem outras bibliotecas como o Flink ML (para aprendizado de máquina), Gelly (para processamento de gráficos), Tables para SQL, entre outras. Essa é a camada que fornece os diversos recursos do Apache Flink.

&emsp; O diagrama abaixo mostra as diferentes camadas do ecossistema Apache Flink

<img src="https://www.tutorialspoint.com/apache_flink/images/ecosystem_on_apache_flink.jpg"  
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

## Aquitetura
A arquitetura básica do Flink é composta por quatro componentes, Programa, Cliente, JobManager e TaskManager. Sendo cada um deles definidos por:

**-Programa:**
É um trecho de código que você executa no cluster Flink.

**-Cliente:**
É responsável por pegar o código (programa) e construir um grafo de fluxo de dados do trabalho, em seguida, passá-lo para o JobManager. Também verifica o resultado dos trabalhos.

**-JobManager:**
Após receber o Grafo de Fluxo de Dados do Trabalho do Cliente, é responsável por criar o grafo de execução. Ele atribui o trabalho aos TaskManagers no cluster e supervisiona a execução do trabalho.

**-TaskManager:**
É responsável por executar todas as tarefas atribuídas pelo JobManager. Todos os TaskManagers executam as tarefas em slots separados, com uma paralelização especificada. Também é responsável por enviar o status das tarefas para o JobManager.

<img src="https://www.tutorialspoint.com/apache_flink/images/execution_architecture.jpg"  
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

<br><br>

https://www.tutorialspoint.com/apache_flink/apache_flink_introduction.htm

<br><br>


<hr>

# Apache Flink - Quick Start

## Ambiente do lab
Visto o básico da arquitetura, do funcionamento e do uso do Apache Flink, vamos comecar a utilizá-lo.

O ambiente utilizado será o: <br><br>
><br>
> - Oracle Virtual Box: Versão 7.0.8 r156879 (Qt5.15.2) <br>
>  Link: https://www.virtualbox.org/wiki/Downloads <br>
><br>
> - Linux mint: Versão 21.2-cinnamon-64<br>
>  Link: https://mirror.ufscar.br/mint-cd/stable/21.2/linuxmint-21.2-cinnamon-64bit.iso<br>

<br>
Após instalar o Linux mint e atualizar o sistema operacional, precisamos observar a versão do Java para o correto funcionamento do Apache Flink.<br>
A versão utilizada do <b>Flink, a v1.18.0,</b> que é a mais recente versão do Flink até o momento da confecção deste tutorial, ela necessita do Java 11 instalado.<br> 
E quando o mint está atualizado, a versão do Linux mint escolhida já contempla a versão 11 do JDK.<br>

Para verificar a versão, utilize o comando:  
``` shell
java -version
```

A respota deve ser: `$ OpenJDK Runtime Environment (build 11.0.21+9-post-Ubuntu-0ubuntu122.04)` 
<br><br>
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/35e59b4c2c815e0ff8e57c0766feb489805d6594/Imagens-Relatorios/Flink/img03.jpg"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

Em seguida, vamos baixar o Apache Flink para ser executado em nossa maquina.
Utilize os comandos:
``` shell
wget https://dlcdn.apache.org/flink/flink-1.18.0/flink-1.18.0-bin-scala_2.12.tgz
tar -xzf flink-1.18.0-bin-scala_2.12.tgz
cd flink-1.18.0/
./bin/start-cluster.sh
ls -l
```
## Execução de Job através da linha de comando
Com o ambiente do flink instalado, vamos testar se o flink esta funcionando corretamente tentando rodar um job de exemplo.
Utilize, os comandos:
``` shell
./bin/flink run examples/streaming/WordCount.jar
tail log/flink-*-taskexecutor-*.out
```
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/403f98600349511852a811b693478caf3cc12e5f/Imagens-Relatorios/Flink/img02.jpg"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

É possivel verificar o funcionamento do nosso job tambem na interface gráfica do Flink.
<table>
  <tr> 
   <td> <img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/6343a25f48760668d4953a5a1237d071353771ba/Imagens-Relatorios/Flink/img04.png"
             style="border-radius: 10px; 
             border:1px solid;
             display: block;
             margin-left: auto;
             margin-right: auto;
             width: 90%;">
   </td>
  </tr>
  <tr> 
   <td> <img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/6343a25f48760668d4953a5a1237d071353771ba/Imagens-Relatorios/Flink/img05.png"
             style="border-radius: 10px; 
             border:1px solid;
             display: block;
             margin-left: auto;
             margin-right: auto;
             width: 90%;">
   </td>
  </tr>
</table>

## Execução de Job através da interface gráfica

Visto isso funcionando, agora vamos experimentar rodar um job diretamente pela interface gráfica.

<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/54d5894815e9e8c3afb0f814450a22f8684c2d26/Imagens-Relatorios/Flink/img06.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
Clique em "Add New" e vamos ao endereço: `/home/[SEU_USUARIO_LINUX]/flink-1.18.0/examples/streaming`<br>
No meu ambiente o endereço fica assim: Ex.: `/home/admin123/flink-1.18.0/examples/streaming`
<br><br>
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/54d5894815e9e8c3afb0f814450a22f8684c2d26/Imagens-Relatorios/Flink/img07.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
Localize novamente o arquivo WordCount.jar e de um duplo clique nele ou clique em "Open" na sequencia.
Assim que subir o arquivo na interface gráfica de um clique sobre o nome e expanda as informaçoes do seu Job.
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/d8501142b2269b93df4d7c0b37486c217e864dd4/Imagens-Relatorios/Flink/img08.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
Por fim é só clicar em "Submmit" para iniciar o Job WordCount mais uma vez.
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/d8501142b2269b93df4d7c0b37486c217e864dd4/Imagens-Relatorios/Flink/img09.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
Note que há mais um novo job WordCount nos "Completed Jobs"
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/d8501142b2269b93df4d7c0b37486c217e864dd4/Imagens-Relatorios/Flink/img10.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
## Construir um job em pyflink

Certo, entendi como iniciar os jobs no Flink, mas agora eu quero aprender a construir um novo job.<br>
Como eu posso fazer um? <br>

Para fazer um job vamos utilizar o editor de texto `xed` para programar em python. 

### > Verificação de requisitos para criar um job em pyflink

Portanto primeiramente, vamos verificar se o python foi atualizado corretamente nessa maquina. <br>
Utilize o comando: `python3 --version` , o Apache Flink v1.18.0 aceita: Python 3.7, 3.8, 3.9 ou 3.10. <br>
``` shell
python3 --version
```
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ba66e7d594a9504e41db40b6b0c1cc3db05100ae/Imagens-Relatorios/Flink/img11.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

Em seguida utilize o comando: 
``` shell
python --version
```
> Caso o comando falhe utilize: <br>
> `sudo ln -s /usr/bin/python3 /usr/bin/python` <br>
> com o link criado, teste novamente o comando: `python --version`

Vamos agora confirmar se o nosso cluster de Flink esta conseguindo executar um código escrito em python. Para isso vamos executar o word_count de novo para teste: <br>
Execute o comando: 
``` bash
./bin/flink run --python examples/python/table/word_count.py
```
<br>
Observe na interface gráfica se o job foi executado no cluster:
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ba66e7d594a9504e41db40b6b0c1cc3db05100ae/Imagens-Relatorios/Flink/img12.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

Estando tudo conforme e o job com status de *FINISHED* vamos então comecar a escrever o nosso job:

### > Contextualização e criação do job

Imagine o seguinte problema.

Uma bolsa de estudos será dada ao melhor aluno da classe. Após vários testes durante o curso, os dois melhores alunos encontram-se empatados. <br>
A fim de desempatar os dois, o professor fará um ultimo teste onde os 2 alunos estarão em computadores separados e farão provas identicas. <br>
Essa prova possui 30 questões de multipla escolha, sendo que essas questões contém pontuações diferentes dependendo no nivel da questão. <br>
A quantidade de questões respondidas por ambos os alunos serão somadas.<br>
Ao ser respondido um total de 10 questões entre ambos os alunos, a prova acaba.<br>
Para garantir que o julgamento será justo. O placar será transmitido em tempo real aos demais alunos.<br>
<br>
Entendido o contexto? <br>
<br>
Vamos então precisar retornar algumas informações no placar para que o público possa acompanhar.
Foram pensados em:
``` 
"ID do Aluno:"
"Questões Respondidas:"
"Ponto da questão:", 
"Total Pontuado:", 
"Média:"
```

Para atender essas informações, a primeira coisa que precisa ser feita é uma função que receba um par de valores (id_aluno, pontuação_do_aluno) e processar as informações desejadas. <br>
Para isso, vamos desenvolver a seguinte função no editor de texto do Linux Mint o `xed`
Digite no seu terminal:
``` bash
xed &
```
<kbd>Ou se preferir digite `xed` ou `TextEditor` no menu iniciar.</kbd>  <br>
A função deve receber o par de valores, iniciar o placar de cada um dos alunos, atualizar a quantidade de questoes respondidas e o total pontuado por aluno. Na sequencia calcular a média e retornar os valores desejados.
``` python
state_dict = {}

def Score(value):
    global state_dict

    # Inicializar o estado para o aluno, se necessário
    if value[0] not in state_dict:
        state_dict[value[0]] = {'Sum': 0, 'Cnt': 0}

    # Acessar os valores do estado atual do aluno
    state = state_dict[value[0]]
    Sum = state['Sum']
    Cnt = state['Cnt']

    # Atualizar o estado
    Sum += value[1]
    Cnt += 1
    state['Sum'] = Sum
    state['Cnt'] = Cnt

    return ("Aluno:", value[0],
            "Questões Respondidas:", Cnt,
            "Ponto:", value[1],
            "Total:", Sum,
            "Média:", round(Sum / Cnt, 2))
```
Podemos testar o funcionamento da nossa função no terminal, usando o comando `python3 caminho\do\arquivo\função.py` ou usar o [colab](https://colab.research.google.com/). Vamos testar usando os pares de resultado do aluno 'a' e do aluno 'b' como exemplo:
``` python
#Pares:
#('a', 1),
#('b', 2),
#('b', 2),
#('a', 3)

print(Score(('a', 1)))
print(Score(('b', 2)))
print(Score(('b', 2)))
print(Score(('a', 3)))
```
Estando a função devidamente escrita e retornando os valores desejados, vamos voltar para a parte principal da estrutura do Flink no programa. <br>
<br>
Precisamos começar instanciando uma sessão de streaming com o StreamExecutionEnvironment. <br>
Na sequência vamos enviar uma janela de valores na ordem que eles foram acontecendo. <br> 
Esses valores serão particionados por uma chave que é justamente o id do aluno. <br>
Por fim, vamos aplicar a nossa função que retorna as informaçoes do placar: a função Score(). E imprimir o valor no terminal do cluster. <br>
Com tudo devidamente construido. É só dar o "execute" em nossa instância. 
``` python
env = StreamExecutionEnvironment.get_execution_environment()
# [(id_aluno, pontuação_do_aluno)]
env.from_collection([('a', 3), ('b', 2), ('b', 2), ('a', 4), ('b', 3),
                     ('a', 4), ('b', 3), ('a', 3), ('b', 2), ('b', 2)]) \
   .key_by(lambda row: row[0]) \
   .map(Score) \
   .print()

env.execute()
```

Portanto, <br>
a estrutura do código completo ficaria: [media.py](https://github.com/SSTDevs/Tools/blob/f93f1d773cb21b0fb8205ea618880188c66a2df6/ApacheFlink/media.py)
``` python
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment, RuntimeContext, MapFunction
from pyflink.datastream.state import ValueStateDescriptor

# Dicionário para armazenar o estado por aluno
state_dict = {}

def Score(value):
    global state_dict

    # Inicializar o estado para o aluno, se necessário
    if value[0] not in state_dict:
        state_dict[value[0]] = {'Sum': 0, 'Cnt': 0}

    # Acessar os valores do estado
    state = state_dict[value[0]]
    Sum = state['Sum']
    Cnt = state['Cnt']

    # Atualizar o estado
    Sum += value[1]
    Cnt += 1
    state['Sum'] = Sum
    state['Cnt'] = Cnt

    return ("Aluno:", value[0],
            "Questões Respondidas:", Cnt,
            "Ponto:", value[1],
            "Total:", Sum,
            "Média:", round(Sum / Cnt, 2))


#_________________________________________________________________________________________________________________________


print("""
---------------------------------------------------------------------------------------------------------------------------
O contexto desse job é simular uma competição entre 2 alunos. Cada aluno tem acesso 
as mesmas 30 questoes. Quando o somatorio de questoes respondidas chegar a 10 questoes, 
encerra-se a competição.
 
O placar do jogo é transmitido da seguinte forma: 
(id_aluno, quantidade de questões respondidas pelo mesmo, pontuação atual da resposta, total de pontos, e a média do aluno)
se estiver no terminal na pasta do flink utilize: `tail log/flink-*-taskexecutor-*.out`
---------------------------------------------------------------------------------------------------------------------------
""")

env = StreamExecutionEnvironment.get_execution_environment()
# [(id_aluno, pontuação_do_aluno)]
env.from_collection([('a', 3), ('b', 2), ('b', 2), ('a', 4), ('b', 3),
                     ('a', 4), ('b', 3), ('a', 3), ('b', 2), ('b', 2)]) \
   .key_by(lambda row: row[0]) \
   .map(Score) \
   .print()

env.execute()
```
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/825cae8098c79c78672a7c3eee431dca0c1319bf/Imagens-Relatorios/Flink/img13.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">
  
Apesar do exemplo ter sido algo simples, como uma competição, poderiamos utilizar uma lógica análoga para jogos, ou sensores, ou diversas outras aplicações no Flink. <br>
Pois o que acabamos de utilizar, foi o **DataStreamAPI** do Apache Flink. <br>
Caso tenha curiosidade, além da operação *Map* que usamos em nossa função o Apache flink possui diversos outros metodos em sua documentação: [DataStreamAPI](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/datastream/operators/overview/) 

## Utilizando o SQL-Client do Flink

Outra forma de utilizar o potencial do Flink é através do [SQL-Client](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sqlclient/#interactive-command-line), o qual permite filtrar e visualizar os resultados em tempo real. <br>
Com essa solução, é possivel fornecer um meio fácil de escrever, debuggar e submeter tabelas no cluster de Flink sem escrever sequer uma linha de Java, Python ou Scala. <br>
 
O SQL-Client é um pacote da distribuição regular do Flink, portanto pode ser usado imediatamente. Ele necessita apenas de um cluster de Flink em execução para processar as tabelas. <br>
Levando em consideração que já iniciamos o clustes para os exemplos anteriores, com o comando './bin/start-cluster.sh', então, para usar o SQL Client utilize agora o comando abaixo em uma nova aba no terminal:
``` bash
./bin/sql-client.sh
```
<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ba66e7d594a9504e41db40b6b0c1cc3db05100ae/Imagens-Relatorios/Flink/img14.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

Vamos confirmar se existe uma conexão com o cluster executando a seguinte query: <br>
``` SQL
SET 'sql-client.execution.result-mode' = 'tableau';
```
``` SQL
SET 'execution.runtime-mode' = 'batch';
```
``` SQL
SELECT
  name,
  COUNT(*) AS cnt
FROM
  (VALUES ('Bob'), ('Alice'), ('Greg'), ('Bob')) AS NameTable(name)
GROUP BY name;
```
o resultado esperado é:
```
+-------+-----+
|  name | cnt |
+-------+-----+
| Alice |   1 |
|   Bob |   2 |
|  Greg |   1 |
+-------+-----+
```
> você pode fechar a visualização de resultado precionando a tecla "q" se necessário

<hr>

O SQL-Client respondendo corretamente o que esperavamos, vamos então entender como utilizar o SQL no Flink para resolver problemas.

Assim como na maioria dos bancos relacionais, é possivel criar Databases e Catálogos.<br>
`-- Criar e definir catálogo`
```SQL
CREATE CATALOG MyCatalog
  WITH (
    'type' = 'generic_in_memory'
  );
```
```SQL
USE CATALOG MyCatalog;
```
`-- Criar e definir database`
```SQL
CREATE DATABASE MyDatabase;
```
```SQL
USE MyDatabase;
```
Até então os comandos são exatamente iguais ao padrão ANSI do SQL, porém é durante a criação de tabela que vemos o primeiro detalhe de diferença em comparação aos bancos relacionais convencionais. <br>
Logo após a declaração da criação temos a obrigação de explicitar o connector e onde desejamos ler e/ou escrever os dados. No caso, para não baixarmos ferramentas auxiliares como kafka, ou MySql, ou qualquer outra, vamos utilizar o 'filesystem' como conector.

`-- Criar a Tabela` 
```SQL
--É possivel passar o caminho completo, ex.:
--CREATE TABLE MyCatalog.MyDatabase.people_job(...
-- ou apenas o nome, pois defininos anteriormente qual catalog e DB estaremos usando.

CREATE TABLE people_job (
    id INT,
    name STRING,
    job STRING,
    salary BIGINT,
    ts_field TIMESTAMP(3),
    WATERMARK FOR ts_field AS ts_field  - INTERVAL '1' SECOND
  )
  WITH (
    'connector' = 'filesystem',
    'path' = 'file:///home/admin123/flink-1.18.0/examples/people.csv',
    'format' = 'csv',
    'csv.ignore-parse-errors' = 'true'
    );
```
A titulo de curiosidade, o conector 'filesystem' configurado dessa forma, guarda cada conjunto de inserção como um fragmento de CSV. Quando pedirmos para ler aquela tabela, ele irá trazer todas as *partes* de csv daquele endereco referente a consulta.

<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ba66e7d594a9504e41db40b6b0c1cc3db05100ae/Imagens-Relatorios/Flink/img15.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

O conector filesystem aceita JSON, Avro, Parquet, ORC e raw, além do formato CSV. <br>
Para mais informações sobre esse conector acesse: [Filesystem](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/filesystem/). <br>
Para mais informaçoes de outros conectores acesse: [Conetores](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/overview/). <br>
<br>

``` SQL
SELECT COUNT(*) FROM MyCatalog.MyDatabase.people_job;
```
É possivel inserir dados a partir de uma subconsulta assim como no SQL ANSI.
``` SQL
INSERT INTO people_job 
  SELECT id, name, job, salary, TO_TIMESTAMP(ts_field, 'yyyy-MM-dd HH:mm:ss.SSS') as ts_field
  FROM
    (VALUES 
      (1, 'Bob', 'Data Engineer', 1, '2020-10-19 13:27:00.000'), 
      (2, 'Alice', 'Business Analyst', 1, '2020-10-19 13:27:05.000'), 
      (3, 'Greg', 'Data Engineer', 1, '2020-10-19 13:27:10.000'), 
      (4, 'Bob', 'Business Analyst', 1, '2020-10-19 13:27:15.000')
    ) AS NameTable(id, name, job, salary, ts_field);
```
``` SQL
SELECT * FROM people_job ORDER BY ts_field ASC;
```
``` SQL
SELECT job, 
       avg(salary) AS avg_salary, 
       count(*) AS nr_people 
FROM people_job 
GROUP BY job;
```
É possivel criar um job de dados agregados com o Flink, por exemplo:
``` SQL
INSERT INTO temp_job_summary_flink
  SELECT
      job,
      AVG(salary) AS avg_salary,
      COUNT(*) AS nr_people
  FROM people_job
  GROUP BY job, TUMBLE(ts_field, INTERVAL '1' MINUTE);
```
``` SQL
SELECT * FROM temp_job_summary_flink;
```
Entretando o conector 'filesystem' não é o mais adequado para fornecimento de dados em streaming. Por exemplo, se tentarmos executar um código para gerar arquivos em formato CSV dentro do endereço da nossa tabela, vamos conseguir ler as inserções, porém elas não irao refletir em tempo real nas tabelas do SQL-Client, apenas o que foi inserido até o momento da execução da consulta. <br>
<br>
Use o codigo [generate.py](https://github.com/SSTDevs/Tools/blob/f76f6dc1e6dd2cd42e24e4f77c5cd35eac760a52/ApacheFlink/generate.py): 
``` python
import json 
from faker import Faker
import faker_commerce
import random
from random import randint
import pandas  as pd
import time
from pprint import pprint

fake = Faker('pt_BR')
fake.add_provider(faker_commerce.Provider)

job_list = [
  'Data Engineer', 
  'Business Analyst', 
  'Software Engineer', 
  'UX Designer', 
  'Software Engineer', 
  'DevOps Engineer', 
  'Vulnerability Analyst',
  'Solutions Architect',
  'Network Specialist',
  'Software Developer'] 

for x in range(15):
  dados = []
  for i in range(3):
    dados.append({
      'id': f'{x+1}{i}',
      'name': fake.credit_card_full().split(sep='\n')[1],
      'job': job_list[randint(0,9)],
      'salary': 1000*randint(29,210),
      'operation_time': time.strftime('%Y-%m-%d %H:%M:%S.000',time.localtime())
    })
    
  df = pd.DataFrame(dados)
  pprint(df)
  df.to_csv(f'/home/admin123/flink-1.18.0/examples/people.csv/part{x+1}_generate_csv', index=False, header=False)
  time.sleep(10)
```
``` SQL
SET 'sql-client.execution.result-mode' = 'table';
```
``` SQL
SET 'execution.runtime-mode' = 'streaming';
```
``` SQL
SELECT * FROM people_job ORDER BY ts_field ASC;
```
``` SQL
SELECT * FROM temp_job_summary_flink;
```
Observe que ambos os resultados não atualizam conforme os dados vão sendo escritos na fonte. <br>
Visto que com o conector 'filesystem' não conseguimos verificar uma visualização em streaming, poderiamos usar um conector de kafka por exemplo, mas prezando por nao baixar ferramentas adicionais, vamos utilizar o conector 'datagen'
``` SQL
CREATE TABLE IF NOT EXISTS SourceTable (
    id INT,
    encrypted_infos VARCHAR
) WITH (
    'connector' = 'datagen',
    'rows-per-second' = '1'
);
```
``` SQL
SELECT * FROM SourceTable;
```
Observe que a tabela ira gerar dados aleatórios a cada segundo por consulta. <br>
Além disso é possivel fazer operações de agregação em tempo real, por exemplo:
``` SQL
SELECT * FROM SourceTable;
```
``` SQL
SELECT avg(id) AS Avg_num,
       count(*) AS Total
FROM SourceTable;
```
Podemos criar uma view tambem no SQL do Flink da mesma forma que fazemos no SQL ANSI.
`-- Define VIEW`
``` SQL
CREATE VIEW SinkView AS
  SELECT avg(id) AS Avg_num,
         count(*) AS Total
  FROM SourceTable;
```
Portanto, apesar de algumas particularidades, vimos como é facil trabalhar com os dados através do SQL-Client do Flink, independente da carga ser batch ou streaming. <br>
A nivel de conhecimento, podemos alterar varias outras configuraçoes de dentro do SQL-Client, por exemplo:
``` SQL

-- Define user-defined functions here.
CREATE FUNCTION myUDF AS 'foo.bar.AggregateUDF';

-- Properties that change the fundamental execution behavior of a table program.
-- execution mode either 'batch' or 'streaming'
SET 'execution.runtime-mode' = 'streaming';

-- available values: 'table', 'changelog' and 'tableau'
SET 'sql-client.execution.result-mode' = 'table';

-- optional: maximum number of maintained rows
SET 'sql-client.execution.max-table-result.rows' = '10000';

-- optional: Flink's parallelism (1 by default)
SET 'parallelism.default' = '1';

-- optional: Defines Flink's job name in session
SET 'pipeline.name' = 'python-to-filesystem';

--optional: interval for periodic watermarks
SET 'pipeline.auto-watermark-interval' = '200';

-- optional: Flink's maximum parallelism
SET 'pipeline.max-parallelism' = '10';

-- optional: table program's idle state time
SET 'table.exec.state.ttl' = '1000';

SET 'restart-strategy.type' = 'fixed-delay';

-- Configuration options for adjusting and tuning table programs.
SET 'table.optimizer.join-reorder-enabled' = 'true';

SET 'table.exec.spill-compression.enabled' = 'true';

SET 'table.exec.spill-compression.block-size' = '128kb';

SET 'table.filesystem.watch-type' = 'PROCESS_ONLY_NEW_FILES';

SET 'table.filesystem.watch-interval' = '5000';

-- set sync mode
SET 'table.dml-sync' = 'false';

```

## Utilizar SQL dentro do pyflink

Mas além da utilização do SQL no client do Flink, é possivel submeter ao cluster a uma tarefa SQL em um job programavel, através do DataStreamAPI + TableAPI. <br>
Mais informaçoes do DataStreamAPI podem ser encontradas na documentação do Flink: [DataStreamAPI](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/python/datastream/intro_to_datastream_api/#emit-results-to-a-table--sql-sink-connector). <br>
<br>
No código abaixo, temos um exemplo de uso do DataStreamAPI com o TableAPI. Nesse código vamos ler uma tabela que recebe dois parametros, um numero de id qualquer e um hash de informações qualquer, tudo gerado aleatoriamente. A inteção desse codigo é fazer um tratamento para verificar esses dados. Quais são os id validos, isso é, quais os id que possuem numeração positiva.<br>

<img src="https://github.com/Igor-R-Amorim/Leega-Academy/blob/ba66e7d594a9504e41db40b6b0c1cc3db05100ae/Imagens-Relatorios/Flink/img16.png"
  style="border-radius: 10px; 
  border:1px solid;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 90%;">

O programa vai, a cada ciclo, gerando mensagens para tratar e resgata apenas as 5 linhas com id validos. Os ciclos se repetem por 5 vezes, para não executar infinitamente e acabar com os recursos da máquina eventualmente. <br>
Essas 5 mensagens tratadas serão escritas em uma tabela ao final de cada ciclo. <br>
<br>
E por fim, para nos certificarmos que as jobs iniciadas nessa instancia serão encerradas. Vamos consultar o endpoint do nosso cluster e verificar quais jobs estão com o tempo de encerramento inifnito e cancela-los.

[Example_Table_API.py](https://github.com/SSTDevs/Tools/blob/7daade550a95d493f04224efaeda31af809c70d8/ApacheFlink/Example_Table_API.py)
``` python
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import *
from pprint import pprint
import time, requests

s_env = StreamExecutionEnvironment.get_execution_environment()
table_env = StreamTableEnvironment.create(stream_execution_environment=s_env)

# Create a sink table
table_env.execute_sql("""
CREATE TABLE SinkTable (
  id INT,
  encrypted_infos VARCHAR
) WITH (
    'connector' = 'filesystem',
    'path' = 'file:///home/admin123/flink-1.18.0/examples/tableAPI.csv',
    'format' = 'csv',
    'csv.ignore-parse-errors' = 'true',
    'csv.allow-comments' = 'true',
    'csv.field-delimiter' = ','
)
""")
print("Tabela SinkTable criada via SQL")

# Create a source table
table_env.execute_sql("""
CREATE TABLE IF NOT EXISTS SourceTable (
id INT,
encrypted_infos VARCHAR
) WITH (
'connector' = 'datagen',
'rows-per-second' = '1'
)
""")
print("Tabela SourceTable criada via SQL")
print('-------------------\n')
table_env.sql_query("SELECT * FROM SourceTable WHERE id>0 LIMIT 5").execute_insert("SinkTable")

limite = 0
while True:
    limite+=1
    if limite > 5:
        break
    
# Append table data to stream env
    time.sleep(1)
    ds = table_env.to_append_stream(
            table_env.from_path('SourceTable'),
            Types.ROW([Types.INT(), Types.STRING()])
         )
# Look for 2 positives id
    ds_row = []
    with ds.execute_and_collect() as results:
        i = 0;    
        for result in results:
            #print(result[0])
            if result[0] > 0:
                ds_row.append(result)
                i=i+1
            if i == 5: 
                break
    print("Dados capturados do Table_env para o Stream_env com sucesso\n-------------------\n")

    table_env.get_config().get_configuration().set_string("pipeline.name", "ds_row-to-collection")
    #print(f"{ds_row} \n")
    collect = s_env.from_collection(ds_row) \
                   .execute_and_collect()
    ds = s_env.from_collection(collect, Types.ROW([Types.INT(), Types.STRING()]))
    #print("Esquema do DataStream:\n", ds.get_type())
    # # print dos dados:
    #for c in collect:
    #    print(c)
    print("Conversão dos dados para datastream executado com sucesso\n-------------------\n")

    time.sleep(1)
    table_env.get_config().get_configuration().set_string("pipeline.name", "collection-to-SinkTable")
    table_env.from_data_stream(ds).execute_insert("SinkTable").wait()
    print("Inserção do dado trabalhado na tabela destino com sucesso\n-------------------\n")

    table_env.get_config().get_configuration().set_string("pipeline.name", "print-SinkTable")
    table_env.execute_sql("SELECT * FROM SinkTable").print()
    print("Exibição dos dados selecionados que foram adicionados na tabela\n-------------------\n")

print("\nVerificando jobs ainda ativos\n-------------------\n")
running_jobs = []
JobId = []
JobName = []
response = requests.get("http://localhost:8081/jobs/overview")
if response.status_code == 200:
    data = response.json()
    #pprint(data)    
    for job in data['jobs']:
        if job['state'] == 'RUNNING':
            running_jobs.append(job) 
    #pprint(running_jobs)
    for job in running_jobs:
        if job['end-time'] == -1:
            JobId.append(job['jid'])
            JobName.append(job['name'])
else:
    print(f"Erro na solicitação. Código de status: {response.status_code}")

#print(JobId)
for i,id in enumerate(JobId):
    response = requests.patch(f'http://localhost:8081/jobs/{id}?mode=cancel')
    if response.status_code == 202:
        print(f"O cancelamento do Job ({id} : {JobName[i]}), \nfoi aceito com sucesso.")
    else:
        print(f"Falha ao cancelar o Job ({id} : {JobName[i]}). \nCódigo de status: {response.status_code}")
print("\n-------------------\n")

```
<kbd>Antes de executar esse programa confirme se a sua versão do python nesse linux já possui os pacotes <strong>pip</strong> de time, pprint e requests</kbd> 




<br><br>
>Obs.: Caso esteja tendo problema para executar algum código python, experimente utilizar o comando pip para instalar o pyflink.

```
sudo apt-get install python3-pip
python3 -m pip install apache-flink
```




<br><br><br>
<br><br><br>
<br><br><br>
<br><br><br>
