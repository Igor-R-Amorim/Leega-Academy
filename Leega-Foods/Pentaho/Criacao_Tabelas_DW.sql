CREATE DATABASE IF NOT EXISTS leegadb_g1;
USE leegadb_g1;

DROP TABLE IF EXISTS DIM_Categoria, DIM_Cliente, DIM_Funcionario, DIM_Produto, DIM_Transportador, DIM_Fornecedor, FT_Vendas;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Categoria
(
  ID_Cat INT
, Nome_Cat TINYTEXT
, Descr_Cat TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Cliente
(
  ID_Cli TINYTEXT
, Nome_Cli TINYTEXT
, Cidade_Cli TINYTEXT
, Regiao_Cli TINYTEXT
, Pais_Cli TINYTEXT
, Tipo_cli TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Funcionario
(
  ID_Func INT
, Nome_Func TINYTEXT
, Cidade_Func TINYTEXT
, Regiao_Func TINYTEXT
, Pais_Func TINYTEXT
, Time_func TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Produto
(
  ID_Prod INT
, Nome_Prod TINYTEXT
, ID_Forn INT
, QtdeporUnid_Prod TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Transportador
(
  ID_Transp INT
, Nome_Transp TINYTEXT
, Pais_Transp TINYTEXT
, Tipo_Transp TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.DIM_Fornecedor
(
  ID_Forn INT
, Nome_Forn TINYTEXT
, Cidade_Forn TINYTEXT
, Regiao_Forn TINYTEXT
, Pais_Forn TINYTEXT
, Tipo_Forn TINYTEXT
)
;

CREATE TABLE IF NOT EXISTS leegadb_g1.FT_Vendas
(
  ID_Pedido INT
, ID_Cli TINYTEXT
, ID_Func INT
, ID_Transp INT
, ID_Prod INT
, PrecoUnit_Prod DOUBLE
, Qtde_Prod DOUBLE
, PercDesc_Prod DOUBLE
, Ano_Ped VARCHAR(100)
, Mes_Ped VARCHAR(100)
, ID_Forn INT
, ID_Cat INT
, VlrFrete_Prod DOUBLE
, VlrTot_Prod DOUBLE
, CidEntrega_Pedido TINYTEXT
, PaisEntrega_Pedido TINYTEXT
)
;