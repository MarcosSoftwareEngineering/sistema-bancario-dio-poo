"""
BANCO DIO - Banking System OOP
DIO Challenge | Python Trail

Implements a complete banking system using Object-Oriented Programming principles:
- Abstract classes and interfaces (Transacao)
- Inheritance (ContaCorrente -> Conta, PessoaFisica -> Cliente)
- Polymorphism (ContaCorrente.sacar overrides Conta.sacar)
- Encapsulation (private attributes via name mangling + properties)
"""

from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Optional
import os
import time


# ══════════════════════════════════════════════
#  TERMINAL UTILITIES — ANSI colors and UI helpers
# ══════════════════════════════════════════════

class Cor:
    """ANSI escape codes for terminal colors and text styles."""
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    PRETO    = "\033[30m"
    VERDE    = "\033[32m"
    AMARELO  = "\033[33m"
    AZUL     = "\033[34m"
    MAGENTA  = "\033[35m"
    CIANO    = "\033[36m"
    BRANCO   = "\033[37m"
    VERMELHO = "\033[31m"
    BG_VERDE    = "\033[42m"
    BG_VERMELHO = "\033[41m"
    BG_AMARELO  = "\033[43m"


def limpar():
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def linha(char="─", largura=52):
    """Print a horizontal divider line using the given character."""
    print(f"{Cor.DIM}{char * largura}{Cor.RESET}")


def titulo_box(texto, cor=None):
    """Print a centered section title with decorative borders.

    Args:
        texto: The title text to display.
        cor: ANSI color code for the title. Defaults to blue.
    """
    if cor is None:
        cor = Cor.AZUL
    w = 52
    pad = (w - len(texto) - 2) // 2
    print(f"\n{cor}{Cor.BOLD}{'─' * w}{Cor.RESET}")
    print(f"{cor}{Cor.BOLD}{' ' * pad} {texto}{Cor.RESET}")
    print(f"{cor}{Cor.BOLD}{'─' * w}{Cor.RESET}")


def badge(texto, cor_bg, cor_txt=None):
    """Return a colored inline badge string (e.g. [OK], [ERRO]).

    Args:
        texto: Label text inside the badge.
        cor_bg: Background color ANSI code.
        cor_txt: Text color ANSI code. Defaults to white.

    Returns:
        Formatted badge string with ANSI codes.
    """
    if cor_txt is None:
        cor_txt = Cor.BRANCO
    return f"{cor_bg}{cor_txt}{Cor.BOLD} {texto} {Cor.RESET}"


def ok(msg):
    """Print a success message with a green OK badge."""
    print(f"\n  {badge('OK', Cor.BG_VERDE)}  {Cor.VERDE}{msg}{Cor.RESET}")


def erro(msg):
    """Print an error message with a red ERRO badge."""
    print(f"\n  {badge('ERRO', Cor.BG_VERMELHO)}  {Cor.VERMELHO}{msg}{Cor.RESET}")


def aviso(msg):
    """Print a warning message with a yellow AVISO badge."""
    print(f"\n  {badge('AVISO', Cor.BG_AMARELO, Cor.PRETO)}  {Cor.AMARELO}{msg}{Cor.RESET}")


def pausar():
    """Pause execution and wait for the user to press Enter."""
    print(f"\n  {Cor.DIM}Pressione Enter para continuar...{Cor.RESET}", end="")
    input()


def cabecalho():
    """Clear the screen and render the application header banner."""
    limpar()
    print(f"\n{Cor.AZUL}{Cor.BOLD}", end="")
    print("  +==================================================+")
    print("  |          BANCO DIO  -  Sistema POO               |")
    print("  +==================================================+")
    print(f"{Cor.RESET}")


def entrada(prompt):
    """Display a styled prompt and return the user's input (stripped).

    Args:
        prompt: The label text shown before the input cursor.

    Returns:
        Stripped string entered by the user.
    """
    return input(f"  {Cor.CIANO}>{Cor.RESET}  {prompt}: ").strip()


def entrada_valor(prompt):
    """Prompt the user for a positive numeric value.

    Accepts both comma and dot as decimal separators.

    Args:
        prompt: The label text shown before the input cursor.

    Returns:
        Parsed float if valid, or None if the input is invalid.
    """
    raw = entrada(prompt)
    try:
        v = float(raw.replace(",", "."))
        if v <= 0:
            raise ValueError
        return v
    except ValueError:
        erro("Valor invalido. Use numeros positivos (ex: 150 ou 150.50).")
        return None


