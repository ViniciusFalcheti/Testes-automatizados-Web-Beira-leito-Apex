# 🧪 Automação de Testes - Beira-leito Apex

Este projeto tem como objetivo automatizar os testes do sistema de gerenciamento de aplicações do **Beira-leito Apex**, garantindo maior confiabilidade e agilidade nas validações funcionais.

## 🚀 Tecnologias Utilizadas

- **Python** – Linguagem principal para desenvolvimento dos testes
- **Selenium WebDriver** – Automação de interações com a interface do usuário
- **pytest** – Framework para execução e organização dos testes
- **python-dotenv** – Gerenciamento seguro de variáveis de ambiente (credenciais e configurações)

## 📁 Estrutura do Projeto

```
.
├── tests/              # Casos de teste organizados por módulo
├── pages/              # Page Objects com os elementos e ações das telas
├── utils/              # Funções auxiliares (ex: conexão com banco, geração de dados)
├── .env                # Variáveis de ambiente (NÃO versionar)
├── .gitignore          # Arquivos e pastas ignoradas pelo Git
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
```

## ⚙️ Configuração do Ambiente

1. **Clone o repositório:**
```bash
git clone https://github.com/ViniciusFalcheti/Testes-automatizados-Web-Beira-leito-Apex.git
cd Testes-automatizados-Web-Beira-leito-Apex
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o arquivo `.env`:**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```dotenv
APEX_USER=seu_usuario_apex
APEX_PASSWORD=sua_senha_apex

DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=oradsv.hcrp.usp.br
DB_SERVICE=HCDESV
ORACLE_CLIENT_DIR=C:\oracle\instantclient_23_7
```

> ⚠️ O arquivo `.env` deve ser mantido fora do controle de versão por segurança.

## 🧪 Executando os Testes

Execute todos os testes com:

```bash
pytest
```

Ou execute um teste específico:

```bash
pytest tests/test_login.py
```

Adicione o parâmetro `-s` para ver prints e logs no terminal:

```bash
pytest -s
```

## 📝 Boas Práticas Utilizadas

- **Page Object Model (POM):** separação da lógica de teste e da lógica de interface.
- **Variáveis de ambiente:** mantêm credenciais e configurações fora do código-fonte.
- **Modularização:** testes organizados por funcionalidades.
- **Reutilização de código:** via funções auxiliares em `utils`.

## 📄 Licença

Este projeto é privado e de uso interno. Todos os direitos reservados.
