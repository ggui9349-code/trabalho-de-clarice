# Mini App de Tarefas

Aplicação web desenvolvida com **Python, Flask e SQLite** para gerenciamento de tarefas.

## Funcionalidades

- Cadastrar uma tarefa;
- Visualizar todas as tarefas;
- Alterar o status entre **Pendente** e **Concluída**;
- Excluir uma tarefa;
- Editar tarefas;
- Filtrar tarefas por status;
- Exibir mensagens de feedback após as ações.

## Tecnologias utilizadas

- Python 3
- Flask
- SQLite
- HTML5
- CSS3

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd mini-app-tarefas
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

Depois, acesse no navegador:

```text
http://127.0.0.1:5000
```

O banco de dados `tarefas.db` é criado automaticamente na primeira execução.

## Estrutura do projeto

```text
mini-app-tarefas/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── editar.html
    └── index.html
```

## Autor

Projeto desenvolvido para o desafio de Mini App de Tarefas utilizando Flask e SQLite.
