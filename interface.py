# interface.py
# SIGMA CALCULATOR — visual neon com animações e teclado físico.
import os
import math
import platform
import subprocess
import tkinter as tk

import customtkinter as ctk

import fundo
import matematica
import tema

if platform.system() == "Windows":
    import winsound

    def tocar_som(arquivo):
        try:
            winsound.PlaySound(
                arquivo,
                winsound.SND_FILENAME | winsound.SND_ASYNC,
            )
        except Exception:
            pass
else:
    def tocar_som(arquivo):
        try:
            subprocess.Popen(
                ["paplay", arquivo],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass


def _flash_widget(widget, cor_borda, cor_original, ms=90):
    try:
        widget.configure(border_color=cor_borda)
        widget.after(ms, lambda: widget.configure(border_color=cor_original))
    except Exception:
        pass


def _botao_calc(pai, texto, fg, hover, borda, comando, largura=78, altura=64):
    """Cria um botão da calculadora com microanimação ao clicar."""

    def executar():
        try:
            btn.configure(fg_color=hover)
            btn.after(60, lambda: btn.configure(fg_color=fg))
        except Exception:
            pass
        comando()

    btn = ctk.CTkButton(
        pai,
        text=texto,
        width=largura,
        height=altura,
        font=tema.FONTE_BOTAO,
        text_color=tema.TEXT_PRIMARY,
        fg_color=fg,
        hover_color=hover,
        border_width=2,
        border_color=borda,
        corner_radius=0,
        command=executar,
    )
    return btn


def construir_calculadora(
    container,
    ir_home,
    funcao_soma,
    funcao_subtracao,
    funcao_multiplicacao,
    funcao_divisao,
):
    container.configure(fg_color=tema.BG_DEEP)

    memoria = {"primeiro_numero": None, "operacao": None}
    aura = {"quantidade": 0}
    operacoes = {
        "+": funcao_soma,
        "-": funcao_subtracao,
        "*": funcao_multiplicacao,
        "/": funcao_divisao,
    }

    canvas = fundo.criar_fundo_interativo(container)

    botao_voltar = ctk.CTkButton(
        canvas,
        text="←  Hub",
        width=100,
        height=36,
        font=tema.FONTE_HUD,
        fg_color=tema.BG_ELEVATED,
        bg_color="transparent",
        hover_color=tema.NEON_VIOLET,
        border_width=2,
        border_color=tema.NEON_PURPLE,
        corner_radius=0,
        command=ir_home,
    )
    id_voltar = canvas.create_window(28, 22, anchor="nw", window=botao_voltar)

    id_nome_app = canvas.create_text(
        0,
        0,
        text="Σ  SIGMA CALCULATOR",
        font=("Consolas", 18, "bold"),
        fill=tema.NEON_GOLD,
        anchor="ne",
        tags=("ui",),
    )
    id_titulo = canvas.create_text(
        0,
        0,
        text="S I G M A",
        font=tema.FONTE_TITULO,
        fill=tema.NEON_CYAN,
        tags=("ui",),
    )
    id_subtitulo = canvas.create_text(
        0,
        0,
        text="calculadora · aura engine v2",
        font=tema.FONTE_SUB,
        fill=tema.TEXT_MUTED,
        tags=("ui",),
    )
    id_rodape = canvas.create_text(
        0,
        0,
        text="FARM  ·  CALCULATE  ·  ASCEND          67 = AURA AWAKENING",
        font=tema.FONTE_MONO,
        fill=tema.TEXT_DIM,
        tags=("ui",),
    )

    cor_titulo_idx = {"i": 0}

    def animar_titulo():
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return
        canvas.itemconfigure(id_titulo, fill=tema.cor_ciclo(cor_titulo_idx["i"]))
        cor_titulo_idx["i"] += 1
        canvas.after(2200, animar_titulo)

    animar_titulo()

    col_aura = ctk.CTkFrame(
        canvas,
        width=300,
        height=520,
        fg_color=tema.BG_GLASS,
        bg_color="transparent",
        border_width=2,
        border_color=tema.NEON_PURPLE,
        corner_radius=0,
    )
    col_aura.pack_propagate(False)

    col_calc = ctk.CTkFrame(
        canvas,
        fg_color=tema.BG_GLASS,
        bg_color="transparent",
        border_width=2,
        border_color=tema.NEON_CYAN,
        corner_radius=0,
    )

    id_aura = canvas.create_window(0, 0, anchor="center", window=col_aura)
    id_calc = canvas.create_window(0, 0, anchor="center", window=col_calc)

    def redesenhar_barras():
        canvas.delete("barra_neon")
        largura = max(canvas.winfo_width(), 1)
        canvas.create_rectangle(
            0, 0, largura, 4,
            fill=tema.NEON_CYAN, outline="", tags=("barra_neon", "ui"),
        )
        canvas.create_rectangle(
            0, 4, largura, 7,
            fill=tema.NEON_MAGENTA, outline="", tags=("barra_neon", "ui"),
        )

    def recentralizar(_evento=None):
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        largura = float(canvas.winfo_width())
        altura = float(canvas.winfo_height())
        if largura < 20 or altura < 20:
            return

        largura_aura = 300
        altura_aura = 520
        largura_calc = max(int(col_calc.winfo_reqwidth()), 1)
        altura_calc = max(int(col_calc.winfo_reqheight()), 1)
        altura_paineis = max(altura_aura, altura_calc)

        gap_colunas = 32
        altura_topo = 64
        altura_rodape = 32
        margem = 20

        bloco_w = largura_aura + gap_colunas + largura_calc
        bloco_h = altura_topo + altura_paineis + altura_rodape

        centro_x = largura / 2.0
        centro_y = altura / 2.0

        bloco_esquerdo = centro_x - bloco_w / 2.0
        bloco_topo = centro_y - bloco_h / 2.0

        if bloco_esquerdo < margem:
            bloco_esquerdo = margem
        if bloco_esquerdo + bloco_w > largura - margem:
            bloco_esquerdo = max(margem, largura - margem - bloco_w)

        if bloco_topo < 48:
            bloco_topo = 48
        if bloco_topo + bloco_h > altura - margem:
            bloco_topo = max(48, altura - margem - bloco_h)

        painel_cx_aura = bloco_esquerdo + largura_aura / 2.0
        painel_cx_calc = bloco_esquerdo + largura_aura + gap_colunas + largura_calc / 2.0
        painel_cy = bloco_topo + altura_topo + altura_paineis / 2.0

        canvas.itemconfigure(id_aura, width=largura_aura, height=altura_aura)
        canvas.itemconfigure(id_calc, width=largura_calc, height=altura_calc)

        canvas.coords(id_voltar, 28, 22)
        canvas.coords(id_nome_app, largura - 28, 40)
        canvas.coords(id_aura, painel_cx_aura, painel_cy)
        canvas.coords(id_calc, painel_cx_calc, painel_cy)
        canvas.coords(id_titulo, centro_x, bloco_topo + 18)
        canvas.coords(id_subtitulo, centro_x, bloco_topo + 48)
        canvas.coords(id_rodape, centro_x, painel_cy + altura_paineis / 2.0 + 18)
        redesenhar_barras()
        canvas.tag_raise("ui")

    def ao_redimensionar(_evento=None):
        canvas.after_idle(recentralizar)

    canvas.bind("<Configure>", ao_redimensionar, add="+")
    canvas.bind("<Map>", ao_redimensionar, add="+")
    janela_raiz = canvas.winfo_toplevel()
    id_bind_janela = janela_raiz.bind("<Configure>", ao_redimensionar, add="+")

    def ao_destruir_canvas(_evento=None):
        try:
            janela_raiz.unbind("<Configure>", id_bind_janela)
        except Exception:
            pass

    canvas.bind("<Destroy>", ao_destruir_canvas, add="+")
    canvas.after(40, recentralizar)
    canvas.after(200, recentralizar)

    ctk.CTkLabel(
        col_aura,
        text="⚡ AURA CORE",
        font=tema.FONTE_HUD,
        text_color=tema.NEON_GOLD,
    ).pack(pady=(24, 4))

    contador_aura = ctk.CTkLabel(
        col_aura,
        text="0",
        font=("Consolas", 48, "bold"),
        text_color=tema.NEON_CYAN,
    )
    contador_aura.pack()

    ctk.CTkLabel(
        col_aura,
        text="AURA",
        font=tema.FONTE_MONO,
        text_color=tema.TEXT_MUTED,
    ).pack()

    nivel_aura = ctk.CTkLabel(
        col_aura,
        text="INICIANTE",
        font=tema.FONTE_HUD,
        text_color=tema.NEON_PINK,
    )
    nivel_aura.pack(pady=(8, 16))

    barra_aura = ctk.CTkProgressBar(
        col_aura,
        width=220,
        height=14,
        corner_radius=0,
        fg_color=tema.BG_DEEP,
        progress_color=tema.NEON_MAGENTA,
        border_width=1,
        border_color=tema.NEON_PURPLE,
    )
    barra_aura.pack(pady=(0, 6))
    barra_aura.set(0)

    label_progresso = ctk.CTkLabel(
        col_aura,
        text="0 / 67 até o próximo nível",
        font=tema.FONTE_MONO,
        text_color=tema.TEXT_DIM,
    )
    label_progresso.pack(pady=(0, 20))

    anel_canvas = tk.Canvas(
        col_aura,
        width=160,
        height=160,
        bg=tema.BG_GLASS,
        highlightthickness=0,
        bd=0,
    )
    anel_canvas.pack(pady=(0, 12))

    angulo_anel = {"v": 0}

    def desenhar_anel():
        try:
            if not anel_canvas.winfo_exists():
                return

            anel_canvas.delete("anel")
            cx, cy, raio = 80, 80, 62
            angulo_anel["v"] = (angulo_anel["v"] + 3) % 360

            quantidade = aura["quantidade"]
            progresso = (quantidade % 67) / 67 if quantidade > 0 else 0

            anel_canvas.create_oval(
                cx - raio,
                cy - raio,
                cx + raio,
                cy + raio,
                outline=tema.BG_DEEP,
                width=10,
                tags="anel",
            )

            for i in range(int(progresso * 60)):
                angulo = math.radians(angulo_anel["v"] + i * 6)
                x1 = cx + (raio - 5) * math.cos(angulo)
                y1 = cy + (raio - 5) * math.sin(angulo)
                x2 = cx + (raio + 5) * math.cos(angulo)
                y2 = cy + (raio + 5) * math.sin(angulo)
                anel_canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=tema.cor_ciclo(i),
                    width=3,
                    tags="anel",
                )

            anel_canvas.create_text(
                cx,
                cy,
                text="67",
                font=("Consolas", 22, "bold"),
                fill=tema.NEON_GOLD,
                tags="anel",
            )
            anel_canvas.after(40, desenhar_anel)
        except Exception:
            pass

    desenhar_anel()

    texto_67 = ctk.CTkLabel(
        col_aura,
        text="",
        font=("Consolas", 56, "bold"),
        text_color=tema.NEON_GOLD,
    )
    texto_67.place(relx=0.5, rely=0.55, anchor="center")

    def animacao_67(etapa=0):
        if not texto_67.winfo_exists():
            return

        if etapa < len(tema.CICLO_NEON):
            cor = tema.CICLO_NEON[etapa]
            texto_67.configure(text="67", text_color=cor)
            col_aura.configure(border_color=cor)
            col_calc.configure(border_color=cor)
            canvas.itemconfigure(id_titulo, fill=cor)
            col_aura.after(90, lambda: animacao_67(etapa + 1))
            return

        texto_67.configure(text="")
        col_aura.configure(border_color=tema.NEON_PURPLE)
        col_calc.configure(border_color=tema.NEON_CYAN)

    def farmar_aura():
        aura["quantidade"] += 1
        quantidade = aura["quantidade"]
        contador_aura.configure(text=f"{quantidade:,}")

        resto = quantidade % 67
        barra_aura.set(resto / 67 if resto else 1.0)
        label_progresso.configure(text=f"{resto} / 67 até o próximo nível")

        if quantidade >= 67:
            nivel_aura.configure(
                text=f"NÍVEL {quantidade // 67}",
                text_color=tema.NEON_GOLD,
            )
        else:
            nivel_aura.configure(text="INICIANTE", text_color=tema.NEON_PINK)

        contador_aura.configure(text_color=tema.NEON_MAGENTA)
        contador_aura.after(
            120,
            lambda: contador_aura.configure(text_color=tema.NEON_CYAN),
        )

        if quantidade % 67 == 0:
        # Agora chama a função para tocar o som
          caminho_som = os.path.join("assets", "67.wav")  # ou apenas "67.wav" se estiver na raiz
          tocar_som(caminho_som)
          animacao_67()

    ctk.CTkButton(
        col_aura,
        text="✦  FARMAR AURA",
        width=240,
        height=54,
        font=tema.FONTE_HUD,
        text_color=tema.BG_DEEP,
        fg_color=tema.NEON_GOLD,
        hover_color=tema.NEON_CYAN,
        border_width=0,
        corner_radius=0,
        command=farmar_aura,
    ).pack(side="bottom", pady=24)

    ctk.CTkLabel(
        col_aura,
        text="clique e absorva energia",
        font=tema.FONTE_MONO,
        text_color=tema.TEXT_DIM,
    ).pack(side="bottom", pady=(0, 8))

    moldura_display = ctk.CTkFrame(
        col_calc,
        fg_color=tema.BG_DEEP,
        border_width=2,
        border_color=tema.NEON_CYAN,
        corner_radius=0,
    )
    moldura_display.pack(padx=20, pady=(20, 12), fill="x")

    expressao_label = ctk.CTkLabel(
        moldura_display,
        text="",
        font=tema.FONTE_MONO,
        text_color=tema.TEXT_DIM,
        anchor="e",
    )
    expressao_label.pack(fill="x", padx=16, pady=(10, 0))

    display = ctk.CTkEntry(
        moldura_display,
        height=64,
        font=tema.FONTE_DISPLAY,
        justify="right",
        fg_color="transparent",
        border_width=0,
        text_color=tema.TEXT_PRIMARY,
        placeholder_text="0",
        corner_radius=0,
    )
    display.pack(padx=12, pady=(0, 12), fill="x")

    frame_teclado = ctk.CTkFrame(
        col_calc,
        fg_color=tema.BG_SURFACE,
        border_width=1,
        border_color=tema.NEON_VIOLET,
        corner_radius=0,
    )
    frame_teclado.pack(padx=16, pady=(0, 20))

    def pulso_display():
        _flash_widget(moldura_display, tema.NEON_MAGENTA, tema.NEON_CYAN, 100)

    def atualizar_expressao():
        primeiro = memoria["primeiro_numero"]
        operacao = memoria["operacao"]

        if primeiro is None or not operacao:
            expressao_label.configure(text="")
            return

        simbolos = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        simbolo = simbolos.get(operacao, operacao)
        expressao_label.configure(
            text=f"{matematica.formatar_resultado(primeiro)} {simbolo}"
        )

    def digitar_numero(numero):
        pulso_display()
        atual = display.get()

        if numero == "." and "." in atual:
            return

        if atual in ("0", "ERRO") and numero != ".":
            display.delete(0, "end")

        display.insert("end", numero)

    def escolher_operacao(operacao):
        try:
            valor = float(display.get().replace(",", "."))
        except ValueError:
            return

        memoria["primeiro_numero"] = valor
        memoria["operacao"] = operacao
        display.delete(0, "end")
        atualizar_expressao()
        pulso_display()

    def limpar_tela():
        display.delete(0, "end")
        memoria["primeiro_numero"] = None
        memoria["operacao"] = None
        expressao_label.configure(text="")
        _flash_widget(moldura_display, tema.NEON_MAGENTA, tema.NEON_CYAN, 150)

    def calcular_resultado():
        try:
            segundo = float(display.get().replace(",", "."))
            primeiro = memoria["primeiro_numero"]
            operacao = memoria["operacao"]

            if primeiro is None or operacao is None:
                return

            funcao = operacoes.get(operacao)
            if funcao is None:
                return

            resultado = funcao(primeiro, segundo)
            display.delete(0, "end")
            display.insert(0, matematica.formatar_resultado(resultado))
            expressao_label.configure(text="")
            memoria["primeiro_numero"] = None
            memoria["operacao"] = None

            for i, cor in enumerate(tema.CICLO_NEON[:4]):
                moldura_display.after(
                    i * 60,
                    lambda c=cor: moldura_display.configure(border_color=c),
                )
            moldura_display.after(
                280,
                lambda: moldura_display.configure(border_color=tema.NEON_CYAN),
            )
        except (ValueError, ZeroDivisionError):
            display.delete(0, "end")
            display.insert(0, "ERRO")
            moldura_display.configure(border_color=tema.NEON_MAGENTA)

    botoes = [
        ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("÷", 0, 3),
        ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("×", 1, 3),
        ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("−", 2, 3),
        ("C", 3, 0), ("0", 3, 1), (".", 3, 2), ("+", 3, 3),
        ("=", 4, 0),
    ]
    mapa_operacoes = {"÷": "/", "×": "*", "−": "-"}

    for texto, linha, coluna in botoes:
        operador = mapa_operacoes.get(texto, texto)

        if texto in mapa_operacoes or texto == "+":
            comando = lambda op=operador: escolher_operacao(op)
            fg, hover, borda = tema.BTN_OP
        elif texto == "=":
            comando = calcular_resultado
            fg, hover, borda = tema.BTN_EQ
        elif texto == "C":
            comando = limpar_tela
            fg, hover, borda = tema.BTN_CLR
        else:
            comando = lambda n=texto: digitar_numero(n)
            fg, hover, borda = tema.BTN_NUM

        btn = _botao_calc(frame_teclado, texto, fg, hover, borda, comando)
        if texto == "=":
            btn.grid(row=linha, column=coluna, columnspan=4, padx=7, pady=7, sticky="ew")
        else:
            btn.grid(row=linha, column=coluna, padx=7, pady=7)

    for coluna in range(4):
        frame_teclado.grid_columnconfigure(coluna, weight=1)

    mapa_teclas = {
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
        "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
        "period": ".", "comma": ".", "KP_Decimal": ".",
        "+": "+", "plus": "+", "-": "-", "minus": "-",
        "*": "*", "asterisk": "*", "/": "/", "slash": "/",
        "KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "*", "KP_Divide": "/",
        "Return": "=", "equal": "=", "KP_Enter": "=",
        "Escape": "C", "BackSpace": "BACKSPACE",
    }

    def ao_tecla(evento):
        chave = evento.keysym
        if chave not in mapa_teclas:
            return

        acao = mapa_teclas[chave]
        if acao == "=":
            calcular_resultado()
        elif acao == "C":
            limpar_tela()
        elif acao == "BACKSPACE":
            valor = display.get()
            if valor:
                display.delete(len(valor) - 1, "end")
        elif acao in ("+", "-", "*", "/"):
            escolher_operacao(acao)
        else:
            digitar_numero(acao)

    for widget in (container, canvas, col_calc, display, frame_teclado):
        widget.bind("<Key>", ao_tecla, add="+")

    display.focus_set()
    recentralizar()
