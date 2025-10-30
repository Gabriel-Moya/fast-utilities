#!/usr/bin/env python3
"""
YouTube to MP3 Downloader

This script downloads audio from YouTube videos and saves them as MP3 files.
"""

import argparse
import os
import sys


def validate_url(url):
    """Validate if the URL is a YouTube URL."""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url for domain in youtube_domains)


def get_ffmpeg_path():
    """
    Get FFmpeg directory path from static-ffmpeg.

    Returns:
        str: Path to directory containing FFmpeg binaries, or None if not available
    """
    try:
        from static_ffmpeg import run
        # Get the ffmpeg and ffprobe paths
        ffmpeg_path, ffprobe_path = run.get_or_fetch_platform_executables_else_raise()
        # Return the directory containing the executables
        return os.path.dirname(ffmpeg_path)
    except ImportError:
        print("Aviso: 'static-ffmpeg' não está instalado.")
        print("Tentando usar FFmpeg do sistema...")
        return None
    except Exception as e:
        print(f"Aviso: Erro ao obter FFmpeg: {e}")
        print("Tentando usar FFmpeg do sistema...")
        return None


def download_audio(url, output_dir):
    """
    Download audio from YouTube video and save as MP3.

    Args:
        url (str): YouTube video URL
        output_dir (str): Directory where the MP3 file will be saved

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import yt_dlp
    except ImportError:
        print("Erro: A biblioteca 'yt-dlp' não está instalada.")
        print("Por favor, instale executando: pip install -r requirements.txt")
        return False

    # Get FFmpeg path
    ffmpeg_path = get_ffmpeg_path()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Diretório criado: {output_dir}")
        except Exception as e:
            print(f"Erro ao criar diretório: {e}")
            return False

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }

    # Add FFmpeg location if available
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path
        print(f"Usando FFmpeg de: {ffmpeg_path}")

    try:
        print(f"\nBaixando áudio de: {url}")
        print(f"Destino: {output_dir}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Replace extension with mp3
            filename = os.path.splitext(filename)[0] + '.mp3'

        print(f"\n✓ Download concluído com sucesso!")
        print(f"Arquivo salvo: {filename}")
        return True

    except Exception as e:
        print(f"\nErro ao baixar o vídeo: {e}")
        return False


def main():
    """Main function to parse arguments and execute download."""
    parser = argparse.ArgumentParser(
        description='Baixa o áudio de vídeos do YouTube e salva como MP3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python youtube_to_mp3.py -u "https://youtube.com/watch?v=dQw4w9WgXcQ" -o ./musicas/
  python youtube_to_mp3.py --url "https://youtu.be/dQw4w9WgXcQ" --output ~/Downloads/
        """
    )

    parser.add_argument(
        '-u', '--url',
        required=True,
        help='URL do vídeo do YouTube'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Diretório de destino para salvar o arquivo MP3'
    )

    args = parser.parse_args()

    # Validate URL
    if not validate_url(args.url):
        print("Erro: A URL fornecida não parece ser uma URL válida do YouTube.")
        print("URLs aceitas: youtube.com, youtu.be, www.youtube.com, m.youtube.com")
        sys.exit(1)

    # Download audio
    success = download_audio(args.url, args.output)

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
