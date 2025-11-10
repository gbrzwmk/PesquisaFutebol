import re
from datetime import datetime

# --- DADOS DOS TIMES (ATUALIZADO PARA 2025) ---
TIMES_BRASILEIRAO_2025 = {
    'A': [
        "Atlético-MG", "Bahia", "Botafogo", "Ceará", "Corinthians",
        "Cruzeiro", "Flamengo", "Fluminense", "Fortaleza", "Grêmio",
        "Internacional", "Juventude", "Mirassol", "Palmeiras", "Red Bull Bragantino",
        "Santos", "São Paulo", "Sport", "Vasco da Gama", "Vitória"
    ],
    'B': [
        "Amazonas", "América-MG", "Athletic-MG", "Athletico-PR", "Atlético-GO",
        "Avaí", "Botafogo-SP", "Chapecoense", "Coritiba", "CRB",
        "Criciúma", "Cuiabá", "Ferroviária", "Goiás", "Novorizontino",
        "Operário-PR", "Paysandu", "Remo", "Vila Nova", "Volta Redonda"
    ],
    'C': [
        "ABC", "Aparecidense", "Botafogo-PB", "Caxias", "CSA",
        "Confiança", "Ferroviário", "Floresta", "Jacuipense", "Joinville",
        "Londrina", "Luverdense", "Náutico", "Retrô", "Sampaio Corrêa",
        "São Bernardo", "São José-RS", "Ypiranga-RS", "Tombense", "Figueirense"
    ],
    'D': [
        "Água Santa", "América-RN", "Anápolis", "ASA", "Azuriz", "Brasil de Pelotas",
        "Brasiliense", "Cianorte", "Costa Rica-MS", "Democrata-GV",
        "Hercílio Luz", "Inter de Limeira", "Ipatinga", "Itabuna", "Manaus",
        "Maranhão", "Moto Club", "Nova Iguaçu", "Pouso Alegre", "Portuguesa-RJ",
        "River-PI", "Santa Cruz", "Santo André", "Sergipe", "Sousa", "Treze"
    ]
}


# --- FUNÇÕES DE VALIDAÇÃO ---
def validar_nome(nome):
    """Valida se o nome completo é válido."""
    if not nome:
        return "O nome não pode ser vazio."
    if not re.match(r'^[a-zA-Zà-úÀ-Ú\s]+$', nome):
        return "O nome contém caracteres inválidos. Use apenas letras e espaços."
    if len(nome.split()) < 2:
        return "Digite o nome completo (nome e sobrenome)."
    return None


def validar_cpf(cpf):
    """Valida se o CPF tem 11 dígitos numéricos."""
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return 'CPF inválido! Digite um CPF com 11 dígitos numéricos.'
    return None


def validar_cep(cep):
    """Valida se o CEP tem 8 dígitos numéricos."""
    cep = re.sub(r'\D', '', cep)
    if len(cep) != 8 or not cep.isdigit():
        return 'CEP inválido! Digite um CEP com 8 dígitos numéricos.'
    return None


def validar_email(email):
    """Valida o formato do e-mail."""
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return 'Email inválido! O formato deve ser exemplo@dominio.com.'
    return None


def validar_telefone(telefone):
    """Valida se o telefone tem entre 8 e 11 dígitos numéricos."""
    telefone_numerico = re.sub(r'\D', '', telefone)
    if not (8 <= len(telefone_numerico) <= 11):
        return 'Telefone inválido! Digite um número válido com ou sem DDD.'
    return None


def validar_idade(ano_nascimento_str):
    """Valida o ano de nascimento e a idade (maior que 18)."""
    try:
        ano_nascimento = int(ano_nascimento_str)
        ano_atual = datetime.today().year
        idade = ano_atual - ano_nascimento
        if not (1920 < ano_nascimento <= ano_atual):
            return "Ano de nascimento inválido. Por favor, digite um ano realista."
        if idade < 18:
            return f"Cadastro não permitido para menores de 18 anos. Idade calculada: {idade} anos."
        return None
    except (ValueError, TypeError):
        return "Ano de nascimento inválido! Digite um ano com 4 dígitos (ex: 1995)."


def validar_uf(estado):
    """Valida se a sigla do estado (UF) é válida."""
    ufs_validas = {
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
        'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    }
    if estado.upper().strip() not in ufs_validas:
        return f"Estado inválido! Digite a sigla de uma UF válida (ex: SP, RJ...)."
    return None


# --- FUNÇÕES AUXILIARES ---
def solicitar_dado_valido(mensagem_prompt, funcao_validacao, mensagem_sucesso=None):
    """Pede um dado ao usuário em loop até que seja válido."""
    # ESTA FUNÇÃO NÃO SERÁ USADA DIRETAMENTE PELO FLASK,
    # POIS ELA USA input() E print(). A LÓGICA AGORA ESTÁ NO app.py
    while True:
        dado = input(mensagem_prompt).strip()
        erro = funcao_validacao(dado)
        if erro:
            print(f"-> Erro: {erro}")
            # Se a validação impedir o cadastro (menor de idade), retorna None para interromper.
            if "Cadastro não permitido" in erro:
                return None
        else:
            if mensagem_sucesso:
                print(f"   {mensagem_sucesso}")
            return dado


def selecionar_time_futebol():
    """Exibe um menu interativo para o usuário selecionar seu time de futebol."""
    # ESTA FUNÇÃO TAMBÉM NÃO SERÁ USADA DIRETAMENTE PELO FLASK
    # O ideal é transformar isso em um <select> no HTML
    print("\nPara personalizar sua experiência, conte pra gente para qual time você torce!")
    # ... (resto do código com input/print)
    pass


# --- FUNÇÃO DE MENSAGEM FINAL ---
def exibir_mensagem_boas_vindas(estado):
    """Exibe uma mensagem personalizada com tema de futebol para cada estado do Brasil."""
    # Esta função pode ser chamada no app.py após o cadastro
    mensagens_esportivas_por_estado = {
        # Região Sudeste
        'SP': "Aqui em São Paulo, a rivalidade é grande, mas a paixão nos une! Seja qual for sua camisa, jogamos no seu time para marcar o golaço!",
        'RJ': "Da geral do Maraca para a varanda do seu novo apê! No Rio, a gente torce com a alma. Deixe a gente ser a sua torcida organizada!",
        'MG': "Uai, sô! Seja Galo ou Raposa, entramos em campo pra te ajudar a levantar essa taça!",
        'ES': "Capixaba torce com raça e fé! Com a mesma garra, buscamos sempre as melhores jogadas.",
        # Outras regiões... (código omitido para brevidade, mas estaria aqui)
    }
    mensagem_padrao = "Seja qual for seu time, estamos com você para realizar o sonho da casa própria!"
    mensagem_personalizada = mensagens_esportivas_por_estado.get(estado.upper(), mensagem_padrao)

    print("\n-----------------------------------------")
    print(mensagem_personalizada)
    print("-----------------------------------------")


# --- FUNÇÃO PRINCIPAL DE CADASTRO ---
def criar_cadastro():
    """Orquestra a coleta de todos os dados do cliente e retorna um dicionário."""
    # ESTA FUNÇÃO É ONDE ESTAVA A LÓGICA DE TERMINAL
    # O app.py agora substitui esta lógica
    pass


# --- BLOCO DE EXECUÇÃO PRINCIPAL (AJUSTADO) ---
if __name__ == "__main__":
    # Este bloco não será mais executado, pois o app.py é o ponto de entrada
    print("Este arquivo contém apenas funções de lógica e não deve ser executado diretamente.")
    print("Execute 'python app.py' para iniciar o sistema web.")