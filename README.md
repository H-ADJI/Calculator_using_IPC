# Technical assignment sekoia

Made by HADJI KHALIL (aka H-ADJI)

## Objectif

Parallelised mathematical calculation using a home made Interpreter running on multiple python processes.

## High level architecture

![architecture image](/assets/IPC_calculator.png "architecture")

## Project Setup

### Requirements

- Python version 3.x the version used for dev environment is 3.10.6
- add your python alias to the Makefile for ease of use 

```sh
py=python
```

or

```sh
py=python3
```

### Dependencies

- Make sure you're inside the project folder
- Create a virtual env to isolate dependencies from conflicting with other project using :

```sh
python -m venv venv
```

- Install dependencies using :

```sh
pip install -r requirements.txt
```

### Running the project

- **Run the server** :

```sh
make server
```

- **Run the client** :

```sh
make client
```

- **Run tests** :

```sh
make testing
```
## Implementation details

### Calculation interpreter
The component holding the logic for reading the arithmetic operations and computing the result. It is a basic implementation of an interpreter that uses the following pipeline :
![Pipeline image](/assets/InterpreterPipeline.png "architecture")

- The arithmetic operations string is feed to the parser that tokenize the text into the defined symboles of the language (math operations in our case)
- The symboles are feed to a parser that generate an AST using the following logic :
  - operations with higher priority goes the base of the tree
  - operations with lower priority goes the root of the tree
![Pipeline image](/assets/AST_example2.png "architecture")

## Project Guidelines

- Develop a client which is able to send the information given at operations.7z:
  - send the information using sockets to the service,
  - receive information through the sockets and store the results in a file,

- Develop a service in Python which is built with the following features:
  - receive information using sockets,
  - It is built by 2 different processes (at least). Consider having more processes to speed calculations,
  - Processes must be able to exchange information using pipes. Please DO NOT use Threading or Pool,
  - Parent process must create and destroy child process for the arithmetic operations given at operations.7z,
  - Once the arithmetic operation is finished on the second process, such process should be destroyed by the parent process,
  - Consider that operations should not be calculated using eval(),
  - Consider using logging instead of console prints.
