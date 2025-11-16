#!/usr/bin/env python3
"""
YouTube Playlist to MP3 Downloader

This script downloads all videos from a YouTube playlist and converts them to MP3 files.
"""

import argparse
import os
import sys


def validate_url(url):
    """Validate if the URL is a YouTube URL."""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url for domain in youtube_domains)


def validate_playlist_url(url):
    """Validate if the URL is a YouTube playlist URL."""
    return 'playlist' in url or 'list=' in url


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


def download_playlist(url, output_dir):
    """
    Download all videos from a YouTube playlist and convert to MP3.

    Args:
        url (str): YouTube playlist URL
        output_dir (str): Directory where the MP3 files will be saved

    Returns:
        tuple: (total_videos, successful_downloads, failed_downloads)
    """
    try:
        import yt_dlp
    except ImportError:
        print("Erro: A biblioteca 'yt-dlp' não está instalada.")
        print("Por favor, instale executando: pip install -r requirements.txt")
        return 0, 0, 0

    # Get FFmpeg path
    ffmpeg_path = get_ffmpeg_path()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Diretório criado: {output_dir}")
        except Exception as e:
            print(f"Erro ao criar diretório: {e}")
            return 0, 0, 0

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(playlist_index)s - %(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,  # Continue on download errors
        'extract_flat': False,
    }

    # Add FFmpeg location if available
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path
        print(f"Usando FFmpeg de: {ffmpeg_path}\n")

    successful = 0
    failed = 0
    total = 0

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First, extract playlist info without downloading
            print("Extraindo informações da playlist...")
            playlist_info = ydl.extract_info(url, download=False)

            if 'entries' not in playlist_info:
                print("Erro: Não foi possível encontrar vídeos na playlist.")
                return 0, 0, 0

            # Filter out None entries (private/deleted videos)
            entries = [e for e in playlist_info['entries'] if e is not None]
            total = len(entries)

            playlist_title = playlist_info.get('title', 'Playlist')
            print(f"\nPlaylist: {playlist_title}")
            print(f"Total de vídeos: {total}")
            print(f"Destino: {output_dir}")
            print("=" * 60)

            # Now download each video
            for index, entry in enumerate(entries, 1):
                video_title = entry.get('title', 'Unknown')
                video_url = entry.get('url', entry.get('webpage_url', ''))

                print(f"\n[{index}/{total}] Baixando: {video_title}")
                print("-" * 60)

                try:
                    ydl.download([video_url])
                    successful += 1
                    print(f"✓ Concluído: {video_title}")
                except Exception as e:
                    failed += 1
                    print(f"✗ Erro ao baixar '{video_title}': {e}")

    except Exception as e:
        print(f"\nErro ao processar playlist: {e}")
        return total, successful, failed

    return total, successful, failed


def main():
    """Main function to parse arguments and execute playlist download."""
    parser = argparse.ArgumentParser(
        description='Baixa todos os áudios de uma playlist do YouTube e salva como MP3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python youtube_playlist_to_mp3.py -u "https://youtube.com/playlist?list=..." -o ./playlists/
  python youtube_playlist_to_mp3.py --url "https://youtube.com/playlist?list=..." --output ~/Music/
        """
    )

    parser.add_argument(
        '-u', '--url',
        required=True,
        help='URL da playlist do YouTube'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Diretório de destino para salvar os arquivos MP3'
    )

    args = parser.parse_args()

    # Validate URL
    if not validate_url(args.url):
        print("Erro: A URL fornecida não parece ser uma URL válida do YouTube.")
        print("URLs aceitas: youtube.com, youtu.be, www.youtube.com, m.youtube.com")
        sys.exit(1)

    if not validate_playlist_url(args.url):
        print("Erro: A URL fornecida não parece ser uma playlist do YouTube.")
        print("URLs de playlist devem conter 'playlist' ou 'list=' no endereço.")
        print("\nDica: Para baixar vídeos individuais, use youtube_to_mp3.py")
        sys.exit(1)

    # Download playlist
    print("Iniciando download da playlist...")
    print("=" * 60)

    total, successful, failed = download_playlist(args.url, args.output)

    # Print summary
    print("\n" + "=" * 60)
    print("RESUMO DO DOWNLOAD")
    print("=" * 60)
    print(f"Total de vídeos na playlist: {total}")
    print(f"✓ Downloads bem-sucedidos: {successful}")
    print(f"✗ Falhas: {failed}")
    print("=" * 60)

    if failed > 0:
        print("\nAlguns vídeos falharam. Possíveis motivos:")
        print("- Vídeos privados ou removidos")
        print("- Restrições de região")
        print("- Problemas de conexão")

    if successful == 0:
        print("\nNenhum vídeo foi baixado com sucesso.")
        sys.exit(1)
    elif failed > 0:
        print(f"\nDownload parcialmente concluído. {successful} de {total} vídeos baixados.")
        sys.exit(0)
    else:
        print("\n✓ Todos os vídeos foram baixados com sucesso!")
        sys.exit(0)


if __name__ == '__main__':
    main()
