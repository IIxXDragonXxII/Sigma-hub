# imagens.py
# Imagens da interface: ícones quadrados, painel da galeria e logo circular.

import os

from PIL import Image, ImageDraw, ImageTk

import tema

PASTA_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Troque este arquivo (ou coloque logo.jpg / logo.webp) para mudar o avatar.
CAMINHO_LOGO = os.path.join(PASTA_ASSETS, "logo.png")
NOMES_LOGO = ("logo", "avatar", "perfil", "icone")
EXTENSOES_LOGO = (".png", ".jpg", ".jpeg", ".webp")


def localizar_logo(caminho_explicito=None):
    """Encontra a imagem do logo/avatar. Altere CAMINHO_LOGO para trocar fácil."""
    candidatos = []
    if caminho_explicito:
        candidatos.append(caminho_explicito)
    candidatos.append(CAMINHO_LOGO)

    for nome in NOMES_LOGO:
        for ext in EXTENSOES_LOGO:
            candidatos.append(os.path.join(PASTA_ASSETS, nome + ext))
            candidatos.append(os.path.join(PASTA_ASSETS, "logo", nome + ext))

    vistos = set()
    for caminho in candidatos:
        caminho = os.path.abspath(caminho)
        if caminho in vistos:
            continue
        vistos.add(caminho)
        if os.path.isfile(caminho):
            return caminho
    return None


def _cobrir_quadrado(imagem, tamanho):
    """Recorta no centro e redimensiona para um quadrado."""
    imagem = imagem.convert("RGBA")
    largura, altura = imagem.size
    lado = min(largura, altura)
    esquerda = (largura - lado) // 2
    topo = (altura - lado) // 2
    quadrado = imagem.crop((esquerda, topo, esquerda + lado, topo + lado))
    return quadrado.resize((tamanho, tamanho), Image.Resampling.LANCZOS)


def criar_logo_circular(
    tamanho,
    caminho=None,
    cor_fundo=tema.BG_GLASS,
    cor_borda=tema.NEON_CYAN,
    espessura_borda=3,
):
    """Cria um PhotoImage circular (RGBA). Os cantos ficam transparentes, sem quadrado preto."""
    tamanho = max(int(tamanho), 16)
    canvas_img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))

    mascara = Image.new("L", (tamanho, tamanho), 0)
    ImageDraw.Draw(mascara).ellipse((1, 1, tamanho - 2, tamanho - 2), fill=255)

    arquivo = localizar_logo(caminho)
    if arquivo:
        with Image.open(arquivo) as original:
            foto = _cobrir_quadrado(original, tamanho)
        foto.putalpha(mascara)
        canvas_img.paste(foto, (0, 0), foto)
    else:
        preenchido = Image.new("RGBA", (tamanho, tamanho), tema.hex_para_rgba(cor_fundo, 255))
        preenchido.putalpha(mascara)
        canvas_img.paste(preenchido, (0, 0), preenchido)

    desenho = ImageDraw.Draw(canvas_img)
    margem = max(espessura_borda // 2, 1)
    desenho.ellipse(
        (margem, margem, tamanho - 1 - margem, tamanho - 1 - margem),
        outline=tema.hex_para_rgba(cor_borda, 255),
        width=espessura_borda,
    )
    return ImageTk.PhotoImage(canvas_img)


def painel_translucido(largura, altura, alpha=118, raio=0):
    """Painel quadrado semitransparente da galeria (o vídeo aparece através)."""
    del raio
    largura = max(int(largura), 8)
    altura = max(int(altura), 8)
    imagem = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(imagem)
    preenchimento = tema.hex_para_rgba(tema.BG_GLASS, alpha)
    borda = tema.hex_para_rgba(tema.NEON_VIOLET, 200)
    caixa = (1, 1, largura - 2, altura - 2)
    desenho.rectangle(caixa, fill=preenchimento, outline=borda, width=2)
    return ImageTk.PhotoImage(imagem)
