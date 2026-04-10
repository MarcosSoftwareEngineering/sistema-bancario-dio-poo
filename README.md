# Bank System OOP - DIO Challenge

A Python-based banking system simulating basic operations via a Command Line Interface (CLI). This project is a refactoring of a procedural banking script into a robust Object-Oriented Programming (OOP) architecture, following a provided UML class diagram. 

This project is part of the Python Developer track by [DIO (Digital Innovation One)](https://www.dio.me/).

## 🚀 Features

The system allows users to perform the following operations through an interactive menu:

* **[1] New User:** Register a new client (Individual/Pessoa Física) with Name, CPF, Date of Birth, and Address.
* **[2] New Account:** Create a new Checking Account (Conta Corrente) linked to an existing user.
* **[3] List Accounts:** Display all registered accounts and their respective owners.
* **[4] Deposit:** Add funds to a specific account. The transaction is recorded in the account's history.
* **[5] Withdraw:** Withdraw funds from an account, respecting business rules (balance availability, withdrawal limits, and maximum daily transactions).
* **[6] Statement:** Display a detailed history of all transactions (deposits and withdrawals) and the current balance.

## 🧠 Software Architecture & OOP Concepts

This project was built focusing on best practices and solid OOP principles:

* **Encapsulation:** Sensitive data like account balance (`_saldo`) and transaction history (`_historico`) are protected and accessed only via secure properties and methods.
* **Inheritance:** Base classes like `Conta` (Account) and `Cliente` (Client) provide common attributes and behaviors for specific implementations like `ContaCorrente` and `PessoaFisica`.
* **Polymorphism:** The `Transacao` (Transaction) interface allows different types of transactions (`Saque` and `Deposito`) to execute their specific logic using a common `registrar()` method.
* **Composition:** The `Historico` class is composed within the `Conta` class, meaning an account inherently owns its transaction history.
* **Abstract Classes (ABC):** Used to define strict contracts for Accounts and Transactions, ensuring derived classes implement mandatory behaviors.

## 🛠️ Technologies Used

* **Python 3**
* **Datetime Module:** For timestamping transactions and handling birth dates.
* **Typing Module:** For better code readability and static type hinting.

## 💻 How to Run

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/MarcosEngenhariaDeSoftware/sistema-bancario-dio-poo.git](https://github.com/MarcosEngenhariaDeSoftware/sistema-bancario-dio-poo.git)

   cd sistema-bancario-dio-poo

   python main.py
