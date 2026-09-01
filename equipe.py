# equipe.py
# Galeria da equipe: molduras retrato com hover e visualizador em tela cheia.

import glob
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

PASTA_FOTOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "equipe",
)

EXTENSOES_ACEITAS = ("*.jpg", "*.jpeg", "*.png", "*.webp")

LARGURA_BASE = 190
ALTURA_BASE = 250
LARGURA_HOVER = 208
ALTURA_HOVER = 290

COLUNAS = 4
MARGEM_GALERIA = 20
PASSOS_ANIMACAO = 8
INTERVALO_MS = 12

MAX_LARGURA_GRANDE = 780
MAX_ALTURA_GRANDE = 740


def _listar_fotos():
    """Retorna todas as imagens encontradas na pasta da equipe."""
    if not os.path.isdir(PASTA_FOTOS):
        return []

    arquivos = []
    for padrao in EXTENSOES_ACEITAS:
        arquivos.extend(glob.glob(os.path.join(PASTA_FOTOS, padrao)))

    return sorted(arquivos)


def _cortar_retrato(imagem, largura_alvo, altura_alvo):
    """Corta a imagem centralizada para a proporção da moldura."""
    razao_alvo = largura_alvo / altura_alvo
    largura, altura = imagem.size

    if altura == 0:
        return imagem

    razao_atual = largura / altura

    if razao_atual > razao_alvo:
        nova_largura = int(altura * razao_alvo)
        esquerda = (largura - nova_largura) // 2
        imagem = imagem.crop((esquerda, 0, esquerda + nova_largura, altura))
    else:
        nova_altura = int(largura / razao_alvo)
        topo = (altura - nova_altura) // 2
        imagem = imagem.crop((0, topo, largura, topo + nova_altura))

    return imagem.resize((largura_alvo, altura_alvo), Image.Resampling.LANCZOS)


def _carregar_miniatura(caminho, largura, altura):
    """Carrega e prepara uma miniatura para o CustomTkinter."""
    if not PIL_DISPONIVEL:
        return None

    try:
        with Image.open(caminho) as imagem_original:
            imagem = imagem_original.convert("RGB")
            imagem = _cortar_retrato(imagem, largura, altura)
            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(largura, altura),
            )
    except Exception as erro:
        print(f"Erro ao carregar imagem '{caminho}': {erro}")
        return None


def _carregar_grande(caminho):
    """Carrega a foto inteira, sem cortar, reduzindo para caber na tela."""
    if not PIL_DISPONIVEL:
        return None

    try:
        with Image.open(caminho) as imagem_original:
            imagem = imagem_original.convert("RGB")
            largura, altura = imagem.size

            if largura <= 0 or altura <= 0:
                return None

            escala = min(
                MAX_LARGURA_GRANDE / largura,
                MAX_ALTURA_GRANDE / altura,
                1.0,
            )
            nova_largura = max(int(largura * escala), 1)
            nova_altura = max(int(altura * escala), 1)
            imagem = imagem.resize(
                (nova_largura, nova_altura),
                Image.Resampling.LANCZOS,
            )
            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(nova_largura, nova_altura),
            )
    except Exception as erro:
        print(f"Erro ao carregar imagem '{caminho}': {erro}")
        return None


