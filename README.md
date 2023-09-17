# TSI-RemoteProcedureCall
 Sistema RPC cuja as funcionalidades irão aumentar semanalmente. O projeto é uma atividade proposta na disciplina de Sistemas Distribuidos.

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
