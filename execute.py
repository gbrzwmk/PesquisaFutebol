from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os

# --- Importando a LÓGICA (nomes 'quiz' e 'criar_cadastro' corretos) ---
try:
    from quiz import gerar_pergunta_aleatoria, TIMES_BRASILEIRAO_2025
    from criar_cadastro import (
        validar_nome, validar_cpf, validar_cep, validar_email, 
        validar_telefone, validar_idade, validar_uf
    )
except ImportError:
    print("ERRO: Verifique se os arquivos 'quiz.py' e 'criar_cadastro.py' estão na mesma pasta que 'execute.py'")
    exit()

app = Flask(__name__)
app.secret_key = 'agora_o_projeto_anda' 

# Dicionário de Votos (fica aqui)
votos = {
    "Corinthians": 0,
    "Palmeiras": 0,
    "São Paulo": 0,
    "Santos": 0
}

# --- ROTA 1: CADASTRO - ETAPA 1 (DADOS PESSOAIS) ---
@app.route('/', methods=['GET', 'POST'])
def cadastro_etapa_1():
    # Se já passou do cadastro, pular
    if session.get('status') == 'cadastrado':
        return redirect(url_for('pagina_quiz'))
    if session.get('status') == 'quiz_completo':
        return redirect(url_for('pagina_votacao'))

    # Inicializa os dados do formulário na sessão
    if 'form_data' not in session:
        session['form_data'] = {}

    erros = []
    if request.method == 'POST':
        nome = request.form.get('nome')
        ano_nascimento = request.form.get('ano_nascimento')
        
        # Validações da Etapa 1
        erro_nome = validar_nome(nome)
        if erro_nome: erros.append(erro_nome)
        
        erro_idade = validar_idade(ano_nascimento)
        if erro_idade: erros.append(erro_idade)

        if not erros:
            # Salva dados na sessão e avança
            session['form_data']['nome'] = nome
            session['form_data']['ano_nascimento'] = ano_nascimento
            session.modified = True # Força o salvamento da sessão
            return redirect(url_for('cadastro_etapa_2'))
        
    return render_template('cadastro_1.html', erros=erros, form_data=session.get('form_data'))


# --- ROTA 2: CADASTRO - ETAPA 2 (DOCUMENTOS) ---
@app.route('/cadastro_etapa_2', methods=['GET', 'POST'])
def cadastro_etapa_2():
    # Proteção: Se não passou pela etapa 1, volta pro começo
    if 'nome' not in session.get('form_data', {}):
        return redirect(url_for('cadastro_etapa_1'))

    erros = []
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        
        # Validações da Etapa 2
        erro_cpf = validar_cpf(cpf)
        if erro_cpf: erros.append(erro_cpf)
        
        erro_email = validar_email(email)
        if erro_email: erros.append(erro_email)

        if not erros:
            # Salva dados na sessão e avança
            session['form_data']['cpf'] = cpf
            session['form_data']['email'] = email
            session.modified = True
            return redirect(url_for('cadastro_etapa_3'))

    return render_template('cadastro_2.html', erros=erros, form_data=session.get('form_data'))


# --- ROTA 3: CADASTRO - ETAPA 3 (CONTATO) ---
@app.route('/cadastro_etapa_3', methods=['GET', 'POST'])
def cadastro_etapa_3():
    # Proteção: Se não passou pela etapa 2, volta
    if 'cpf' not in session.get('form_data', {}):
        return redirect(url_for('cadastro_etapa_2'))

    erros = []
    if request.method == 'POST':
        telefone = request.form.get('telefone')
        cep = request.form.get('cep')
        estado = request.form.get('estado')
        
        # Validações da Etapa 3
        erro_telefone = validar_telefone(telefone)
        if erro_telefone: erros.append(erro_telefone)
        
        erro_cep = validar_cep(cep)
        if erro_cep: erros.append(erro_cep)
        
        erro_estado = validar_uf(estado)
        if erro_estado: erros.append(erro_estado)

        if not erros:
            # CADASTRO COMPLETO!
            session['status'] = 'cadastrado'
            # Salva o nome do usuário para usar depois
            session['nome_usuario'] = session['form_data']['nome']
            
            # Limpa os dados temporários do formulário
            session.pop('form_data', None)
            
            # Redireciona para o Quiz!
            return redirect(url_for('pagina_quiz'))

    return render_template('cadastro_3.html', erros=erros, form_data=session.get('form_data'))


