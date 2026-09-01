# minigame.py
# AURA REFLEX: clique no alvo antes que ele desapareça.
# No final, o jogador digita o nome (uma vez só) e a pontuação é enviada
# para a API de ranking do SIGMA HUB (hospedada no Square Cloud), que
# guarda tudo num banco compartilhado — o ranking é o mesmo em qualquer PC.

import json
import random
import threading
import urllib.error
import urllib.request

import customtkinter as ctk

import fundo
import tema

DURACAO_JOGO_S = 30
TAMANHO_ALVO = 60
TEMPO_MIN_ALVO_MS = 550
TEMPO_MAX_ALVO_MS = 1100

# Troque pela URL do seu app publicado no Square Cloud (sem barra no final).
URL_API = "https://bdsigmahub.squareweb.app/"

TAMANHO_RANKING = 10
NOME_MAX_CHARS = 14

MEDALHAS = {0: "🥇", 1: "🥈", 2: "🥉"}


# ---------------------------------------------------------------------------
# Comunicação com a API de ranking
# ---------------------------------------------------------------------------

def _requisicao(caminho, metodo="GET", corpo=None, tempo_limite=5):
    """Faz uma chamada HTTP simples à API (sem depender de bibliotecas extras)."""
    url = f"{URL_API}{caminho}"
    dados = None
    # Um User-Agent de navegador evita bloqueios 403 de proxies que rejeitam
    # o identificador padrão do urllib ("Python-urllib/3.x") por parecer bot.
    cabecalhos = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SigmaHub/1.0"
        ),
        "Accept": "application/json",
    }

    if corpo is not None:
        dados = json.dumps(corpo).encode("utf-8")
        cabecalhos["Content-Type"] = "application/json"

    pedido = urllib.request.Request(url, data=dados, headers=cabecalhos, method=metodo)
    with urllib.request.urlopen(pedido, timeout=tempo_limite) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def _relatar_erro(acao, erro):
    """Imprime detalhes do erro (inclusive o código HTTP, se houver) para facilitar o diagnóstico."""
    if isinstance(erro, urllib.error.HTTPError):
        try:
            corpo = erro.read().decode("utf-8", errors="replace")
        except Exception:
            corpo = ""
        print(f"{acao}: HTTP {erro.code} {erro.reason} — {corpo[:200]}")
    else:
        print(f"{acao}: {erro}")


def buscar_ranking(limite=TAMANHO_RANKING):
    """Busca o ranking na API. Devolve None se não conseguir conectar."""
    try:
        return _requisicao(f"/ranking?limite={limite}")
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as erro:
        _relatar_erro("Não foi possível buscar o ranking", erro)
        return None


def enviar_pontuacao(nome, pontos):
    """Envia a pontuação para a API. Devolve None se não conseguir conectar."""
    try:
        return _requisicao("/salvar", metodo="POST", corpo={"nome": nome, "pontuacao": pontos})
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as erro:
        _relatar_erro("Não foi possível salvar a pontuação", erro)
        return None


MARGEM_PAINEL = 30
TOPO_PAINEL = 78
LARGURA_MIN_PAINEL = 340
ALTURA_MIN_PAINEL = 360