def animacao_carregando(msg="Processando"):
    """Display a spinner animation in the terminal while simulating processing.

    Args:
        msg: Message shown alongside the spinner.
    """
    frames = ["|", "/", "-", "\\"]
    for _ in range(8):
        for f in frames:
            print(f"\r  {Cor.CIANO}{f}{Cor.RESET}  {msg}...", end="", flush=True)
            time.sleep(0.04)
    print("\r" + " " * 40 + "\r", end="")


def mini_card_conta(conta):
    """Render a compact visual card showing account type, number, and balance.

    Args:
        conta: A Conta (or subclass) instance to display.
    """
    from __main__ import ContaCorrente
    tipo = "Conta Corrente" if isinstance(conta, ContaCorrente) else "Conta"
    cor  = Cor.AZUL if isinstance(conta, ContaCorrente) else Cor.VERDE
    print(f"\n  {cor}+{'─'*38}+{Cor.RESET}")
    print(f"  {cor}|{Cor.RESET}  {Cor.BOLD}{tipo:<36}{cor}|{Cor.RESET}")
    print(f"  {cor}|{Cor.RESET}  Ag. {conta.agencia}  -  Conta {conta.numero:04d}{'':>17}{cor}|{Cor.RESET}")
    saldo_str = f"R$ {conta.saldo:>10,.2f}"
    print(f"  {cor}|{Cor.RESET}  Saldo: {Cor.VERDE}{Cor.BOLD}{saldo_str:<29}{Cor.RESET}{cor}|{Cor.RESET}")
    print(f"  {cor}+{'─'*38}+{Cor.RESET}")


# ══════════════════════════════════════════════
#  INTERFACE — Transacao (Abstract Base Class)
# ══════════════════════════════════════════════

class Transacao(ABC):
    """Abstract interface that every banking transaction must implement.

    Concrete subclasses (Deposito, Saque) must define:
    - valor: the monetary amount of the transaction.
    - registrar: the logic to apply the transaction to an account.
    """

    @property
    @abstractmethod
    def valor(self):
        """Return the transaction amount."""
        ...

    @abstractmethod
    def registrar(self, conta):
        """Apply this transaction to the given account.

        Args:
            conta: The Conta instance to operate on.
        """
        ...


class Deposito(Transacao):
    """Concrete transaction that credits funds into an account."""

    def __init__(self, valor):
        """
        Args:
            valor: Positive float representing the deposit amount.
        """
        self._valor = valor

    @property
    def valor(self):
        """Return the deposit amount."""
        return self._valor

    def registrar(self, conta):
        """Deposit funds and record the transaction in the account history.

        Args:
            conta: The target Conta instance.
        """
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    """Concrete transaction that debits funds from an account."""

    def __init__(self, valor):
        """
        Args:
            valor: Positive float representing the withdrawal amount.
        """
        self._valor = valor

    @property
    def valor(self):
        """Return the withdrawal amount."""
        return self._valor

    def registrar(self, conta):
        """Withdraw funds and record the transaction in the account history.

        Args:
            conta: The target Conta instance.
        """
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ══════════════════════════════════════════════
#  Historico — Transaction log
# ══════════════════════════════════════════════

