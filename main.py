def depositar(saldo, extrato, valor):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    print(f"Saldo total: R$ {saldo:.2f}")
    return saldo, extrato


def sacar(saldo, extrato, valor, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1
    print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    print(f"Saldo restante: R$ {saldo:.2f}")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios, nome, cpf, data_nascimento, endereco):
    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
    }

    usuarios.append(usuario)
    print(f"Usuário {nome} criado com sucesso.")
    return True


def criar_conta_corrente(contas, agencia, numero, usuarios, cpf_cliente):
    usuario = next((u for u in usuarios if u["cpf"] == cpf_cliente), None)

    if usuario is None:
        print("Erro: usuário não encontrado para o CPF informado.")
        return False

    if any(conta["numero"] == numero and conta["agencia"] == agencia for conta in contas):
        print("Erro: conta já existe.")
        return False

    conta = {
        "agencia": agencia,
        "numero": numero,
        "cliente": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0,
    }

    contas.append(conta)
    print(f"Conta corrente {agencia}/{numero} criada para {usuario['nome']}.")
    return True


def main():

    """
    Função principal do programa, responsável por mostrar o menu ao usuário e
    realizar as operações escolhidas pelo mesmo.

    """

    menu = """
    ---Bem-vindo ao Banco Python---
    Escolha a operação desejada:

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair

=> """

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, extrato, valor)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo,
                extrato,
                valor,
                limite,
                numero_saques,
                LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            nome = input("Nome do cliente: ")
            while True:
                cpf = input("CPF do cliente: ")
                if not cpf.isdigit():
                    print("Erro: CPF deve conter apenas números.")
                elif any(usuario["cpf"] == cpf for usuario in usuarios):
                    print("Erro: já existe usuário com esse CPF.")
                else:
                    break
            while True:
                data_nascimento = input("Data de nascimento: ")
                if not data_nascimento.isdigit():
                    print("Erro: Data de nascimento deve conter apenas números.")
                else:
                    break
            endereco = input("Endereço (logradouro, nº, bairro, cidade/sigla do estado): ")
            criar_usuario(usuarios, nome, cpf, data_nascimento, endereco)

        elif opcao == "nc":
            agencia = input("Agência: ")
            numero = input("Número da conta: ")
            cpf_cliente = input("CPF do cliente para vincular a conta: ")
            criar_conta_corrente(contas, agencia, numero, usuarios, cpf_cliente)

        elif opcao == "q":
            print("Obrigado por utilizar nossos serviços!\n")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()