# --- ROTA DO QUIZ ---
@app.route('/quiz')
def pagina_quiz():
    if session.get('status') != 'cadastrado' and session.get('status') != 'quiz_completo':
        return redirect(url_for('cadastro_etapa_1'))
    if session.get('status') == 'quiz_completo':
        return redirect(url_for('pagina_votacao'))

    if 'pontos' not in session:
        session['pontos'] = 0
        session['pergunta_atual'] = 1
    
    pergunta, opcoes, resposta_certa = gerar_pergunta_aleatoria(TIMES_BRASILEIRAO_2025)
    session['resposta_certa'] = resposta_certa
    
    return render_template('quiz.html', 
                           pergunta=pergunta, 
                           opcoes=opcoes, 
                           pontos=session['pontos'], 
                           num_pergunta=session['pergunta_atual'])

@app.route('/responder_quiz', methods=['POST'])
def responder_quiz():
    if session.get('status') != 'cadastrado':
        return redirect(url_for('cadastro_etapa_1'))

    resposta_usuario = request.form.get('opcao')
    resposta_certa = session.get('resposta_certa', '')
    
    mensagem = ""
    foi_correto = False
    if resposta_usuario == resposta_certa:
        session['pontos'] += 1
        mensagem = "RESPOSTA CORRETA!"
        foi_correto = True
    else:
        mensagem = f"QUE PENA! A resposta correta era: '{resposta_certa}'"

    session['pergunta_atual'] += 1
    total_perguntas_quiz = 5 

    if session['pergunta_atual'] <= total_perguntas_quiz:
        return render_template('quiz.html', 
                               mensagem_anterior=mensagem,
                               foi_correto=foi_correto,
                               pontos=session['pontos'],
                               num_pergunta=session['pergunta_atual'],
                               redirect_url=url_for('pagina_quiz') 
                              )
    else:
        session['status'] = 'quiz_completo'
        pontos_finais = session.get('pontos', 0)
        session.pop('pontos', None)
        session.pop('pergunta_atual', None)
        session.pop('resposta_certa', None)
        
        return render_template('resultado_quiz.html', 
                               pontos=pontos_finais,
                               total=total_perguntas_quiz)

# --- ROTA DA VOTAÇÃO ---
@app.route('/votacao')
def pagina_votacao():
    if session.get('status') != 'quiz_completo':
        if session.get('status') == 'cadastrado':
            return redirect(url_for('pagina_quiz'))
        return redirect(url_for('cadastro_etapa_1'))

    # MUDANÇA 1: Passa o status de "já votou" para o HTML
    return render_template('index.html', votos=votos, has_voted=session.get('has_voted', False))


@app.route('/votar', methods=['POST'])
def votar():
    if session.get('status') != 'quiz_completo':
        return jsonify({'error': 'Nao autorizado'}), 403
    
    # MUDANÇA 2: Checa se o usuário já votou
    if session.get('has_voted', False):
        return jsonify({'error': 'Você só pode votar uma vez por cadastro!'})

    time = request.form['time']
    if time in votos:
        votos[time] += 1
    
    # MUDANÇA 3: Marca o usuário como "já votou"
    session['has_voted'] = True
    
    return jsonify(votos)

# --- ROTA DE LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('cadastro_etapa_1'))

# --- ANTI-CACHE ---
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    if not os.path.exists('templates'):
        print("ERRO: Pasta 'templates' não encontrada.")
    if not os.path.exists('static'):
        print("ERRO: Pasta 'static' não encontrada. Crie-a e coloque o 'fundo.jpg' nela.")
    else:
        print("="*50)
        print("Servidor Flask rodando!")
        print("Acesse o site em: http://127.0.0.1:5000/")
        print("="*50)
        app.run(debug=True)