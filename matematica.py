# matematica.py
# Operações da calculadora.


def soma(x, y):
    """Retorna a adição de dois números."""
    return x + y


def subtracao(x, y):
    """Retorna a diferença entre dois números."""
    return x - y


def multiplicacao(x, y):
    """Retorna a multiplicação de dois números."""
    return x * y


def divisao(x, y):
    """Retorna a divisão. Levanta ZeroDivisionError se y for zero."""
    if y == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return x / y


def formatar_resultado(valor):
    """Formata o número para o display, sem lixo de ponto flutuante."""
    if isinstance(valor, str):
        return valor

    arredondado = round(valor, 10)

    if abs(arredondado - round(arredondado)) < 1e-10:
        return str(int(round(arredondado)))

    texto = f"{arredondado:.10g}"
    return texto
