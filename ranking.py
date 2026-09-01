# ranking.py
# Ranking compartilhado: o jogo fala com a API hospedada no Square Cloud.
# Qualquer PC que rodar o jogo salva/lê do mesmo lugar, pela internet.

import requests

# Troque pelo domínio gerado pelo Square Cloud após o deploy.
API_URL = "https://bdsigmahub.squareweb.app/"

TIMEOUT_SEGUNDOS = 8


def salvar_pontuacao(nome, pontuacao):
    """Salva a pontuação do jogador. Se o nome já existir, só atualiza
    quando a nova pontuação for maior que a registrada.
    Retorna uma tupla (atualizou: bool, pontuacao_final: int).
    Levanta ValueError para dados inválidos, ou requests.RequestException
    se a conexão com o servidor falhar."""
    nome = (nome or "").strip()
    if not nome:
        raise ValueError("Nome não pode ser vazio.")
    try:
        pontuacao = int(pontuacao)
    except (TypeError, ValueError):
        raise ValueError("Pontuação inválida.")

    resposta = requests.post(
        f"{API_URL}/salvar",
        json={"nome": nome, "pontuacao": pontuacao},
        timeout=TIMEOUT_SEGUNDOS,
    )

    if resposta.status_code == 400:
        raise ValueError(resposta.json().get("erro", "Dados inválidos."))
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["atualizou"], dados["pontuacao"]


def obter_ranking(limite=10):
    """Retorna lista de tuplas (nome, pontuacao) ordenada da maior pra menor."""
    resposta = requests.get(
        f"{API_URL}/ranking",
        params={"limite": limite},
        timeout=TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    dados = resposta.json()
    return [(item["nome"], item["pontuacao"]) for item in dados]


def obter_pontuacao(nome):
    """Retorna a pontuação atual do jogador, ou None se ele não existir."""
    nome = (nome or "").strip()
    resposta = requests.get(f"{API_URL}/pontuacao/{nome}", timeout=TIMEOUT_SEGUNDOS)
    resposta.raise_for_status()
    return resposta.json().get("pontuacao")


def limpar_ranking():
    """Não implementado no servidor por segurança (evita apagar por engano
    o ranking de todo mundo). Se precisar, apague o ranking.db direto no
    Square Cloud ou crie um endpoint de admin protegido por senha."""
    raise NotImplementedError(
        "Limpeza do ranking não está exposta pela API por segurança."
    )