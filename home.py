# home.py
# Tela inicial do SIGMA HUB com cards animados.

import os

import customtkinter as ctk

import fundo
import imagens
import tema

try:
    from PIL import Image

    PIL_DISPONIVEL = True
except ImportError:
    PIL_DISPONIVEL = False

PASTA_ICONES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "icones",
)

LARGURA_CARD_BASE = 250
ALTURA_CARD_BASE = 320
LARGURA_CARD_HOVER = 278
ALTURA_CARD_HOVER = 352

TAMANHO_ICONE = 120
PASSOS_ANIMACAO = 12
INTERVALO_MS = 10

LARGURA_AREA_CARDS = 960
ALTURA_AREA_CARDS = 380

TAMANHO_LOGO = 90
MARGEM_LOGO = 24
# Imagem do círculo: assets/logo.png (também aceita logo.jpg / avatar.png)


def _ease_in_out(progresso):
    return progresso * progresso * (3 - 2 * progresso)


def _carregar_icone(nome_arquivo):
    """Carrega um ícone da pasta assets/icones."""
    if not PIL_DISPONIVEL:
        return None

    caminho = os.path.join(PASTA_ICONES, nome_arquivo)
    if not os.path.isfile(caminho):
        return None

    try:
        with Image.open(caminho) as imagem_original:
            imagem = imagem_original.convert("RGB")
            imagem = imagem.resize(
                (TAMANHO_ICONE, TAMANHO_ICONE),
                Image.Resampling.LANCZOS,
            )
            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(TAMANHO_ICONE, TAMANHO_ICONE),
            )
    except Exception as erro:
        print(f"Erro ao carregar ícone '{nome_arquivo}': {erro}")
        return None


