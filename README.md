<h1 align="center"> 
Remote Procedure Call
</h1>
<h4 align="center">
Sistema RPC cuja as funcionalidades irão aumentar semanalmente. 
 
O projeto é uma atividade proposta na disciplina de Sistemas Distribuidos.
</h4>

<br/>

<div align="center" >
 
![image](https://github.com/ViniciusJPSilva/TSI-RemoteProcedureCall/assets/81810017/2ada99f6-64ba-401a-8479-0fd7f90694fd)

</div>

<hr/>

<h3>
Instalação das Bibliotecas
</h3>

É recomendado que seja criado um ambiente virtual para execução da aplicação, conforme o comando abaixo:
```py
python -m venv venv
```

<br/>

Acesse o ambiente virtual (Powershell):
```py
.\venv\Scripts\Activate.ps1  
```

<br/>

Instale os pacotes python:
```py 
pip install -r requirements.txt
```

<br/>

<hr>

## Semana 1

O servidor RPC deverá conter as operações básicas de soma, subtração, multiplicação e divisão e o cliente deverá possuir as respectivas chamadas.

<hr>

## Semana 2

1) Adicione ao RPC a operação is_prime(number: int) -> bool
2) Modifique a assinatura da operação, para que a mesma recebe uma lista de números inteiros como argumento, e retorne uma lista de booleanos.
3) Exiba todos os números primos entre 10 e 10000.
4) Adicione multiprocessamento à implementação da operação no servidor, de modo que ela seja capaz de analisar se vários números da lista são primos em paralelo.
5) Utilize o módulo time para contabilizar o tempo de execução da operação com e sem multiprocessamento, para demonstrar que a versão paralela é realmente mais rápida.
   
<hr>

## Semana 3

Implementação um sistema de cache em memória no cliente para todas as operações do RPC.

<hr>

## Semana 4

1) Crie uma constante de código que defina o tempo mínimo para a sincronização do cache em memória com o cache em disco.
2) Crie uma constante de código que defina o número máximo de registros armazenados no cache em disco. Caso seu tamanho ultrapasse esse valor, os registros mais antigos deverão ser substituídos pelos registros mais novos.

<hr>

## Semana 5

Desenvolva a operação remota:

last_news_if_barbacena(qtd_noticias : int) -> []

1) A operação deverá coletar os títulos das qtd_noticias mais recentes da página de notícias do Campus Barbacena: https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int=0
2) As operação deverá utilizar o mesmo mecanismo de cache das demais.
3) Altere a operação de modo que a coleta das diversas páginas de notícias seja realizada com paralelismo.
4) Reflita sobre o problema em se utilizar o mesmo mecanismo de cache das outras operações.

<hr>

## Semana 6

1) O mecanismo de cache de notícias deverá lidar com requisições onde o número de notícias solicitadas seja menor que um número previamente solicitado, aproveitando esses dados.
2) O cache deverá ficar consistente com atualizações no site de notícias do IF, usando um modelo de restrição de 5 minutos.

<hr>

## Semanas 7 e 8

1) O cliente RPC agora será instanciado recebendo o IP e a porta do servidor de nomes, e não mais do servidor de operações.
2) A consulta ao servidor de nomes deverá ser via UDP.
3) O servidor de nomes deverá retornar uma lista com os IPs dos servidores de operação que implementam a operação solicitada.
4) O cliente deverá escolher um desses IPs aleatoriamente, para realizar o balanceamento de carga das requisições.

<hr>

## Semana 9 e 10

1) Chamada remota valida_CPF(str:cpf) -> bool
2) Sistema de log para auditoria: em um único arquivo texto (por servidor de operações), armazenar para cada requisição recebida (em uma linha): timestamp, IP do cliente, nome da operação, tempo de resposta.
3) Criar um shell script que leia um arquivo de log nesse formato e exiba todos os IPs únicos que fizeram requisições.
4) Criar um notebook no Kaggle ou Google Colab, fazer o upload de um arquivo de log, transformar seus dados em um dataframe Pandas. A partir dele, gerar:

```py 
a) um gráfico de pizza com a porcentagem de chamadas por operação.
b) um gráfico de barras (horizontal) com a quantidade de requisições por endereço IP.
c) um gráfico de barras (vertical) com a quantidade de requisições por horário do dia.
d) um gráfico de dispersão onde cada ponto é uma requisição, o eixo x é a operação chamada e o eixo y é o tempo de resposta.
```

5) Implementar comunicação segura nas chamadas de procedimento remoto, usando criptografia. Você pode usar criptografia nas mensagens ou sockets seguros (SSL).

6) Link do Collab: <a href="https://colab.research.google.com/drive/14BeH1GfkLQ574NJQ2hREjLDqW-QPHN2L?usp=sharing">Clique aqui!</a>

<hr>

## Semana 11 - Final

1) Crie uma GUI para o usuário interagir com o RPC (chamar as operações). Ela pode ser desktop ou web, em linguagem/toolkit livre.

