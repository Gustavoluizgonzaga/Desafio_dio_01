# Desafio DIO 01 - Sistema Bancário em Python

Este é um projeto simples de um sistema bancário desenvolvido em Python como parte do desafio da DIO (Digital Innovation One). O sistema permite realizar operações básicas de um banco, como depósitos, saques, visualização de extratos, criação de usuários e contas correntes.

## Funcionalidades

- **Depósito**: Permite depositar valores na conta.
- **Saque**: Permite sacar valores, com limite de R$ 500 por saque e no máximo 3 saques por dia.
- **Extrato**: Exibe o histórico de movimentações e o saldo atual.
- **Novo Usuário**: Cria um novo usuário com nome, CPF, data de nascimento e endereço.
- **Nova Conta**: Cria uma nova conta corrente vinculada a um usuário existente.

## Requisitos

- Python 3.x instalado no sistema.

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/Desafio_dio_01.git
   ```

2. Navegue até o diretório do projeto:
   ```
   cd Desafio_dio_01
   ```

3. (Opcional) Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

4. Execute o programa:
   ```
   python main.py
   ```

## Como Usar

Após executar o programa, você verá um menu com as opções disponíveis. Digite a letra correspondente à operação desejada:

- `d` para depósito
- `s` para saque
- `e` para extrato
- `nu` para novo usuário
- `nc` para nova conta
- `q` para sair

Siga as instruções na tela para inserir os valores necessários.

## Estrutura do Projeto

- `main.py`: Arquivo principal contendo toda a lógica do sistema bancário.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Abra uma issue ou envie um pull request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.