class Historico:
    """Stores an ordered log of all transactions performed on an account."""

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        """Return the list of transaction records (read-only access pattern)."""
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Append a transaction snapshot to the history log.

        Each entry is a dict with keys: 'tipo', 'valor', 'data'.

        Args:
            transacao: A Transacao instance that was successfully applied.
        """
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })


# ══════════════════════════════════════════════
#  Conta — Base account class
# ══════════════════════════════════════════════

class Conta:
    """Base class representing a generic bank account.

    Provides core deposit and withdrawal logic.
    Subclasses (e.g. ContaCorrente) can override sacar to add constraints.
    """

    def __init__(self, cliente, numero):
        """
        Args:
            cliente: The Cliente instance who owns this account.
            numero: Unique integer account number.
        """
        self._saldo = 0.0          # Current balance, always >= 0
        self._numero = numero       # Account number
        self._agencia = "0001"      # Branch code (fixed for this system)
        self._cliente = cliente     # Owner reference
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Factory method: create and return a new account instance.

        Using a classmethod allows subclasses to inherit the factory
        and still return the correct type.

        Args:
            cliente: The Cliente instance who owns this account.
            numero: Unique integer account number.

        Returns:
            A new instance of this class (or subclass).
        """
        return cls(cliente, numero)

    # ── Read-only properties (encapsulation) ──

    @property
    def saldo(self): return self._saldo

    @property
    def numero(self): return self._numero

    @property
    def agencia(self): return self._agencia

    @property
    def cliente(self): return self._cliente

    @property
    def historico(self): return self._historico

    def sacar(self, valor):
        """Debit the account by the given amount.

        Validates that the value is positive and that sufficient
        balance exists before performing the debit.

        Args:
            valor: Positive float amount to withdraw.

        Returns:
            True if the withdrawal succeeded, False otherwise.
        """
        if valor <= 0:
            erro("Valor invalido para saque.")
            return False
        if valor > self._saldo:
            erro("Saldo insuficiente.")
            return False
        self._saldo -= valor
        animacao_carregando("Processando saque")
        ok(f"Saque de R$ {valor:,.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        """Credit the account by the given amount.

        Args:
            valor: Positive float amount to deposit.

        Returns:
            True if the deposit succeeded, False otherwise.
        """
        if valor <= 0:
            erro("Valor invalido para deposito.")
            return False
        self._saldo += valor
        animacao_carregando("Processando deposito")
        ok(f"Deposito de R$ {valor:,.2f} realizado com sucesso!")
        return True

    def __str__(self):
        return (
            f"Agencia : {self._agencia}\n"
            f"Conta   : {self._numero:04d}\n"
            f"Titular : {self._cliente.nome}"
        )


# ══════════════════════════════════════════════
#  ContaCorrente — Checking account (inherits Conta)
# ══════════════════════════════════════════════

class ContaCorrente(Conta):
    """Checking account with per-transaction withdrawal limit and daily cap.

    Demonstrates polymorphism by overriding Conta.sacar to enforce:
    - Maximum amount per withdrawal (_limite).
    - Maximum number of withdrawals per day (_limite_saques).
    """

    LIMITE_PADRAO = 500.0    # Default max amount per withdrawal
    LIMITE_SAQUES_PADRAO = 3 # Default max withdrawals per day

    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        """
        Args:
            cliente: The Cliente instance who owns this account.
            numero: Unique integer account number.
            limite: Max amount allowed per single withdrawal.
            limite_saques: Max number of withdrawals allowed per day.
        """
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self): return self._limite

    @property
    def limite_saques(self): return self._limite_saques

    def _saques_hoje(self):
        """Count how many withdrawals have been recorded in the history.

        Returns:
            Integer count of Saque entries in the transaction log.
        """
        return sum(1 for t in self.historico.transacoes if t["tipo"] == "Saque")

    def sacar(self, valor):
        """Override Conta.sacar to add checking-account restrictions.

        Checks the per-transaction limit and daily withdrawal cap
        before delegating to the parent implementation.

        Args:
            valor: Positive float amount to withdraw.

        Returns:
            True if all validations pass and the withdrawal succeeds.
        """
        if valor <= 0:
            erro("Valor invalido para saque.")
            return False
        if valor > self._limite:
            erro(f"Valor excede o limite por saque (R$ {self._limite:,.2f}).")
            return False
        if self._saques_hoje() >= self._limite_saques:
            erro(f"Limite de {self._limite_saques} saques diarios atingido.")
            return False
        # Delegate balance check and debit to the parent class
        return super().sacar(valor)

    def __str__(self):
        restantes = self._limite_saques - self._saques_hoje()
        return (
            super().__str__() + "\n"
            f"Tipo    : Conta Corrente\n"
            f"Limite  : R$ {self._limite:,.2f}\n"
            f"Saques  : {restantes}/{self._limite_saques} restantes hoje"
        )


# ══════════════════════════════════════════════
#  Cliente — Base customer class
# ══════════════════════════════════════════════

class Cliente:
    """Base class representing a bank customer.

    Holds an address and a list of associated accounts.
    Subclasses (e.g. PessoaFisica) add identity information.
    """

    def __init__(self, endereco):
        """
        Args:
            endereco: Full address string for this customer.
        """
        self._endereco = endereco
        self._contas = []  # List of Conta instances owned by this customer

    @property
    def endereco(self): return self._endereco

    @property
    def contas(self): return self._contas

    @property
    def nome(self):
        """Customer display name. Overridden by subclasses."""
        return "Cliente"

    def realizar_transacao(self, conta, transacao):
        """Execute a transaction on one of the customer's accounts.

        Delegates to the Transacao object so that each transaction type
        handles its own registration logic (Open/Closed Principle).

        Args:
            conta: The target Conta instance.
            transacao: A Transacao instance (Deposito or Saque).
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Associate a new account with this customer.

        Args:
            conta: A Conta instance to add to the customer's portfolio.
        """
        self._contas.append(conta)


# ══════════════════════════════════════════════
#  PessoaFisica — Individual customer (inherits Cliente)
# ══════════════════════════════════════════════

class PessoaFisica(Cliente):
    """Represents an individual (natural person) bank customer.

    Extends Cliente with Brazilian individual taxpayer data:
    CPF, full name, and date of birth.
    """

    def __init__(self, nome, cpf, data_nascimento, endereco):
        """
        Args:
            nome: Full legal name.
            cpf: Brazilian CPF number (digits only; formatting is stripped).
            data_nascimento: Date of birth as a datetime.date object.
            endereco: Full address string.
        """
        super().__init__(endereco)
        self._nome = nome
        # Store CPF as digits only to simplify comparisons
        self._cpf = cpf.replace(".", "").replace("-", "")
        self._data_nascimento = data_nascimento

    @property
    def nome(self): return self._nome

    @property
    def cpf(self): return self._cpf

    @property
    def data_nascimento(self): return self._data_nascimento

    def _cpf_fmt(self):
        """Return the CPF formatted as XXX.XXX.XXX-XX for display purposes."""
        c = self._cpf
        if len(c) == 11:
            return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
        return c

    def __str__(self):
        return (
            f"Nome    : {self._nome}\n"
            f"CPF     : {self._cpf_fmt()}\n"
            f"Nasc.   : {self._data_nascimento.strftime('%d/%m/%Y')}\n"
            f"End.    : {self._endereco}"
        )


# ══════════════════════════════════════════════
#  FLOW HELPERS — Reusable lookup utilities
# ══════════════════════════════════════════════

def _filtrar_cliente(cpf, clientes):
    """Find a PessoaFisica in the list by CPF (ignores formatting).

    Args:
        cpf: CPF string (with or without dots/dashes).
        clientes: List of Cliente instances to search.

    Returns:
        The matching Cliente instance, or None if not found.
    """
    cpf = cpf.replace(".", "").replace("-", "").strip()
    for c in clientes:
        if isinstance(c, PessoaFisica) and c.cpf == cpf:
            return c
    return None


def _recuperar_conta(cliente):
    """Resolve which account to operate on for the given customer.

    If the customer has only one account it is returned directly.
    If there are multiple accounts, a numbered list is shown and
    the user is asked to choose.

    Args:
        cliente: The Cliente instance whose accounts to query.

    Returns:
        The selected Conta instance, or None if unavailable / invalid choice.
    """
    if not cliente.contas:
        aviso("Este cliente nao possui contas cadastradas.")
        return None
    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Multiple accounts: let the user pick
    print(f"\n  {Cor.BOLD}Contas disponíveis:{Cor.RESET}")
    for i, conta in enumerate(cliente.contas, 1):
        tipo = "CC" if isinstance(conta, ContaCorrente) else "CA"
        print(f"  {Cor.CIANO}[{i}]{Cor.RESET} Ag. {conta.agencia} - "
              f"Conta {conta.numero:04d} ({tipo}) - "
              f"Saldo: R$ {conta.saldo:,.2f}")
    try:
        idx = int(entrada("Numero da conta desejada")) - 1
        if 0 <= idx < len(cliente.contas):
            return cliente.contas[idx]
        erro("Opcao invalida.")
    except ValueError:
        erro("Entrada invalida.")
    return None


def _pegar_cliente(clientes):
    """Prompt for a CPF and return the matching customer.

    Args:
        clientes: List of Cliente instances to search.

    Returns:
        The matching Cliente, or None if not found.
    """
    cpf = entrada("CPF do cliente (so numeros)")
    cliente = _filtrar_cliente(cpf, clientes)
    if not cliente:
        erro("Cliente nao encontrado.")
    return cliente


# ══════════════════════════════════════════════
#  MENU ACTIONS — One function per menu option
# ══════════════════════════════════════════════

def depositar(clientes):
    """Handle the Deposit menu option.

    Locates the customer and account, shows the current balance,
    prompts for an amount, and executes a Deposito transaction.

    Args:
        clientes: List of registered Cliente instances.
    """
    cabecalho()
    titulo_box("DEPOSITO", Cor.VERDE)
    cliente = _pegar_cliente(clientes)
    if not cliente: return pausar()
    conta = _recuperar_conta(cliente)
    if not conta: return pausar()
    mini_card_conta(conta)                               # Show balance before
    valor = entrada_valor("Valor do deposito  R$")
    if valor is None: return pausar()
    cliente.realizar_transacao(conta, Deposito(valor))
    mini_card_conta(conta)                               # Show balance after
    pausar()


def sacar(clientes):
    """Handle the Withdrawal menu option.

    Locates the customer and account, shows the current balance,
    prompts for an amount, and executes a Saque transaction.

    Args:
        clientes: List of registered Cliente instances.
    """
    cabecalho()
    titulo_box("SAQUE", Cor.AMARELO)
    cliente = _pegar_cliente(clientes)
    if not cliente: return pausar()
    conta = _recuperar_conta(cliente)
    if not conta: return pausar()
    mini_card_conta(conta)                               # Show balance before
    valor = entrada_valor("Valor do saque     R$")
    if valor is None: return pausar()
    cliente.realizar_transacao(conta, Saque(valor))
    mini_card_conta(conta)                               # Show balance after
    pausar()


def exibir_extrato(clientes):
    """Handle the Statement menu option.

    Displays all transactions with color-coded debit/credit indicators,
    followed by running totals for deposits and withdrawals.

    Args:
        clientes: List of registered Cliente instances.
    """
    cabecalho()
    titulo_box("EXTRATO", Cor.CIANO)
    cliente = _pegar_cliente(clientes)
    if not cliente: return pausar()
    conta = _recuperar_conta(cliente)
    if not conta: return pausar()

    mini_card_conta(conta)
    print()
    linha()

    transacoes = conta.historico.transacoes
    if not transacoes:
        print(f"  {Cor.DIM}Nenhuma movimentacao registrada.{Cor.RESET}")
    else:
        depositos = sum(t["valor"] for t in transacoes if t["tipo"] == "Deposito")
        saques_t  = sum(t["valor"] for t in transacoes if t["tipo"] == "Saque")

        for t in transacoes:
            eh_dep = t["tipo"] == "Deposito"
            icone  = f"{Cor.VERDE}+{Cor.RESET}" if eh_dep else f"{Cor.VERMELHO}-{Cor.RESET}"
            sinal  = f"{Cor.VERDE}+" if eh_dep else f"{Cor.VERMELHO}-"
            print(
                f"  {Cor.DIM}{t['data']}{Cor.RESET}  {icone}  "
                f"{t['tipo']:<10}  "
                f"{sinal}R$ {t['valor']:>10,.2f}{Cor.RESET}"
            )

        linha()
        print(f"  {Cor.DIM}Total depositos :{Cor.RESET} {Cor.VERDE}+R$ {depositos:>9,.2f}{Cor.RESET}")
        print(f"  {Cor.DIM}Total saques    :{Cor.RESET} {Cor.VERMELHO}-R$ {saques_t:>9,.2f}{Cor.RESET}")

    linha()
    pausar()


def criar_cliente(clientes):
    """Handle the New Customer menu option.

    Collects personal data, validates CPF uniqueness, and
    registers a new PessoaFisica in the system.

    Args:
        clientes: List of registered Cliente instances (mutated in place).
    """
    cabecalho()
    titulo_box("NOVO CLIENTE", Cor.MAGENTA)
    print(f"  {Cor.DIM}Preencha os dados do novo cliente.{Cor.RESET}\n")

    cpf = entrada("CPF (somente numeros)").replace(".", "").replace("-", "")
    if _filtrar_cliente(cpf, clientes):
        erro("CPF ja cadastrado.")
        return pausar()

    nome     = entrada("Nome completo")
    data_str = entrada("Data de nascimento (dd/mm/aaaa)")
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        erro("Data invalida. Use o formato dd/mm/aaaa.")
        return pausar()

    logradouro = entrada("Logradouro")
    numero_end = entrada("Numero")
    bairro     = entrada("Bairro")
    cidade_uf  = entrada("Cidade/UF")
    endereco   = f"{logradouro}, {numero_end} - {bairro} - {cidade_uf}"

    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data, endereco=endereco)
    clientes.append(cliente)
    animacao_carregando("Cadastrando cliente")
    ok(f"Cliente '{nome}' cadastrado com sucesso!")
    pausar()


def criar_conta(clientes, contas):
    """Handle the New Account menu option.

    Links a new ContaCorrente to an existing customer.
    Account numbers are assigned sequentially.

    Args:
        clientes: List of registered Cliente instances.
        contas: List of all Conta instances (mutated in place).
    """
    cabecalho()
    titulo_box("NOVA CONTA CORRENTE", Cor.AZUL)
    cliente = _pegar_cliente(clientes)
    if not cliente: return pausar()

    numero = len(contas) + 1  # Simple sequential numbering
    conta  = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    animacao_carregando("Criando conta")
    ok(f"Conta Corrente n. {numero:04d} criada para {cliente.nome}!")
    mini_card_conta(conta)
    pausar()


def listar_contas(contas):
    """Handle the List Accounts menu option.

    Renders a visual card and detail block for every registered account.

    Args:
        contas: List of all Conta instances.
    """
    cabecalho()
    titulo_box("CONTAS CADASTRADAS", Cor.CIANO)
    if not contas:
        aviso("Nenhuma conta cadastrada ainda.")
        return pausar()
    for conta in contas:
        mini_card_conta(conta)
        for l in str(conta).split("\n"):
            print(f"  {Cor.DIM}{l}{Cor.RESET}")
        print()
    pausar()


def listar_clientes(clientes):
    """Handle the List Customers menu option.

    Displays the string representation of every registered customer.

    Args:
        clientes: List of registered Cliente instances.
    """
    cabecalho()
    titulo_box("CLIENTES CADASTRADOS", Cor.MAGENTA)
    if not clientes:
        aviso("Nenhum cliente cadastrado ainda.")
        return pausar()
    for c in clientes:
        linha(".")
        for l in str(c).split("\n"):
            print(f"  {l}")
    linha(".")
    pausar()


# ══════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════

# Each tuple: (command string, display label, ANSI color)
OPCOES = [
    ("d",  "Depositar",       Cor.VERDE),
    ("s",  "Sacar",           Cor.AMARELO),
    ("e",  "Extrato",         Cor.CIANO),
    ("nc", "Nova Conta",      Cor.AZUL),
    ("lc", "Listar Contas",   Cor.AZUL),
    ("nu", "Novo Cliente",    Cor.MAGENTA),
    ("lu", "Listar Clientes", Cor.MAGENTA),
    ("q",  "Sair",            Cor.VERMELHO),
]


def exibir_menu():
    """Render the main navigation menu with color-coded options."""
    cabecalho()
    print(f"  {Cor.DIM}Selecione uma opcao:{Cor.RESET}\n")
    for cmd, nome, cor in OPCOES:
        sep = "  " if len(cmd) == 1 else " "
        print(f"    {cor}{Cor.BOLD}[{cmd}]{sep}{Cor.RESET}{nome}")
    print()


def main():
    """Application entry point.

    Initialises the in-memory data stores and runs the main event loop,
    dispatching each user command to the appropriate handler function.
    """
    clientes = []  # In-memory list of all registered customers
    contas   = []  # In-memory list of all registered accounts

    while True:
        exibir_menu()
        opcao = entrada("Opcao").lower()

        match opcao:
            case "d":  depositar(clientes)
            case "s":  sacar(clientes)
            case "e":  exibir_extrato(clientes)
            case "nc": criar_conta(clientes, contas)
            case "lc": listar_contas(contas)
            case "nu": criar_cliente(clientes)
            case "lu": listar_clientes(clientes)
            case "q":
                cabecalho()
                print(f"\n  {Cor.VERDE}{Cor.BOLD}Obrigado por usar o Banco DIO. Ate logo!{Cor.RESET}\n")
                break
            case _:
                aviso("Opcao invalida. Tente novamente.")
                time.sleep(1)


if __name__ == "__main__":
    main()