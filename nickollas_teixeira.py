# =====================================================================
# DADOS IMUTÁVEIS (TUPLAS)
# =====================================================================

# MATRIZ_TAXAS: Multiplicadores de mercado para os 12 meses.
# Ex: 1.20 = ganho de 20%, 0.95 = queda de 5%, 1.00 = estabilidade.
MATRIZ_TAXAS = (
    {"NVIDIA": 1.00, "AAPL": 1.00, "MSFT": 1.00, "PETR4": 1.00, "VALE3": 1.00}, # Mês 1 
    {"NVIDIA": 1.20, "AAPL": 1.05, "MSFT": 1.01, "PETR4": 0.98, "VALE3": 0.95}, # Mês 2
    {"NVIDIA": 1.05, "AAPL": 1.15, "MSFT": 0.99, "PETR4": 1.02, "VALE3": 0.90}, # Mês 3
    {"NVIDIA": 1.10, "AAPL": 1.02, "MSFT": 1.05, "PETR4": 0.95, "VALE3": 0.98}, # Mês 4
    {"NVIDIA": 1.02, "AAPL": 0.95, "MSFT": 0.98, "PETR4": 1.12, "VALE3": 1.01}, # Mês 5
    {"NVIDIA": 1.15, "AAPL": 1.10, "MSFT": 1.02, "PETR4": 0.95, "VALE3": 0.92}, # Mês 6
    {"NVIDIA": 1.00, "AAPL": 1.00, "MSFT": 1.00, "PETR4": 1.05, "VALE3": 1.06}, # Mês 7 (Crash rodará isolado)
    {"NVIDIA": 0.98, "AAPL": 1.02, "MSFT": 0.95, "PETR4": 1.08, "VALE3": 1.12}, # Mês 8
    {"NVIDIA": 1.01, "AAPL": 0.99, "MSFT": 1.03, "PETR4": 1.02, "VALE3": 1.20}, # Mês 9
    {"NVIDIA": 1.03, "AAPL": 1.01, "MSFT": 0.97, "PETR4": 1.15, "VALE3": 1.02}, # Mês 10
    {"NVIDIA": 0.99, "AAPL": 1.05, "MSFT": 1.02, "PETR4": 0.98, "VALE3": 1.05}, # Mês 11
    {"NVIDIA": 1.02, "AAPL": 1.00, "MSFT": 1.04, "PETR4": 1.02, "VALE3": 1.01}  # Mês 12
)

# NOTICIAS_MERCADO: Manchetes de cada mês para o dashboard.
NOTICIAS_MERCADO = (
    "Mês 1: Abertura do mercado. Analistas indicam forte otimismo com IA e cautela com commodities.",
    "Mês 2: BOOM DA IA! Alta histórica na busca por chips impulsiona forte crescimento do setor.",
    "Mês 3: FRENESI TECNOLÓGICO: Rumores apontam que nova linha de celulares terá IA super avançada.",
    "Mês 4: PORTO SEGURO: Mercado estica e investidores correm para big techs consolidadas.",
    "Mês 5: TENSÕES GLOBAIS: Problemas em refinarias no exterior indicam que o petróleo pode disparar.",
    "Mês 6: EUFORIA: Setor de tecnologia bate recorde histórico. Especialistas alertam para correções.",
    "Mês 7: URGENTE: Bug global de cibersegurança paralisa servidores no mundo todo. Pânico em Wall Street!",
    "Mês 8: RECUPERAÇÃO: Após susto tecnológico, investidores migram capital para commodities.",
    "Mês 9: SUPER SAFRA: Empresa de mineração anuncia descoberta de nova jazida massiva.",
    "Mês 10: DIVIDENDOS: Rumores de pagamentos bilionários de estatais inflam o setor de energia.",
    "Mês 11: BLACK FRIDAY: Fortes expectativas impulsionam o setor de smartphones.",
    "Mês 12: FECHAMENTO: O mercado entra em estabilidade para o fechamento de balanços do ano."
)

# =====================================================================
# FUNÇÕES DE REGRAS E MOTOR DE TEMPO
# =====================================================================

def obter_precos_mes(mes):
    """
    Função auxiliar: Retorna o dicionário de taxas correspondente ao mês.
    Lembrando que índices de tupla começam em 0, então mês 1 = índice 0.
    """
    # Ex: return MATRIZ_TAXAS[mes - 1]
    pass


def registrar_historico(historico, escolha, estado):
    # Lógica para registrar a escolha do usuário e o estado atual no histórico
    pass


def verificar_vitoria_derrota(estado):
    """
    O Juiz do jogo.
    Se o mês for maior que 12, avalia o patrimônio (>= 25000 é Vitória).
    Retorna True para quebrar o loop do main.py se o jogo acabou, ou False para continuar.
    """
    # Ex: if estado["mes_atual"] > 12: fazer os prints de fim de jogo e retornar True
    pass


def aplicar_evento_mercado(estado):
    """
    Gatilho de evento isolado.
    Se o estado["mes_atual"] for igual a 7, multiplica o valor atual 
    das ações de tecnologia (NVIDIA, AAPL, MSFT) por 0.85 (queda de 15%).
    """
    # Ex: if estado["mes_atual"] == 7: aplica conta e alerta o usuário
    pass


def simular_virada_de_mes(estado):
    """
    Avança o relógio do jogo.
    1. Soma R$ 1.000 de salário no saldo_disponivel.
    2. Pega as taxas do próximo mês e multiplica pelos precos_mercado atuais.
    3. Soma +1 no mes_atual.
    """
    # Lógica para simular a virada de mês, atualizando os preços com base na MATRIZ_TAXAS
    pass


def obter_noticia_mes(mes) -> str:
    """
    Resgata a notícia da tupla baseada no mês atual do estado para enviar ao painel visual.
    """
    return NOTICIAS_MERCADO[mes - 1]