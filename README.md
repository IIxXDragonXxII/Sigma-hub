# SIGMA HUB

SIGMA HUB é um aplicativo desktop com interface neon, que reúne três módulos:

- **Equipe**: galeria de fotos com visualizador em tela cheia.
- **Calculadora**: calculadora estilo "aura" com contador de pontos e animações.
- **Mini Game**: "Aura Reflex" – clique no alvo antes que ele suma.

O projeto usa `customtkinter` para a interface e possui fundo em vídeo (opcional) e música ambiente (opcional).

---

## Como executar

### 1. Instalar as bibliotecas

Dê um duplo clique no arquivo **instalar_bibliotecas.bat**.

Ele vai:
- Verificar se o Python está instalado.
- Criar uma pasta `venv` (ambiente virtual) se ela não existir.
- Instalar todas as bibliotecas necessárias (`customtkinter`, `Pillow`, `opencv-python`, `pygame`).
- Gerar o arquivo `requirements.txt` com as versões instaladas.

O terminal vai mostrar o progresso e ficará aberto em caso de erro.

### 2. Iniciar o programa

Dê um duplo clique no arquivo **iniciar.bat**.

Ele vai:
- Verificar se a `venv` existe.
- Ativar o ambiente virtual.
- Rodar o programa principal (`main.py`).

Se a `venv` não existir, ele avisa para executar o instalador primeiro.

---

## Para que serve cada .bat

| Arquivo                  | Função |
|--------------------------|--------|
| `instalar_bibliotecas.bat` | Prepara o ambiente: cria a venv e instala todas as dependências. |
| `iniciar.bat`            | Inicia o aplicativo com a venv ativada. Mantém o terminal aberto se houver erro. |

---

## Estrutura principal