def construir_jogo(container, ir_home):
    container.configure(fg_color=tema.BG_DEEP)
    canvas = fundo.criar_fundo_interativo(container)

    estado = {
        "pontos": 0,
        "tempo_restante": DURACAO_JOGO_S,
        "job_alvo": None,
        "job_relogio": None,
        "jogando": False,
    }

    botao_voltar = ctk.CTkButton(
        canvas,
        text="←  Hub",
        width=110,
        height=38,
        font=tema.FONTE_HUD,
        fg_color=tema.BG_ELEVATED,
        hover_color=tema.NEON_VIOLET,
        border_width=2,
        border_color=tema.NEON_GOLD,
        corner_radius=0,
        command=lambda: finalizar_e_sair(),
    )
    canvas.create_window(30, 22, anchor="nw", window=botao_voltar)

    painel = ctk.CTkFrame(
        canvas,
        fg_color=tema.BG_GLASS,
        bg_color=tema.BG_GLASS,
        border_width=3,
        border_color=tema.NEON_VIOLET,
        corner_radius=0,
    )
    painel.pack_propagate(False)
    id_painel = canvas.create_window(0, 0, anchor="n", window=painel)

    centro = ctk.CTkFrame(painel, fg_color="transparent")
    centro.pack(expand=True, fill="both", padx=30, pady=16)

    def reposicionar_painel(_evento=None):
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        largura = max(canvas.winfo_width(), 40)
        altura = max(canvas.winfo_height(), 40)
        w = max(largura - MARGEM_PAINEL * 2, LARGURA_MIN_PAINEL)
        h = max(altura - TOPO_PAINEL - MARGEM_PAINEL, ALTURA_MIN_PAINEL)
        painel.configure(width=w, height=h)
        canvas.coords(id_painel, largura / 2, TOPO_PAINEL)
        canvas.tag_raise("ui")

    canvas.bind("<Configure>", reposicionar_painel, add="+")
    canvas.after(30, reposicionar_painel)

    ctk.CTkLabel(
        centro,
        text="A U R A   R E F L E X",
        font=tema.FONTE_TITULO,
        text_color=tema.NEON_GOLD,
    ).pack(pady=(4, 2))

    ctk.CTkLabel(
        centro,
        text="clique no alvo antes que ele suma",
        font=tema.FONTE_MONO,
        text_color=tema.TEXT_MUTED,
    ).pack(pady=(0, 10))

    hud = ctk.CTkFrame(
        centro,
        fg_color=tema.BG_GLASS,
        border_width=2,
        border_color=tema.NEON_PURPLE,
        corner_radius=0,
    )
    hud.pack(fill="x", pady=6)

    label_pontos = ctk.CTkLabel(
        hud,
        text="PONTOS: 0",
        font=tema.FONTE_HUD,
        text_color=tema.NEON_GOLD,
    )
    label_pontos.pack(side="left", padx=24, pady=10)

    label_tempo = ctk.CTkLabel(
        hud,
        text=f"{DURACAO_JOGO_S}s",
        font=tema.FONTE_HUD,
        text_color=tema.TEXT_PRIMARY,
    )
    label_tempo.pack(side="right", padx=24, pady=10)

    arena = ctk.CTkFrame(
        centro,
        fg_color=tema.BG_SURFACE,
        border_width=3,
        border_color=tema.NEON_VIOLET,
        corner_radius=0,
    )
    arena.pack(expand=True, fill="both", pady=14)

    alvo = ctk.CTkButton(
        arena,
        text="",
        width=TAMANHO_ALVO,
        height=TAMANHO_ALVO,
        corner_radius=0,
        fg_color=tema.NEON_GOLD,
        hover_color="#FDE68A",
        text_color=tema.BG_DEEP,
        border_width=0,
    )

    # Painel exibido ao final da partida (formulário de nome, depois o ranking).
    tela_fim = ctk.CTkFrame(
        arena,
        fg_color=tema.BG_GLASS,
        border_width=3,
        border_color=tema.NEON_GOLD,
        corner_radius=0,
    )

    controles = ctk.CTkFrame(centro, fg_color="transparent")
    controles.pack(pady=(0, 16))

    botao_iniciar = ctk.CTkButton(
        controles,
        text="COMEÇAR",
        width=220,
        height=48,
        font=tema.FONTE_HUD,
        fg_color=tema.NEON_PURPLE,
        hover_color=tema.NEON_VIOLET,
        border_width=2,
        border_color=tema.NEON_GOLD,
        corner_radius=0,
    )
    botao_iniciar.pack()

    def cancelar_job(chave):
        job = estado[chave]
        if job is None:
            return
        try:
            arena.after_cancel(job)
        except Exception:
            pass
        estado[chave] = None

    def parar_timers():
        cancelar_job("job_alvo")
        cancelar_job("job_relogio")

    def posicionar_alvo_aleatorio():
        margem = 0.12
        alvo.place(
            relx=random.uniform(margem, 1 - margem),
            rely=random.uniform(margem, 1 - margem),
            anchor="center",
        )

    def agendar_proximo_alvo():
        if not estado["jogando"]:
            return

        posicionar_alvo_aleatorio()
        tempo_ms = random.randint(TEMPO_MIN_ALVO_MS, TEMPO_MAX_ALVO_MS)
        estado["job_alvo"] = arena.after(tempo_ms, agendar_proximo_alvo)

    def ao_clicar_alvo():
        if not estado["jogando"]:
            return

        estado["pontos"] += 2
        label_pontos.configure(text=f"PONTOS: {estado['pontos']}")
        cancelar_job("job_alvo")
        agendar_proximo_alvo()

    def ao_clicar_errado(_evento=None):
        # Clique na arena que não acertou o alvo (o alvo captura o clique
        # antes, então isso só dispara quando o clique foi no vazio).
        if not estado["jogando"]:
            return

        estado["pontos"] -= 1
        label_pontos.configure(text=f"PONTOS: {estado['pontos']}")

    def atualizar_relogio():
        if not estado["jogando"]:
            return

        estado["tempo_restante"] -= 1
        label_tempo.configure(text=f"{estado['tempo_restante']}s")

        if estado["tempo_restante"] <= 0:
            finalizar_jogo()
        else:
            estado["job_relogio"] = arena.after(1000, atualizar_relogio)

    # -----------------------------------------------------------------
    # Tela de fim de jogo: nome -> ranking
    # -----------------------------------------------------------------

    def limpar_tela_fim():
        for widget in tela_fim.winfo_children():
            widget.destroy()

    def esconder_tela_fim():
        tela_fim.place_forget()

    def mostrar_form_nome(pontos):
        limpar_tela_fim()

        ctk.CTkLabel(
            tela_fim,
            text="FIM DE JOGO",
            font=tema.FONTE_TITULO,
            text_color=tema.NEON_GOLD,
        ).pack(padx=40, pady=(30, 4))

        ctk.CTkLabel(
            tela_fim,
            text=f"{pontos} pontos",
            font=tema.FONTE_HUD,
            text_color=tema.TEXT_PRIMARY,
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            tela_fim,
            text="digite seu nome para entrar no ranking",
            font=tema.FONTE_MONO,
            text_color=tema.TEXT_MUTED,
        ).pack(pady=(0, 8))

        campo_nome = ctk.CTkEntry(
            tela_fim,
            width=220,
            height=40,
            justify="center",
            font=tema.FONTE_HUD,
            fg_color=tema.BG_ELEVATED,
            border_color=tema.NEON_PURPLE,
            border_width=2,
            corner_radius=0,
            placeholder_text="seu nome",
        )
        campo_nome.pack(pady=(0, 18))
        campo_nome.focus_set()

        botao_salvar = ctk.CTkButton(
            tela_fim,
            text="SALVAR",
            width=180,
            height=42,
            font=tema.FONTE_HUD,
            fg_color=tema.NEON_PURPLE,
            hover_color=tema.NEON_VIOLET,
            border_width=2,
            border_color=tema.NEON_GOLD,
            corner_radius=0,
        )
        botao_salvar.pack(pady=(0, 10))

        botao_pular = ctk.CTkButton(
            tela_fim,
            text="pular e ver ranking",
            width=180,
            height=30,
            font=tema.FONTE_MONO,
            fg_color="transparent",
            hover_color=tema.BG_ELEVATED,
            text_color=tema.TEXT_MUTED,
            border_width=0,
            corner_radius=0,
        )
        botao_pular.pack(pady=(0, 26))

        # Só deixa enviar uma vez: depois de clicar, os botões ficam bloqueados
        # e a tela muda para o ranking — não dá pra voltar e salvar de novo.
        def ao_salvar(_evento=None):
            nome = campo_nome.get().strip() or "ANÔNIMO"
            nome = nome[:NOME_MAX_CHARS].upper()

            campo_nome.configure(state="disabled")
            botao_salvar.configure(state="disabled", text="SALVANDO...")
            botao_pular.configure(state="disabled")

            def trabalho():
                enviar_pontuacao(nome, pontos)
                ranking = buscar_ranking(TAMANHO_RANKING)
                tela_fim.after(0, lambda: mostrar_ranking(ranking, nome))

            threading.Thread(target=trabalho, daemon=True).start()

        def ao_pular(_evento=None):
            campo_nome.configure(state="disabled")
            botao_salvar.configure(state="disabled")
            botao_pular.configure(state="disabled", text="carregando...")

            def trabalho():
                ranking = buscar_ranking(TAMANHO_RANKING)
                tela_fim.after(0, lambda: mostrar_ranking(ranking, None))

            threading.Thread(target=trabalho, daemon=True).start()

        campo_nome.bind("<Return>", ao_salvar)
        botao_salvar.configure(command=ao_salvar)
        botao_pular.configure(command=ao_pular)

        tela_fim.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_ranking(ranking, nome_destaque):
        limpar_tela_fim()

        ctk.CTkLabel(
            tela_fim,
            text="RANKING",
            font=tema.FONTE_TITULO,
            text_color=tema.NEON_GOLD,
        ).pack(padx=44, pady=(26, 4))

        if ranking is None:
            ctk.CTkLabel(
                tela_fim,
                text="sem conexão com o servidor do ranking",
                font=tema.FONTE_MONO,
                text_color=tema.NEON_MAGENTA,
            ).pack(padx=30, pady=(6, 16))
        else:
            ctk.CTkLabel(
                tela_fim,
                text="melhores pontuações",
                font=tema.FONTE_MONO,
                text_color=tema.TEXT_MUTED,
            ).pack(pady=(0, 14))

            corpo = ctk.CTkFrame(tela_fim, fg_color="transparent")
            corpo.pack(padx=30, pady=(0, 10))

            if not ranking:
                ctk.CTkLabel(
                    corpo,
                    text="ainda não há pontuações salvas",
                    font=tema.FONTE_MONO,
                    text_color=tema.TEXT_MUTED,
                ).pack(pady=20)

            for indice, item in enumerate(ranking):
                em_destaque = (
                    nome_destaque is not None and item.get("nome") == nome_destaque
                )
                texto_posicao = MEDALHAS.get(indice, f"{indice + 1:>2}.")

                linha = ctk.CTkFrame(
                    corpo,
                    fg_color=tema.BG_ELEVATED if em_destaque else "transparent",
                    corner_radius=0,
                    border_width=2 if em_destaque else 0,
                    border_color=tema.NEON_GOLD,
                )
                linha.pack(fill="x", pady=2)

                ctk.CTkLabel(
                    linha,
                    text=texto_posicao,
                    font=tema.FONTE_HUD,
                    text_color=tema.NEON_GOLD if indice == 0 else tema.TEXT_PRIMARY,
                    width=34,
                ).pack(side="left", padx=(8, 4), pady=6)

                ctk.CTkLabel(
                    linha,
                    text=item.get("nome", "?"),
                    font=tema.FONTE_HUD,
                    text_color=tema.TEXT_PRIMARY,
                    anchor="w",
                    width=150,
                ).pack(side="left", padx=4, pady=6)

                ctk.CTkLabel(
                    linha,
                    text=f'{item.get("pontuacao", 0)} pts',
                    font=tema.FONTE_MONO,
                    text_color=tema.NEON_CYAN,
                    width=70,
                    anchor="e",
                ).pack(side="right", padx=(4, 8), pady=6)

        rodape = ctk.CTkFrame(tela_fim, fg_color="transparent")
        rodape.pack(pady=(6, 26))

        ctk.CTkButton(
            rodape,
            text="JOGAR DE NOVO",
            width=180,
            height=42,
            font=tema.FONTE_HUD,
            fg_color=tema.NEON_PURPLE,
            hover_color=tema.NEON_VIOLET,
            border_width=2,
            border_color=tema.NEON_GOLD,
            corner_radius=0,
            command=jogar_novamente,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            rodape,
            text="HUB",
            width=110,
            height=42,
            font=tema.FONTE_HUD,
            fg_color=tema.BG_ELEVATED,
            hover_color=tema.NEON_VIOLET,
            border_width=2,
            border_color=tema.NEON_GOLD,
            corner_radius=0,
            command=finalizar_e_sair,
        ).pack(side="left", padx=6)

        tela_fim.place(relx=0.5, rely=0.5, anchor="center")

    def jogar_novamente():
        esconder_tela_fim()
        iniciar_partida()

    def finalizar_jogo():
        estado["jogando"] = False
        parar_timers()
        alvo.place_forget()
        mostrar_form_nome(estado["pontos"])

    def finalizar_e_sair():
        estado["jogando"] = False
        parar_timers()
        esconder_tela_fim()
        ir_home()

    def iniciar_partida():
        esconder_tela_fim()
        estado["pontos"] = 0
        estado["tempo_restante"] = DURACAO_JOGO_S
        estado["jogando"] = True

        label_pontos.configure(text="PONTOS: 0")
        label_tempo.configure(text=f"{DURACAO_JOGO_S}s")
        botao_iniciar.pack_forget()

        agendar_proximo_alvo()
        estado["job_relogio"] = arena.after(1000, atualizar_relogio)

    alvo.configure(command=ao_clicar_alvo)
    arena.bind("<Button-1>", ao_clicar_errado)
    botao_iniciar.configure(command=iniciar_partida)