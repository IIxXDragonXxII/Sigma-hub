# hub.py
# Navegação em uma única janela: cada tela limpa o container e redesenha.

import customtkinter as ctk

import equipe
import home
import interface
import minigame
import musica
import tema


def _montar_controles_musica(janela):
    """Controles fixos na janela, fora do container que troca de tela."""
    barra = ctk.CTkFrame(
        janela,
        fg_color=tema.BG_GLASS,
        bg_color=tema.BG_DEEP,
        border_width=2,
        border_color=tema.NEON_PURPLE,
        corner_radius=0,
    )
    barra.place(relx=0.99, rely=0.98, anchor="se")

    texto_mudo = "🔇  mudo" if musica.esta_mudo() else "🔊  som"
    botao_mudo = ctk.CTkButton(
        barra,
        text=texto_mudo,
        width=110,
        height=32,
        font=tema.FONTE_HUD,
        fg_color=tema.BG_ELEVATED,
        hover_color=tema.NEON_VIOLET,
        border_width=1,
        border_color=tema.NEON_GOLD,
        corner_radius=0,
    )
    botao_mudo.pack(side="left", padx=(10, 8), pady=8)

    slider = ctk.CTkSlider(
        barra,
        width=110,
        from_=0,
        to=1,
        corner_radius=0,
        button_corner_radius=0,
        command=lambda valor: musica.definir_volume(valor),
    )
    slider.set(musica.volume_atual())
    slider.pack(side="left", padx=(0, 12), pady=8)

    def ao_mudo():
        mudo = musica.alternar_mudo()
        botao_mudo.configure(text="🔇  mudo" if mudo else "🔊  som")

    botao_mudo.configure(command=ao_mudo)

    if not musica.esta_pronta():
        botao_mudo.configure(state="disabled", text="sem música")
        slider.configure(state="disabled")

    return barra


def iniciar_app(
    janela,
    funcao_soma,
    funcao_subtracao,
    funcao_multiplicacao,
    funcao_divisao,
):
    """Inicializa o hub e configura a navegação entre as telas."""
    janela.configure(fg_color=tema.BG_DEEP)
    musica.iniciar()

    container = ctk.CTkFrame(
        janela,
        fg_color=tema.BG_DEEP,
        bg_color=tema.BG_DEEP,
        corner_radius=0,
        border_width=0,
    )
    container.pack(expand=True, fill="both")

    controles = _montar_controles_musica(janela)

    def limpar_container():
        for widget in container.winfo_children():
            widget.destroy()

    def mostrar_home():
        limpar_container()
        home.construir_home(
            container,
            ir_equipe=mostrar_equipe,
            ir_calculadora=mostrar_calculadora,
            ir_minigame=mostrar_minigame,
        )
        controles.lift()

    def mostrar_equipe():
        limpar_container()
        equipe.construir_equipe(container, ir_home=mostrar_home)
        controles.lift()

    def mostrar_calculadora():
        limpar_container()
        interface.construir_calculadora(
            container,
            ir_home=mostrar_home,
            funcao_soma=funcao_soma,
            funcao_subtracao=funcao_subtracao,
            funcao_multiplicacao=funcao_multiplicacao,
            funcao_divisao=funcao_divisao,
        )
        controles.lift()

    def mostrar_minigame():
        limpar_container()
        minigame.construir_jogo(container, ir_home=mostrar_home)
        controles.lift()

    mostrar_home()
