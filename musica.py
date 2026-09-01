# musica.py
# Música de fundo da aplicação: continua entre as telas, com mudo e volume.
# Detecta o sistema operacional e ajusta a inicialização do áudio para cada um.
import os
import platform

try:
    import pygame
    PYGAME_OK = True
except ImportError:
    pygame = None
    PYGAME_OK = False

PASTA_APP = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_APP, "assets")
CAMINHO_MUSICA = os.path.join(PASTA_ASSETS, "musica.mp3")
EXTENSOES = (".mp3", ".wav", ".ogg", ".flac", ".m4a")
NOMES = ("musica", "music", "soundtrack", "fundo", "bgm")

SISTEMA = platform.system()  # "Windows", "Linux", "Darwin" (macOS)

_estado = {
    "pronto": False,
    "mudo": False,
    "volume": 0.45,
    "caminho": None,
}


def _dica_instalacao_pygame():
    if SISTEMA == "Windows":
        return "pip install pygame"
    if SISTEMA == "Darwin":
        return "pip install pygame  (se falhar, instale antes: brew install sdl2 sdl2_mixer)"
    # Linux
    return (
        "pip install pygame --break-system-packages\n"
        "Se der erro de áudio, instale as libs do sistema, por ex. no Arch:\n"
        "  sudo pacman -S sdl2 sdl2_mixer"
    )


def _parametros_mixer():
    """Parâmetros de pre_init ajustados por sistema, para reduzir problemas comuns
    de latência/driver em cada plataforma."""
    frequencia = 44100
    tamanho = -16  # 16 bits, assinado
    canais = 2

    if SISTEMA == "Windows":
        # driver padrão (directsound/wasapi) lida bem com buffer menor
        buffer = 512
    elif SISTEMA == "Darwin":
        # CoreAudio também é tranquilo com buffer pequeno
        buffer = 512
    else:
        # Linux (ALSA/PulseAudio/Pipewire) costuma se beneficiar de um buffer
        # um pouco maior para evitar cortes/estalos
        buffer = 1024

    return frequencia, tamanho, canais, buffer


def _localizar_musica(caminho_explicito=None):
    candidatos = []
    if caminho_explicito:
        candidatos.append(caminho_explicito)
    candidatos.append(CAMINHO_MUSICA)
    pastas = (
        PASTA_ASSETS,
        os.path.join(PASTA_ASSETS, "audio"),
        os.path.join(PASTA_ASSETS, "musica"),
        PASTA_APP,
    )
    for pasta in pastas:
        if not os.path.isdir(pasta):
            continue
        for nome in NOMES:
            for ext in EXTENSOES:
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
            if os.path.splitext(arquivo)[1].lower() in EXTENSOES:
                return os.path.join(pasta, arquivo)
    return None


def _inicializar_mixer():
    """Inicializa o mixer com parâmetros ajustados ao sistema operacional.
    Se falhar, tenta de novo com as configurações padrão do pygame."""
    frequencia, tamanho, canais, buffer = _parametros_mixer()
    try:
        pygame.mixer.pre_init(frequencia, tamanho, canais, buffer)
        pygame.mixer.init()
        return True
    except Exception as erro:
        print(f"[{SISTEMA}] Falha ao iniciar mixer com parâmetros customizados: {erro}")
        print("Tentando novamente com configuração padrão...")
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        try:
            pygame.mixer.init()
            return True
        except Exception as erro2:
            print(f"[{SISTEMA}] Falha ao iniciar mixer: {erro2}")
            return False


def _carregar_com_fallback(caminho):
    """Tenta carregar o arquivo indicado; no Linux, se for MP3 e falhar
    (SDL2_mixer às vezes é compilado sem suporte a MP3), procura um
    arquivo alternativo em OGG/WAV na mesma pasta."""
    try:
        pygame.mixer.music.load(caminho)
        return caminho
    except Exception as erro:
        print(f"Não foi possível carregar '{caminho}': {erro}")
        if SISTEMA == "Linux" and caminho.lower().endswith(".mp3"):
            pasta = os.path.dirname(caminho)
            base = os.path.splitext(os.path.basename(caminho))[0]
            for ext in (".ogg", ".wav", ".flac"):
                alternativa = os.path.join(pasta, base + ext)
                if os.path.isfile(alternativa):
                    print(f"Tentando alternativa: {alternativa}")
                    try:
                        pygame.mixer.music.load(alternativa)
                        return alternativa
                    except Exception as erro2:
                        print(f"Também falhou: {erro2}")
        return None


def iniciar(caminho_explicito=None):
    """Começa a música uma única vez, em loop. Não reinicia ao trocar de tela."""
    if _estado["pronto"]:
        return _estado["pronto"]
    if not PYGAME_OK:
        print(f"Instale pygame para a música de fundo:\n{_dica_instalacao_pygame()}")
        return False

    caminho = _localizar_musica(caminho_explicito)
    if caminho is None:
        print("Nenhuma música encontrada.")
        print(f"Coloque um arquivo em: {CAMINHO_MUSICA}")
        return False

    if not _inicializar_mixer():
        return False

    caminho_carregado = _carregar_com_fallback(caminho)
    if caminho_carregado is None:
        return False

    try:
        pygame.mixer.music.set_volume(_estado["volume"])
        pygame.mixer.music.play(loops=-1)
        _estado["caminho"] = caminho_carregado
        _estado["pronto"] = True
        _estado["mudo"] = False
        return True
    except Exception as erro:
        print(f"Não foi possível iniciar a música: {erro}")
        return False


def esta_mudo():
    return _estado["mudo"]


def volume_atual():
    return _estado["volume"]


def esta_pronta():
    return _estado["pronto"]


def sistema_atual():
    return SISTEMA


def alternar_mudo():
    """Muta/desmuta sem reiniciar. Ao desmutar, continua de onde parou."""
    if not _estado["pronto"]:
        return _estado["mudo"]
    _estado["mudo"] = not _estado["mudo"]
    if _estado["mudo"]:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        pygame.mixer.music.set_volume(_estado["volume"])
    return _estado["mudo"]


def definir_volume(valor):
    """Define o volume entre 0.0 e 1.0. Com mudo ativo, só guarda o valor."""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return _estado["volume"]
    _estado["volume"] = max(0.0, min(1.0, valor))
    if _estado["pronto"] and not _estado["mudo"]:
        pygame.mixer.music.set_volume(_estado["volume"])
    return _estado["volume"]