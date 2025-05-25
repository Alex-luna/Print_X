import os
import re
import time
import glob
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import imagehash
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGDisplayBounds, CGMainDisplayID, CGWindowListCreateImage, kCGWindowImageDefault
from Quartz import kCGWindowListOptionAll
from Quartz.CoreGraphics import kCGWindowImageDefault
from Cocoa import NSURL

# --- Configuração inicial ---
INTERVALO_PADRAO = 5  # segundos (pode ser alterado pelo usuário)
PADRAO_NOME = r"screenshot_(\\d{3})\\.png"


def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Selecione a pasta para salvar os screenshots")
    root.destroy()
    return pasta


def proximo_numero_arquivo(pasta):
    arquivos = glob.glob(os.path.join(pasta, "screenshot_*.png"))
    max_num = 0
    for arq in arquivos:
        m = re.search(PADRAO_NOME, os.path.basename(arq))
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    return max_num + 1


def capturar_tela(path_destino_jpg):
    # Captura a tela principal inteira
    display_id = CGMainDisplayID()
    bounds = CGDisplayBounds(display_id)
    image = CGWindowListCreateImage(bounds, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, kCGWindowImageDefault)
    if image is None:
        raise RuntimeError("Não foi possível capturar a tela.")
    # Salva como PNG temporário
    from Quartz import CGImageDestinationCreateWithURL, CGImageDestinationAddImage, CGImageDestinationFinalize
    try:
        from CoreServices import kUTTypePNG
    except ImportError:
        from UniformTypeIdentifiers import UTType
        kUTTypePNG = UTType.PNG.identifier
    from uuid import uuid4
    import shutil
    temp_png = path_destino_jpg + f"_{uuid4().hex}.png"
    url = NSURL.fileURLWithPath_(temp_png)
    dest = CGImageDestinationCreateWithURL(url, kUTTypePNG, 1, None)
    CGImageDestinationAddImage(dest, image, None)
    CGImageDestinationFinalize(dest)
    # Converte PNG para JPEG com qualidade 90
    with Image.open(temp_png) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(path_destino_jpg, 'JPEG', quality=90, optimize=True)
    os.remove(temp_png)


def hash_imagem(path):
    with Image.open(path) as img:
        return imagehash.phash(img)


def main():
    print("--- Screenshot Automático com Filtro de Duplicatas ---")
    pasta = selecionar_pasta()
    if not pasta:
        print("Nenhuma pasta selecionada. Encerrando.")
        return
    print(f"Pasta selecionada: {pasta}")
    try:
        intervalo = int(input(f"Intervalo entre capturas (segundos) [padrão: {INTERVALO_PADRAO}]: ") or INTERVALO_PADRAO)
    except Exception:
        intervalo = INTERVALO_PADRAO
    print(f"Capturando a cada {intervalo} segundos. Pressione Ctrl+C para sair.")
    num = proximo_numero_arquivo(pasta)
    hash_anterior = None
    while True:
        nome_arquivo = f"screenshot_{num:03d}.jpg"
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        try:
            capturar_tela(caminho_arquivo)
            hash_atual = hash_imagem(caminho_arquivo)
            if hash_anterior is not None and hash_atual - hash_anterior <= 2:
                os.remove(caminho_arquivo)
                print(f"Imagem {nome_arquivo} deletada (duplicada da anterior).")
            else:
                print(f"Captura realizada: {nome_arquivo}")
                hash_anterior = hash_atual
                num += 1
        except Exception as e:
            print(f"Erro ao capturar ou processar imagem: {e}")
        time.sleep(intervalo)


if __name__ == "__main__":
    main() 