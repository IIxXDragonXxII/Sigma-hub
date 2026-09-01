# main.py
# Ponto de entrada: abre o SIGMA HUB e liga a matemática à interface.

import customtkinter as ctk

import hub
import matematica
import update_checker


def iniciar():
    print("Iniciando SIGMA HUB...")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    janela = ctk.CTk()
    janela.title("SIGMA HUB")
    janela.geometry("1100x700")
    janela.minsize(820, 560)

    try:
        janela.state("zoomed")
    except Exception:
        try:
            janela.attributes("-zoomed", True)
        except Exception:
            largura = janela.winfo_screenwidth()
            altura = janela.winfo_screenheight()
            janela.geometry(f"{largura}x{altura}+0+0")

    hub.iniciar_app(
        janela,
        funcao_soma=matematica.soma,
        funcao_subtracao=matematica.subtracao,
        funcao_multiplicacao=matematica.multiplicacao,
        funcao_divisao=matematica.divisao,
    )

    has_update, msg = update_checker.run_update_check(janela)

    if has_update:
        print(msg)
        # Simple yes/no dialog using CTk
        resposta = ctk.CTkMessagebox(
            title="Atualização Disponível",
            message=msg,
            icon="question",
            option_1="Não",
            option_2="Sim",
        )
        if resposta == "Sim":
            dl_path, asset_name = update_checker.download_update()
            if dl_path:
                if update_checker.apply_update(dl_path, asset_name):
                    update_checker.save_version(msg)
                    print("Atualização aplicada com sucesso!")
                    janela.destroy()
                    iniciar()
                else:
                    print("Falha ao aplicar atualização")
            else:
                print("Falha ao baixar atualização")
    else:
        print(msg)

    janela.mainloop()


if __name__ == "__main__":
    iniciar()
