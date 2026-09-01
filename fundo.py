# fundo.py
# Fundo em vídeo em tela cheia (cover): preenche a área, sem bordas pretas,
# e acompanha o redimensionamento da janela. Sem efeitos de cursor.

import os
import tkinter as tk

import tema

try:
    import cv2
    from PIL import Image, ImageTk

    VIDEO_DISPONIVEL = True
except ImportError:
    VIDEO_DISPONIVEL = False
    cv2 = None
    Image = None
    ImageTk = None

PASTA_APP = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_APP, "assets")

# Coloque o vídeo em assets/fundo.mp4 (ou altere este caminho).
CAMINHO_VIDEO = os.path.join(PASTA_ASSETS, "fundo.mp4")

EXTENSOES_VIDEO = (".mp4", ".webm", ".mov", ".avi", ".mkv", ".m4v")
NOMES_VIDEO = ("fundo", "background", "bg", "video")


def _localizar_video(caminho_explicito=None):
    """Encontra o arquivo de vídeo do fundo."""
    candidatos = []

    if caminho_explicito:
        candidatos.append(caminho_explicito)
    candidatos.append(CAMINHO_VIDEO)

    pastas = (
        PASTA_ASSETS,
        os.path.join(PASTA_ASSETS, "video"),
        PASTA_APP,
    )

    for pasta in pastas:
        if not os.path.isdir(pasta):
            continue
        for nome in NOMES_VIDEO:
            for ext in EXTENSOES_VIDEO:
                candidatos.append(os.path.join(pasta, nome + ext))

    vistos = set()
    for caminho in candidatos:
        caminho = os.path.abspath(caminho)
        if caminho in vistos:
            continue
        vistos.add(caminho)
        if os.path.isfile(caminho):
            return caminho

    for pasta in pastas:
        if not os.path.isdir(pasta):
            continue
        try:
            arquivos = sorted(os.listdir(pasta))
        except OSError:
            continue
        for arquivo in arquivos:
            if os.path.splitext(arquivo)[1].lower() in EXTENSOES_VIDEO:
                return os.path.join(pasta, arquivo)

    return None


def _preencher_cover(frame_bgr, largura, altura):
    """Redimensiona o frame no modo cover: preenche tudo, recorta o excedente."""
    largura = max(int(largura), 1)
    altura = max(int(altura), 1)
    origem_h, origem_w = frame_bgr.shape[:2]
    if origem_w < 1 or origem_h < 1:
        return None

    escala = max(largura / origem_w, altura / origem_h)
    novo_w = max(int(origem_w * escala + 0.5), 1)
    novo_h = max(int(origem_h * escala + 0.5), 1)

    interpolacao = cv2.INTER_AREA if escala < 1 else cv2.INTER_LINEAR
    redimensionado = cv2.resize(frame_bgr, (novo_w, novo_h), interpolation=interpolacao)

    x = max((novo_w - largura) // 2, 0)
    y = max((novo_h - altura) // 2, 0)
    recorte = redimensionado[y:y + altura, x:x + largura]

    if recorte.shape[1] != largura or recorte.shape[0] != altura:
        recorte = cv2.resize(recorte, (largura, altura), interpolation=cv2.INTER_LINEAR)

    return recorte


def criar_fundo_interativo(
    pai,
    cor_fundo=tema.BG_DEEP,
    quantidade_particulas=55,
    caminho_video=None,
):
    """Cria o fundo em vídeo. Devolve o canvas para a interface continuar por cima.

    quantidade_particulas existe só para não quebrar chamadas antigas.
    """
    del quantidade_particulas

    canvas = tk.Canvas(pai, bg=cor_fundo, highlightthickness=0, bd=0, cursor="")
    canvas.pack(expand=True, fill="both")
    canvas.pack_propagate(False)

    id_video = canvas.create_image(0, 0, anchor="nw", tags=("video_fundo",))
    canvas.tag_lower("video_fundo")

    estado = {
        "cap": None,
        "foto": None,
        "frame": None,
        "executando": True,
        "job": None,
        "tamanho": (0, 0),
        "atraso_ms": 33,
    }

    def encerrar(_evento=None):
        estado["executando"] = False
        job = estado["job"]
        if job is not None:
            try:
                canvas.after_cancel(job)
            except Exception:
                pass
            estado["job"] = None

        cap = estado["cap"]
        if cap is not None:
            cap.release()
            estado["cap"] = None

        estado["foto"] = None
        estado["frame"] = None

    def mostrar_frame(frame_bgr, largura, altura):
        coberto = _preencher_cover(frame_bgr, largura, altura)
        if coberto is None:
            return

        rgb = cv2.cvtColor(coberto, cv2.COLOR_BGR2RGB)
        imagem = Image.fromarray(rgb)
        foto = ImageTk.PhotoImage(image=imagem)

        estado["foto"] = foto
        canvas.itemconfigure(id_video, image=foto)
        canvas.coords(id_video, 0, 0)
        canvas.tag_lower("video_fundo")

    def redesenhar_atual():
        if not estado["executando"]:
            return
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        largura = max(canvas.winfo_width(), 1)
        altura = max(canvas.winfo_height(), 1)
        estado["tamanho"] = (largura, altura)

        if estado["frame"] is not None:
            mostrar_frame(estado["frame"], largura, altura)

    def ler_proximo_frame():
        cap = estado["cap"]
        if cap is None:
            return None

        ok, frame = cap.read()
        if not ok or frame is None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = cap.read()
            if not ok or frame is None:
                return None
        return frame

    def animar():
        if not estado["executando"]:
            return
        try:
            if not canvas.winfo_exists():
                encerrar()
                return
        except Exception:
            encerrar()
            return

        largura = max(canvas.winfo_width(), 1)
        altura = max(canvas.winfo_height(), 1)

        if largura > 2 and altura > 2:
            frame = ler_proximo_frame()
            if frame is not None:
                estado["frame"] = frame
                mostrar_frame(frame, largura, altura)
            estado["tamanho"] = (largura, altura)

        estado["job"] = canvas.after(estado["atraso_ms"], animar)

    def ao_redimensionar(_evento=None):
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return

        largura = max(canvas.winfo_width(), 1)
        altura = max(canvas.winfo_height(), 1)
        if (largura, altura) == estado["tamanho"]:
            return
        redesenhar_atual()

    caminho = _localizar_video(caminho_video)

    if VIDEO_DISPONIVEL and caminho:
        cap = cv2.VideoCapture(caminho)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            if fps <= 1:
                fps = 30
            estado["atraso_ms"] = max(int(1000 / fps), 8)
            estado["cap"] = cap
        else:
            cap.release()
            print(f"Não foi possível abrir o vídeo de fundo: {caminho}")
    elif not VIDEO_DISPONIVEL:
        print("Instale opencv-python e Pillow para o fundo em vídeo.")
        print("    pip install opencv-python pillow")
    else:
        print("Nenhum vídeo de fundo encontrado.")
        print(f"Coloque um arquivo em: {CAMINHO_VIDEO}")

    canvas.bind("<Configure>", ao_redimensionar, add="+")
    canvas.bind("<Destroy>", encerrar, add="+")

    if estado["cap"] is not None:
        canvas.after(16, animar)

    return canvas
