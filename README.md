# Fast Utilities

Coleção de scripts Python utilitários para tarefas do dia a dia.

## Configuração do Ambiente

### 1. Criar ambiente virtual (recomendado)

```bash
# Criar virtual environment
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

Todas as dependências necessárias, incluindo FFmpeg, serão instaladas automaticamente.

---

## Scripts Disponíveis

### zip_folder

Script para compactar pastas em arquivos ZIP.

**Uso:**
```bash
python zip_folder.py
```

O script solicitará o caminho da pasta que deseja compactar. O arquivo ZIP será salvo no diretório pai com o nome `py_compact.zip`.

**Exemplo:**
```bash
python zip_folder.py
# Digite o caminho quando solicitado: /home/user/minha_pasta
# Resultado: /home/user/py_compact.zip
```

---

### youtube_to_mp3

Script para baixar o áudio de vídeos do YouTube e salvar como MP3.

O FFmpeg é incluído automaticamente via dependências, sem necessidade de instalação manual.

**Uso:**
```bash
python youtube_to_mp3.py -u <URL> -o <DIRETORIO_DESTINO>
```

**Parâmetros:**
- `-u, --url`: URL do vídeo do YouTube (obrigatório)
- `-o, --output`: Diretório onde o arquivo MP3 será salvo (obrigatório)

**Exemplos:**
```bash
# Baixar para a pasta atual
python youtube_to_mp3.py -u "https://youtube.com/watch?v=dQw4w9WgXcQ" -o ./

# Baixar para pasta específica
python youtube_to_mp3.py -u "https://youtu.be/dQw4w9WgXcQ" -o ~/Downloads/musicas/

# O script cria automaticamente o diretório se não existir
python youtube_to_mp3.py --url "https://youtube.com/watch?v=abc123" --output ./minhas_musicas/
```

O arquivo será salvo com o título do vídeo como nome do arquivo.