def construir_equipe(container, ir_home):
    container.configure(fg_color=tema.BG_DEEP)
    canvas = fundo.criar_fundo_interativo(container)

    botao_voltar = ctk.CTkButton(
        canvas,
        text="←  Hub",
        width=110,
        height=38,
        font=tema.FONTE_HUD,
        fg_color=tema.BG_ELEVATED,
        bg_color="transparent",
        hover_color=tema.NEON_VIOLET,
        border_width=2,
        border_color=tema.NEON_GOLD,
        corner_radius=0,
        command=ir_home,
    )
    canvas.create_window(30, 22, anchor="nw", window=botao_voltar)

    id_titulo = canvas.create_text(
        0,
        0,
        text="EQUIPE",
        font=("Consolas", 26, "bold"),
        fill=tema.NEON_GOLD,
        anchor="w",
        tags=("ui",),
    )

    id_overlay = canvas.create_image(0, 0, anchor="nw", tags=("overlay_galeria",))
    overlay_ref = {"img": None, "geo": (0, 0, 0, 0)}
    scroll = {"y": 0}

    largura_celula = LARGURA_HOVER + 28
    altura_celula = ALTURA_HOVER + 34
    itens = []

    def geometria_painel():
        largura = max(canvas.winfo_width(), 40)
        altura = max(canvas.winfo_height(), 40)
        x = 30
        y = 72
        w = max(largura - 60, 40)
        h = max(altura - 96, 40)
        return x, y, w, h

    def atualizar_overlay():
        x, y, w, h = geometria_painel()
        anterior = overlay_ref["geo"]
        if (x, y, w, h) == anterior and overlay_ref["img"] is not None:
            canvas.coords(id_overlay, x, y)
            return

        foto = imagens.painel_translucido(w, h, alpha=118)
        overlay_ref["img"] = foto
        overlay_ref["geo"] = (x, y, w, h)
        canvas.itemconfigure(id_overlay, image=foto)
        canvas.coords(id_overlay, x, y)
        canvas.tag_lower("overlay_galeria")
        canvas.tag_raise("overlay_galeria")
        canvas.tag_lower("video_fundo")

    fotos = _listar_fotos()
    estado_visualizador = {"overlay": None}

    def fechar_visualizador():
        overlay = estado_visualizador["overlay"]
        if overlay is not None:
            overlay.destroy()
            estado_visualizador["overlay"] = None

    def abrir_visualizador(caminho):
        fechar_visualizador()

        overlay = ctk.CTkFrame(container, fg_color=tema.BG_DEEP, corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lift()
        estado_visualizador["overlay"] = overlay

        quadro = ctk.CTkFrame(
            overlay,
            fg_color=tema.BG_GLASS,
            border_width=3,
            border_color=tema.NEON_GOLD,
            corner_radius=0,
        )
        quadro.place(relx=0.5, rely=0.5, anchor="center")

        imagem_grande = _carregar_grande(caminho)
        if imagem_grande is not None:
            label_imagem = ctk.CTkLabel(quadro, image=imagem_grande, text="")
            label_imagem.image = imagem_grande
        else:
            label_imagem = ctk.CTkLabel(
                quadro,
                text=os.path.basename(caminho),
                font=tema.FONTE_MONO,
                text_color=tema.TEXT_PRIMARY,
            )

        label_imagem.pack(padx=18, pady=(18, 10))

        ctk.CTkButton(
            quadro,
            text="fechar",
            width=140,
            height=38,
            font=tema.FONTE_HUD,
            fg_color=tema.NEON_VIOLET,
            hover_color=tema.NEON_PURPLE,
            border_width=2,
            border_color=tema.NEON_GOLD,
            corner_radius=0,
            command=fechar_visualizador,
        ).pack(pady=(0, 18))

        overlay.bind("<Button-1>", lambda _e: fechar_visualizador())
        overlay.bind("<Escape>", lambda _e: fechar_visualizador())
        overlay.focus_set()

    id_vazio = None
    if not fotos:
        id_vazio = canvas.create_text(
            0,
            0,
            text=(
                "nenhuma foto ainda\n\n"
                "coloque as fotos da equipe dentro de:\n"
                "assets/equipe/"
            ),
            font=tema.FONTE_MONO,
            fill=tema.NEON_LILAC,
            justify="center",
            tags=("ui",),
        )

    for indice, caminho in enumerate(fotos):
        linha = indice // COLUNAS
        coluna = indice % COLUNAS

        estado = {
            "largura": LARGURA_BASE,
            "altura": ALTURA_BASE,
            "job": None,
        }

        miniatura_base = _carregar_miniatura(caminho, LARGURA_BASE, ALTURA_BASE)
        miniatura_hover = _carregar_miniatura(caminho, LARGURA_HOVER, ALTURA_HOVER)

        moldura = ctk.CTkFrame(
            canvas,
            width=LARGURA_BASE,
            height=ALTURA_BASE,
            fg_color=tema.BG_GLASS,
            bg_color=tema.BG_GLASS,
            corner_radius=0,
            border_width=2,
            border_color=tema.NEON_VIOLET,
        )
        moldura.pack_propagate(False)

        id_moldura = canvas.create_window(0, 0, anchor="s", window=moldura)

        if miniatura_base is not None:
            foto_label = ctk.CTkLabel(
                moldura,
                image=miniatura_base,
                text="",
                fg_color=tema.BG_GLASS,
                bg_color=tema.BG_GLASS,
                corner_radius=0,
            )
            foto_label.image_base = miniatura_base
            foto_label.image_hover = miniatura_hover
        else:
            foto_label = ctk.CTkLabel(
                moldura,
                text=os.path.basename(caminho),
                font=tema.FONTE_MONO,
                text_color=tema.TEXT_PRIMARY,
                wraplength=LARGURA_BASE - 10,
                fg_color=tema.BG_GLASS,
                bg_color=tema.BG_GLASS,
                corner_radius=0,
            )

        foto_label.place(relx=0.5, rely=0.5, anchor="center")

        def animar(
            moldura=moldura,
            estado=estado,
            foto_label=foto_label,
            miniatura_hover=miniatura_hover,
            miniatura_base=miniatura_base,
            largura_alvo=LARGURA_BASE,
            altura_alvo=ALTURA_BASE,
            cor_alvo=tema.NEON_VIOLET,
            entrando=False,
        ):
            if estado["job"] is not None:
                try:
                    moldura.after_cancel(estado["job"])
                except Exception:
                    pass
                estado["job"] = None

            largura_inicio = estado["largura"]
            altura_inicio = estado["altura"]

            if entrando and miniatura_hover is not None:
                foto_label.configure(image=miniatura_hover)
            elif not entrando and miniatura_base is not None:
                foto_label.configure(image=miniatura_base)

            def passo(n=0):
                if not moldura.winfo_exists():
                    return

                progresso = n / PASSOS_ANIMACAO
                nova_largura = int(
                    largura_inicio + (largura_alvo - largura_inicio) * progresso
                )
                nova_altura = int(
                    altura_inicio + (altura_alvo - altura_inicio) * progresso
                )

                moldura.configure(width=nova_largura, height=nova_altura)
                estado["largura"] = nova_largura
                estado["altura"] = nova_altura

                if n >= PASSOS_ANIMACAO:
                    moldura.configure(border_color=cor_alvo)
                    estado["job"] = None
                else:
                    estado["job"] = moldura.after(INTERVALO_MS, lambda: passo(n + 1))

            passo()

        def ao_entrar(_evento=None, animar=animar):
            animar(
                largura_alvo=LARGURA_HOVER,
                altura_alvo=ALTURA_HOVER,
                cor_alvo=tema.NEON_GOLD,
                entrando=True,
            )

        def ao_sair(_evento=None, animar=animar):
            animar(
                largura_alvo=LARGURA_BASE,
                altura_alvo=ALTURA_BASE,
                cor_alvo=tema.NEON_VIOLET,
                entrando=False,
            )

        def ao_clicar(_evento=None, caminho=caminho):
            abrir_visualizador(caminho)

        for widget in (moldura, foto_label):
            widget.bind("<Enter>", ao_entrar)
            widget.bind("<Leave>", ao_sair)
            widget.bind("<Button-1>", ao_clicar)
            try:
                widget.configure(cursor="hand2")
            except Exception:
                pass

        itens.append({
            "id": id_moldura,
            "linha": linha,
            "coluna": coluna,
        })

    def linhas_totais():
        if not itens:
            return 1
        return max(item["linha"] for item in itens) + 1

    def aplicar_layout():
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        atualizar_overlay()
        x, y, w, h = geometria_painel()
        canvas.coords(id_titulo, 160, 40)

        conteudo_h = linhas_totais() * altura_celula + MARGEM_GALERIA
        max_scroll = max(0, conteudo_h - h + MARGEM_GALERIA)
        if scroll["y"] > max_scroll:
            scroll["y"] = max_scroll
        if scroll["y"] < 0:
            scroll["y"] = 0

        if id_vazio is not None:
            canvas.coords(id_vazio, x + w / 2, y + h / 2)

        for item in itens:
            cx = x + MARGEM_GALERIA + item["coluna"] * largura_celula + largura_celula / 2
            base_y = (
                y
                + MARGEM_GALERIA
                + (item["linha"] + 1) * altura_celula
                - 10
                - scroll["y"]
            )
            canvas.coords(item["id"], cx, base_y)
            visivel = y + 8 < base_y < y + h + ALTURA_HOVER
            estado = "normal" if visivel else "hidden"
            canvas.itemconfigure(item["id"], state=estado)

        canvas.tag_raise("ui")

    def ao_scroll(evento):
        delta = getattr(evento, "delta", 0)
        if delta == 0:
            passo = -40 if getattr(evento, "num", 0) == 4 else 40
        else:
            passo = -40 if delta > 0 else 40
        scroll["y"] += passo
        aplicar_layout()

    def ao_redimensionar(_evento=None):
        overlay_ref["geo"] = (0, 0, 0, 0)
        canvas.after_idle(aplicar_layout)

    canvas.bind("<Configure>", ao_redimensionar, add="+")
    canvas.bind("<MouseWheel>", ao_scroll, add="+")
    canvas.bind("<Button-4>", ao_scroll, add="+")
    canvas.bind("<Button-5>", ao_scroll, add="+")
    canvas.after(30, aplicar_layout)
    canvas.after(200, aplicar_layout)