def construir_home(container, ir_equipe, ir_calculadora, ir_minigame):
    """Constrói a tela inicial do SIGMA HUB."""
    container.configure(fg_color=tema.BG_DEEP)
    canvas = fundo.criar_fundo_interativo(container)

    logo_circular = imagens.criar_logo_circular(TAMANHO_LOGO)
    canvas.logo_circular = logo_circular
    centro_logo = MARGEM_LOGO + TAMANHO_LOGO / 2
    canvas.create_image(
        centro_logo,
        centro_logo,
        image=logo_circular,
        tags=("ui", "logo_circular"),
    )

    id_titulo = canvas.create_text(
        0,
        0,
        text="SIGMA HUB",
        font=tema.FONTE_TITULO,
        fill=tema.NEON_CYAN,
        tags=("ui",),
    )
    id_subtitulo = canvas.create_text(
        0,
        0,
        text="escolha um módulo para entrar",
        font=tema.FONTE_SUB,
        fill=tema.TEXT_MUTED,
        tags=("ui",),
    )
    id_rodape = canvas.create_text(
        0,
        0,
        text="SIGMA HUB — feito pela equipe",
        font=tema.FONTE_MONO,
        fill=tema.TEXT_DIM,
        tags=("ui",),
    )

    idx_cor = {"i": 0}

    def pulsar_titulo():
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        canvas.itemconfigure(id_titulo, fill=tema.cor_ciclo(idx_cor["i"]))
        idx_cor["i"] += 1
        canvas.after(2400, pulsar_titulo)

    pulsar_titulo()

    def criar_card(arquivo_icone, titulo_txt, descricao_txt, comando, cor_borda, relx):
        estado = {
            "largura": LARGURA_CARD_BASE,
            "altura": ALTURA_CARD_BASE,
            "job": None,
        }

        card = ctk.CTkFrame(
            canvas,
            width=LARGURA_CARD_BASE,
            height=ALTURA_CARD_BASE,
            fg_color=tema.BG_GLASS,
            bg_color=tema.BG_GLASS,
            border_width=2,
            border_color=cor_borda,
            corner_radius=0,
        )
        card.pack_propagate(False)
        id_card = canvas.create_window(0, 0, anchor="center", window=card)
        card._id_canvas = id_card
        card._relx = relx

        icone_ctk = _carregar_icone(arquivo_icone)
        if icone_ctk is not None:
            icone_widget = ctk.CTkLabel(
                card,
                image=icone_ctk,
                text="",
                width=TAMANHO_ICONE,
                height=TAMANHO_ICONE,
                fg_color=tema.BG_GLASS,
                bg_color=tema.BG_GLASS,
                corner_radius=0,
            )
            icone_widget.image = icone_ctk
        else:
            icone_widget = ctk.CTkFrame(
                card,
                width=TAMANHO_ICONE,
                height=TAMANHO_ICONE,
                corner_radius=0,
                fg_color=tema.BG_ELEVATED,
                bg_color=tema.BG_GLASS,
                border_width=2,
                border_color=tema.NEON_GOLD,
            )
            icone_widget.pack_propagate(False)

        icone_widget.pack(pady=(36, 14))

        nome_label = ctk.CTkLabel(
            card,
            text=titulo_txt,
            font=tema.FONTE_CARD,
            text_color=tema.TEXT_PRIMARY,
        )
        nome_label.pack(pady=(0, 6))

        desc_label = ctk.CTkLabel(
            card,
            text=descricao_txt,
            font=tema.FONTE_MONO,
            text_color=tema.TEXT_MUTED,
            wraplength=200,
            justify="center",
        )
        desc_label.pack(pady=(0, 12))

        entrar_label = ctk.CTkLabel(
            card,
            text="→ entrar",
            font=tema.FONTE_MONO,
            text_color=cor_borda,
        )
        entrar_label.pack(side="bottom", pady=18)

        def animar(largura_alvo, altura_alvo, cor_alvo):
            if estado["job"] is not None:
                try:
                    card.after_cancel(estado["job"])
                except Exception:
                    pass
                estado["job"] = None

            largura_inicio = estado["largura"]
            altura_inicio = estado["altura"]

            def passo(n=0):
                if not card.winfo_exists():
                    return

                progresso = _ease_in_out(n / PASSOS_ANIMACAO)
                nova_largura = int(
                    largura_inicio + (largura_alvo - largura_inicio) * progresso
                )
                nova_altura = int(
                    altura_inicio + (altura_alvo - altura_inicio) * progresso
                )

                card.configure(width=nova_largura, height=nova_altura)
                estado["largura"] = nova_largura
                estado["altura"] = nova_altura

                if n >= PASSOS_ANIMACAO:
                    card.configure(border_color=cor_alvo)
                    estado["job"] = None
                else:
                    estado["job"] = card.after(INTERVALO_MS, lambda: passo(n + 1))

            passo()

        def ao_entrar(_evento=None):
            animar(LARGURA_CARD_HOVER, ALTURA_CARD_HOVER, tema.NEON_GOLD)

        def ao_sair(_evento=None):
            animar(LARGURA_CARD_BASE, ALTURA_CARD_BASE, cor_borda)

        def ao_clicar(_evento=None):
            comando()

        for widget in (card, icone_widget, nome_label, desc_label, entrar_label):
            widget.bind("<Enter>", ao_entrar)
            widget.bind("<Leave>", ao_sair)
            widget.bind("<Button-1>", ao_clicar)
            try:
                widget.configure(cursor="hand2")
            except Exception:
                pass

        return card

    cards = [
        criar_card(
            "equipe.png",
            "EQUIPE",
            "conheça quem fez o projeto",
            ir_equipe,
            tema.NEON_MAGENTA,
            0.16,
        ),
        criar_card(
            "calculadora.png",
            "CALCULADORA",
            "sigma calculator · aura 67",
            ir_calculadora,
            tema.NEON_CYAN,
            0.50,
        ),
        criar_card(
            "minigame.png",
            "MINI GAME",
            "versão base · em construção",
            ir_minigame,
            tema.NEON_PURPLE,
            0.84,
        ),
    ]

    def recentralizar(_evento=None):
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        largura = canvas.winfo_width()
        altura = canvas.winfo_height()
        cx = largura / 2
        cy = altura / 2

        canvas.coords(id_titulo, cx, cy - 250)
        canvas.coords(id_subtitulo, cx, cy - 208)
        canvas.coords(id_rodape, cx, cy + 250)

        origem_x = cx - LARGURA_AREA_CARDS / 2
        for card in cards:
            canvas.coords(
                card._id_canvas,
                origem_x + card._relx * LARGURA_AREA_CARDS,
                cy + 20,
            )

        canvas.tag_raise("ui")

    canvas.bind("<Configure>", recentralizar, add="+")
    canvas.after(30, recentralizar)
