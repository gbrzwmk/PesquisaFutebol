# 🚀 Projeto: Cadastro, Quiz e Votação (Flask)

Este é um projeto web desenvolvido em Python com o micro-framework Flask. Ele guia um usuário através de um fluxo de três etapas: um cadastro completo, um quiz temático sobre futebol e, por fim, um sistema de votação.

O projeto demonstra o gerenciamento de estado e de sessão de usuário (`session`) para garantir que o usuário só possa acessar o quiz após se cadastrar, e só possa votar após completar o quiz.

## ✨ Funcionalidades Principais

* **Formulário de Cadastro em Múltiplas Etapas:** Um fluxo de cadastro dividido em 3 páginas (Dados Pessoais, Documentos, Contato) para melhorar a experiência do usuário.
* **Validação de Dados no Backend:** Todas as entradas do usuário (Nome, CPF, E-mail, CEP, Idade, etc.) são validadas no servidor usando lógica modular.
* **Gerenciamento de Sessão:** O Flask `session` é usado para:
    * Rastrear o progresso do usuário (`status`: 'cadastrado', 'quiz_completo').
    * Impedir acesso direto a páginas (ex: não pode acessar `/quiz` sem se cadastrar).
    * Impedir que o usuário vote mais de uma vez por sessão.
* **Quiz Dinâmico:** Um quiz de 5 perguntas geradas aleatoriamente sobre as séries (A, B, C, D) do Brasileirão 2025.
* **Sistema de Votação Simples:** Um painel de votação em tempo real (atualizado com JavaScript/AJAX) onde o usuário pode votar no seu time favorito (entre 4 opções).
* **Estrutura de Código Modular:** A lógica de negócio (validações, geração de quiz) está separada do servidor web:
    * `execute.py`: Servidor Flask e rotas.
    * `criar_cadastro.py`: Funções de lógica e validação.
    * `quiz.py`: Funções de lógica do quiz.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3
* **Framework:** Flask
* **Frontend:** HTML / CSS / JavaScript (implícitos nos arquivos de `templates` e `static`)

## 📁 Estrutura do Projeto

```

/seu-projeto/
|
|--- execute.py           \# Arquivo principal do servidor Flask
|--- criar\_cadastro.py    \# Módulo com lógica de validação de cadastro
|--- quiz.py              \# Módulo com lógica de geração do quiz
|
|--- /templates/          \# (Necessário) Pasta para os arquivos HTML
|     |--- cadastro\_1.html
|     |--- cadastro\_2.html
|     |--- cadastro\_3.html
|     |--- quiz.html
|     |--- resultado\_quiz.html
|     |--- index.html       (Página de votação)
|
|--- /static/             \# (Necessível) Pasta para CSS, JS e imagens
|--- fundo.jpg      (Exemplo, conforme mencionado no código)

````

## ⚙️ Instalação e Execução

1.  **Clone este repositório** (ou baixe os arquivos para uma pasta).

2.  **Crie e ative um ambiente virtual** (Recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: .\venv\Scripts\activate
    ```

3.  **Instale o Flask** (única dependência externa):
    ```bash
    pip install Flask
    ```

4.  **Crie as pastas `templates` e `static`** na raiz do projeto, caso não existam.

5.  **Coloque os arquivos HTML** (`cadastro_1.html`, `cadastro_2.html`, `cadastro_3.html`, `quiz.html`, `resultado_quiz.html`, `index.html`) dentro da pasta `templates`.

6.  **Coloque seus arquivos estáticos** (CSS, imagens como `fundo.jpg`) dentro da pasta `static`.

7.  **Execute o servidor:**
    ```bash
    python execute.py
    ```

8.  **Acesse o projeto** no seu navegador no endereço: `http://127.0.0.1:5000/`

## 🌊 Fluxo do Usuário

1.  O usuário acessa a raiz (`/`) e é apresentado à **Etapa 1 do Cadastro**.
2.  Ao preencher e enviar, ele avança para a **Etapa 2** e **Etapa 3**.
3.  Após o cadastro ser validado e concluído, a `session['status']` muda para `'cadastrado'` e ele é redirecionado para a página `/quiz`.
4.  O usuário responde às 5 perguntas do quiz.
5.  Ao finalizar o quiz, a `session['status']` muda para `'quiz_completo'` e ele vê sua pontuação final, com um link para a página de votação (`/votacao`).
6.  O usuário pode votar **apenas uma vez** (controlado pela `session['has_voted']`).
7.  A qualquer momento, o usuário pode usar a rota `/logout` para limpar sua sessão e reiniciar o fluxo.

## ⚠️ Limitações Conhecidas

* **Votação em Memória:** Os votos são armazenados em um dicionário global no `execute.py`. Isso significa que **todos os votos serão perdidos se o servidor Flask for reiniciado**. Para persistência, seria necessário um banco de dados (como SQLite ou PostgreSQL).
* **Sessão de Curta Duração:** O `status` do usuário é baseado na sessão do Flask, que é armazenada em cookies no navegador. Limpar os cookies ou fechar o navegador (dependendo da configuração) fará o usuário perder seu progresso.
````
