#  SIGMA HUB

![SIGMA HUB Banner](https://img.shields.io/badge/SIGMA%20HUB-1.0.0-orange?style=for-the-badge)

**Aplicativo desktop moderno com interface neon, reunindo três módulos em um só lugar:**

-  **Equipe**: Galeria de fotos com molduras e visualizador em tela cheia
-  **Calculadora**: Calculadora estilo "aura" com contador de pontos e animações neon
-  **Mini Game**: "Aura Reflex" - teste seus reflexos clicando no alvo antes que ele suma

---

##  Como Executar

### 1. Instalar Bibliotecas

**Windows**: Dê duplo clique em `instalar_bibliotecas.bat`

**Linux/Mac**: Execute `./instalar_bibliotecas.sh`

Ele vai:
- ✅ Verificar se o Python está instalado
- ✅ Criar uma pasta `venv` (ambiente virtual) se não existir
- ✅ Instalar todas as bibliotecas necessárias (`customtkinter`, `Pillow`, `opencv-python`, `pygame`)
- ✅ Gerar o arquivo `requirements.txt` com as versões instaladas

>  *Se der algum erro, execute como administrador ou verifique se o Python3 está no PATH*

### 2. Iniciar o Programa

**Windows**: Dê duplo clique em `iniciar.bat`

**Linux/Mac**: Execute `./iniciar.sh`

Ele vai:
- ✅ Verificar se a `venv` existe
- ✅ Ativar o ambiente virtual
- ✅ Rodar o programa principal (`main.py`)

>  *Se a `venv` não existir, execute o instalador primeiro*

---

##  Para que serve cada arquivo

| Arquivo | Função |
|---------|--------|
| `instalar_bibliotecas.bat/.sh` | Prepara o ambiente: cria a venv e instala todas as dependências |
| `iniciar.bat/.sh` | Inicia o aplicativo com a venv ativada. Mantém o terminal aberto se houver erro |
| `main.py` | Ponto de entrada do SIGMA HUB |
| `assets/` | Pasta com todas as imagens, ícones, música e vídeos |

---

##  Recursos

### Interface 
- Tema neon escuro com cores personalizáveis
- Animações suaves em todos os componentes
- Efeito vidro fosco (glass effect) em cards e painéis
- Fontes variadas por sistema operacional (Windows, macOS, Linux)

### Módulos 

**Equipe**
- Galeria de fotos com hover effects
- Visualizador em tela cheia
- Animação de expansão ao passar o mouse

**Calculadora**
- Contador de "Aura" integrado
- Efeitos de pulsação e flash ao clicar
- Animação de barras neon ao redor
- Teclado físico com atalhos

**Mini Game** "Aura Reflex"
- Temporizador de 30 segundos
- Alvos que aparecem e desaparecem aleatoriamente
- Sistema de pontos (acertos dão +2, erros dão -1)
- Ranking online compartilhado
- Salvamento de nome ao final da partida

### Áudio 
- Música de fundo contínua entre telas
- Controle de volume global
- Botão mudo/desmudo
- Sistema de fallback para diferentes formatos de áudio

### Atualização Automática 
- Verifica GitHub toda vez que o app é aberto
- Detecta se há nova versão do código
- Detecta alterações nos arquivos de assets (imagens)
- Permite download e instalação automática
- Versionamento via `version.txt`

---

## Tecnologias Utilizadas

- `customtkinter` - Interface moderna e responsiva
- `Pillow` - Manipulação de imagens
- `opencv-python` - Fundo em vídeo
- `pygame` - Sistema de áudio
- `customtkinter` - Theme system neon
- HTTP requests - Comunicação com API de ranking

---

##  Estrutura do Projeto

```
SIGMA HUB/
├── main.py              # Ponto de entrada
├── hub.py               # Navegação entre telas
├── home.py              # Tela inicial
├── equipe.py            # Galeria da equipe
├── calculadora/         # Módulo calculadora
├── minigame/            # Módulo mini game
├── assets/              # Imagens, ícones, áudio, vídeo
├── venv/                # Ambiente virtual (gerado automaticamente)
├── requirements.txt     # Dependências Python
├── instalar_bibliotecas.*  # Scripts de instalação
└── iniciar.*            # Scripts de início
```

---

##  Personalização

### Para mudar o logo/avatar:
1. Coloque sua imagem em `assets/logo.png` (ou `logo.jpg`, `logo.webp`)
2. Os nomes suportados: `logo`, `avatar`, `perfil`, `icone`

### Para adicionar novas fotos da equipe:
1. Coloque imagens em `assets/equipe/` com extensão `.jpg`, `.jpeg`, `.png` ou `.webp`
2. As imagens serão automaticamente redimensionadas e molduradas

### Para mudar a música de fundo:
1. Coloque seu arquivo em `assets/musica.mp3` (ou `.wav`, `.ogg`, `.flac`)
2. Suporta: `.mp3`, `.wav`, `.ogg`, `.flac`, `.m4a`
3. Nomes alternativos: `music`, `soundtrack`, `fundo`, `bgm`

### Para atualizar o visual:
1. Modifique as cores em `tema.py`
2. As fontes são detectadas automaticamente pelo sistema operacional

---

##  Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

##  Equipe

Desenvolvido por **Kaua Development** com ❤️ para a comunidade SIGMA.

---

##  Contato

- GitHub: [kaua/Sigma-Hub](https://github.com/IIxXDragonXxII/Sigma-hub/)
- Issues: Use o GitHub Issues para reportar bugs ou sugerir features

---

**⭐ Se gostou do projeto, dê uma estrela no GitHub!**
