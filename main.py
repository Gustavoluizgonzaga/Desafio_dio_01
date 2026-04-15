
import textwrap
from datetime import datetime
from abc import ABC, abstractmethod
from functools import wraps

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor
        self._data = None

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes.copy()

    def adicionar_transacao(self, transacao):
        transacao.data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self._transacoes.append(transacao)


class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False

        if valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        else:
            print("Valor inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        else:
            print("Valor inválido.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._data_ultima = None
        self._transacoes_hoje = 0

    def depositar(self, valor):
        hoje = datetime.now().date()
        if self._data_ultima != hoje:
            self._transacoes_hoje = 0
            self._data_ultima = hoje

        if self._transacoes_hoje >= 10:
            print("Operação falhou! Você excedeu o número de transações permitidas para hoje.")
            return False

        sucesso = super().depositar(valor)
        if sucesso:
            self._transacoes_hoje += 1
        return sucesso

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.") 

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

def listar_contas(contas):
    for conta in contas:
        print("-" * 30)
        print(textwrap.dedent(str(conta)))
   
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
   
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: ")) 
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            tipo = transacao.__class__.__name__
            valor = transacao.valor
            extrato += f"{tipo}: R$ {valor:.2f}\n"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")       
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe um cliente com esse CPF!")
        return 
    
    nome = input("Informe o nome do cliente: ")
    data_nascimento = input("Informe a data de nascimento do cliente (dd-mm-aaaa): ")
    endereco = input("Informe o endereço do cliente: (logradouro, número, bairro, cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)

    print("Cliente criado com sucesso!")

def criar_conta(contas,numero_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n Conta criada com sucesso!")
    

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
    

def recuperar_conta_cliente(cliente): 
    if not cliente.contas:
        print("Cliente não possui conta!")
        return 

    if len(cliente.contas) == 1:
        return cliente.contas[0] 

def main():

    """
    Função principal do programa, responsável por mostrar o menu ao usuário e
    realizar as operações escolhidas pelo mesmo.

    """

    menu = """
   ================== MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[sc] Selecionar conta
[lc] Listar contas
[nu] Novo usuário
[nc] Nova conta
[q] Sair

=> """

    
    clientes = []
    contas = []
    current_account = None

    while True:
        opcao = input(menu)

        if opcao == "d":
            depositar(clientes)           

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
           criar_cliente(clientes)

        elif opcao == "nc":
           numero_conta = len(contas) + 1
           criar_conta(contas, numero_conta, clientes)
           
        elif opcao == "q":
            print("Obrigado por utilizar nossos serviços!\n")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()