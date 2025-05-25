import os
import sys
import time
import tempfile
import subprocess
import platform
import shutil
from datetime import datetime

# Função para detectar o sistema operacional
def detectar_sistema_operacional():
    sistemas = {
        'Linux': 'Linux',
        'Darwin': 'macOS',
        'Windows': 'Windows'
    }
    so = platform.system()
    return sistemas.get(so, so)

# Função para imprimir o conteúdo de um arquivo
# no sistema operacional detectado
def imprimir_arquivo(caminho_arquivo):
    sistema = detectar_sistema_operacional()
    if sistema == 'Windows':
        os.startfile(caminho_arquivo, 'print')
    elif sistema == 'macOS':
        subprocess.run(['lp', caminho_arquivo])
    elif sistema == 'Linux':
        subprocess.run(['lp', caminho_arquivo])
    else:
        print(f'Sistema operacional {sistema} não suportado para impressão.')

# Função para criar um arquivo temporário com o texto
def criar_arquivo_temporario(texto, extensao='.txt'):
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nome_arquivo = f'printx_{timestamp}{extensao}'
    caminho_arquivo = os.path.join(temp_dir, nome_arquivo)
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    return caminho_arquivo

# Função principal
def main():
    if len(sys.argv) < 2:
        print('Uso: python main.py "Texto a ser impresso"')
        sys.exit(1)
    texto = sys.argv[1]
    caminho_arquivo = criar_arquivo_temporario(texto)
    print(f'Arquivo temporário criado em: {caminho_arquivo}')
    imprimir_arquivo(caminho_arquivo)
    # Aguarda um tempo antes de remover o arquivo
    time.sleep(5)
    try:
        os.remove(caminho_arquivo)
        print('Arquivo temporário removido.')
    except Exception as e:
        print(f'Erro ao remover arquivo temporário: {e}')

if __name__ == '__main__':
    main()
