import random
import os

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


def gerar_pergunta_aleatoria(times_dict):
    """
    Gera aleatoriamente uma de duas estruturas de pergunta sobre os times e suas divisões.
    Retorna uma tupla: (texto_da_pergunta, lista_de_opcoes, texto_da_resposta_correta)
    """
    tipo_pergunta = random.choice(['qual_serie', 'qual_time'])
    todas_as_series = list(times_dict.keys())

    if tipo_pergunta == 'qual_serie':
        # Pergunta: "Em qual série o time X joga?"
        serie_correta_key = random.choice(todas_as_series)
        time_correto = random.choice(times_dict[serie_correta_key])

        pergunta = f"Em qual série o time '{time_correto}' está em 2025?"
        resposta_correta = f"Série {serie_correta_key}"

        # Gera opções incorretas
        opcoes_incorretas = []
        series_erradas = [s for s in todas_as_series if s != serie_correta_key]
        random.shuffle(series_erradas)
        for serie in series_erradas[:3]:
            opcoes_incorretas.append(f"Série {serie}")

        opcoes = opcoes_incorretas + [resposta_correta]
        random.shuffle(opcoes)
        return pergunta, opcoes, resposta_correta

    else:  # tipo_pergunta == 'qual_time'
        # Pergunta: "Qual destes times joga na série X?"
        serie_correta_key = random.choice(todas_as_series)
        time_correto = random.choice(times_dict[serie_correta_key])

        pergunta = f"Qual destes times disputa a Série '{serie_correta_key}' em 2025?"
        resposta_correta = time_correto

        # Gera opções incorretas (times de outras séries)
        opcoes_incorretas = []
        series_erradas = [s for s in todas_as_series if s != serie_correta_key]
        while len(opcoes_incorretas) < 3:
            serie_aleatoria = random.choice(series_erradas)
            time_errado = random.choice(times_dict[serie_aleatoria])
            if time_errado not in opcoes_incorretas:
                opcoes_incorretas.append(time_errado)

        opcoes = opcoes_incorretas + [resposta_correta]
        random.shuffle(opcoes)
        return pergunta, opcoes, resposta_correta


def iniciar_quiz(numero_de_perguntas=5):
    """
    Executa o loop principal do Quiz, gerenciando as perguntas, respostas e pontuação.
    ESTA FUNÇÃO NÃO SERÁ USADA DIRETAMENTE PELO FLASK (usa input/print)
    """
    pass


# --- Bloco de Execução ---
if __name__ == "__main__":
    # Este bloco não será mais executado, pois o app.py é o ponto de entrada
    print("Este arquivo contém apenas funções de lógica e não deve ser executado diretamente.")
    print("Execute 'python app.py' para iniciar o sistema web.")