# API Engenharia de Software - CSIndex

Nomes: 
Henrique Eustáquio Lopes Ferreira     2015068990
Tiago Melo Tannus                     2012079762

A API desenhada foi projetada levando em consideração princípios de simplicidade e organização de código. Em termos de tecnologia, usou-se Python v2.7.10 (default, Jul 15 2017, 17:16:57) [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] para a linguagem host. Para o framework da API, usamos Flask v1.0.2, por ser um pacote popular, com grande e ativa comunidade e pela velocidade de implementação que nos possibilitou. Toda a API foi implementada em um arquivo, api.py e por default o servidor local é executado em modo de debug.

Basicamente, por ser quase um protótipo, optamos por utilizar a URL padrão /api/__x__, em que __x__ corresponde à questão do enunciado do trabalho. Isso não só facilita legibilidade, mas também testes, considerando que não existe, nesse caso, uma versão definitiva e que o código da API pode e deve ser continuamente aprimorado, sabendo-se que trata-se de somente um arquivo.

Temos, enfim, a escolha de uma url para cada questão. Isso foi proposto pela simplicidade de implementação. O método HTTP utilizado foi o GET, já que só temos retrieving de dados e não precisamos de outras funcionalidades no momento.

Em termos de REST e HTTP, temos:


Método HTTP         URL                   Action
GET                 http://api/1          Número de publicações em uma determinada conferência de uma área
GET                 http://api/2          Número de publicações no conjunto de conferências de uma área
GET                 http://api/3          Scores de todos os departamentos em uma área
GET                 http://api/4          Score de um determinado departamento em uma área
GET                 http://api/5          Número de professores que publicam em uma determinada área (organizados por departamentos)
GET                 http://api/6          Número de professores de um determinado departamento que publicam em uma áre
GET                 http://api/7          Todos os papers de uma área (ano, título, deptos e autores)
GET                 http://api/8          Todos os papers de uma área em um determinado ano
GET                 http://api/9          Todos os papers de um departamento em uma área
GET                 http://api/10         Todos os papers de um professor (dado o seu nome)

Por fim, em termos de códigos de erros, optamos por utilizar o 404 para Not Found, conforme o padrão HTTP. Remodelamos para .json para facilitar a leitura do erro.
