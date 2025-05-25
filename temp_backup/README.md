# Screenshot Automático com Filtro de Duplicatas (macOS)

## Descrição

Este aplicativo Python para macOS realiza capturas de tela automáticas em intervalos configuráveis, salva as imagens em uma pasta escolhida pelo usuário e remove capturas duplicadas automaticamente.

## Funcionalidades
- Captura de tela inteira do Mac a cada X segundos.
- Seleção da pasta de destino via caixa de diálogo nativa.
- Numeração sequencial dos arquivos (`screenshot_001.png`, ...).
- Detecção e exclusão automática de capturas duplicadas (hash perceptual).
- Logs simples no terminal.

## Requisitos
- macOS
- Python 3.8+

## Instalação

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o script principal:
   ```bash
   python main.py
   ```
2. Escolha a pasta onde deseja salvar as capturas.
3. O programa rodará até ser encerrado manualmente (Ctrl+C).

## Observações
- O programa pode solicitar permissões de "Gravação de Tela" na primeira execução.
- Para empacotar como `.app`, consulte ferramentas como `py2app` ou `briefcase`.

## Licença
MIT
