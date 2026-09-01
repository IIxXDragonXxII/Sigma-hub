# tema.py
# Paleta e tipografia compartilhadas do SIGMA HUB.

import platform

# Fundo
BG_DEEP = "#020008"
BG_SURFACE = "#0A0520"
BG_GLASS = "#110830"
BG_ELEVATED = "#1A0F3D"

# Neon / acentos
NEON_CYAN = "#00E5FF"
NEON_MAGENTA = "#FF2D95"
NEON_GOLD = "#FFD60A"
NEON_PURPLE = "#A855F7"
NEON_VIOLET = "#7C3AED"
NEON_PINK = "#F472B6"
NEON_LILAC = "#C084FC"
NEON_AURORA = "#4C1D95"

# Texto
TEXT_PRIMARY = "#F5EEFF"
TEXT_MUTED = "#9B8EC4"
TEXT_DIM = "#6B5F94"

# Botões da calculadora: (fg, hover, borda)
BTN_NUM = ("#1A1040", "#2A1860", NEON_PURPLE)
BTN_OP = ("#2D1060", "#4C1D95", NEON_GOLD)
BTN_EQ = ("#6D28D9", "#9333EA", NEON_CYAN)
BTN_CLR = ("#3B0764", "#581C87", NEON_MAGENTA)

# Tipografia por sistema
_SISTEMA = platform.system()

if _SISTEMA == "Windows":
    FONTE_TITULO = ("Segoe UI", 36, "bold")
    FONTE_SUB = ("Segoe UI", 13)
    FONTE_DISPLAY = ("Consolas", 34, "bold")
    FONTE_BOTAO = ("Segoe UI", 22, "bold")
    FONTE_HUD = ("Segoe UI", 14, "bold")
    FONTE_MONO = ("Consolas", 12, "bold")
    FONTE_CARD = ("Segoe UI", 21, "bold")
elif _SISTEMA == "Darwin":
    FONTE_TITULO = ("SF Pro Display", 36, "bold")
    FONTE_SUB = ("SF Pro Text", 13)
    FONTE_DISPLAY = ("Menlo", 34, "bold")
    FONTE_BOTAO = ("SF Pro Display", 22, "bold")
    FONTE_HUD = ("SF Pro Text", 14, "bold")
    FONTE_MONO = ("Menlo", 12, "bold")
    FONTE_CARD = ("SF Pro Display", 21, "bold")
else:
    FONTE_TITULO = ("Cantarell", 36, "bold")
    FONTE_SUB = ("Cantarell", 13)
    FONTE_DISPLAY = ("DejaVu Sans Mono", 34, "bold")
    FONTE_BOTAO = ("Cantarell", 22, "bold")
    FONTE_HUD = ("Cantarell", 14, "bold")
    FONTE_MONO = ("DejaVu Sans Mono", 12, "bold")
    FONTE_CARD = ("Cantarell", 21, "bold")

CICLO_NEON = [
    NEON_CYAN,
    NEON_MAGENTA,
    NEON_GOLD,
    NEON_PURPLE,
    NEON_PINK,
    NEON_CYAN,
]


def cor_ciclo(indice):
    """Retorna a próxima cor do ciclo neon."""
    return CICLO_NEON[indice % len(CICLO_NEON)]


def hex_para_rgb(cor):
    """Converte '#RRGGBB' em (r, g, b)."""
    texto = cor.lstrip("#")
    return tuple(int(texto[i:i + 2], 16) for i in (0, 2, 4))


def hex_para_rgba(cor, alpha):
    """Converte '#RRGGBB' em (r, g, b, a)."""
    vermelho, verde, azul = hex_para_rgb(cor)
    return (vermelho, verde, azul, int(alpha))
