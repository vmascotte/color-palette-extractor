# Color Palette Extractor

Este projeto tem como objetivo extrair uma paleta de cores dominante de uma imagem usando KMeans.

## Requisitos de ambiente

- Python 3.8 ou superior
- `pip` para instalar as dependências

### Dependências

As bibliotecas necessárias estão listadas em `requirements.txt`:

```
pillow
numpy
scikit-learn>=1.4
gradio
```

É recomendado usar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

Para extrair as cores de uma imagem, execute:

```bash
python palette.py caminho/da/imagem
```

Por exemplo, usando a imagem de exemplo fornecida (`1.PNG`):

```bash
python palette.py 1.PNG
```

### Saída determinística

Para obter os mesmos resultados em execuções subsequentes, forneça um
`random_state` para o KMeans:

```bash
python palette.py 1.PNG -r 42
python palette.py 1.PNG -r 42
```

As cores impressas serão as mesmas nas duas execuções.

O script exibirá as cores encontradas em formato hexadecimal, uma por linha.

## Interface Web

Também é possível utilizar uma interface simples no navegador para extrair a paleta de cores.
Execute:

```bash
python web_ui.py
```

O navegador padrão será aberto automaticamente, exibindo um seletor de imagem e o número de cores desejado. Após enviar a imagem, as cores extraídas aparecerão na tela.

### Atualização do programa

Se o projeto foi clonado via `git`, a interface conta com um botão **Atualizar Programa** que executa `git pull` para baixar eventuais mudanças do repositório.

## Uso simplificado no Windows

Para facilitar a execução em máquinas Windows, este repositório inclui o arquivo
`start_ui.bat`. Basta baixar o projeto, executar esse arquivo e a interface será
aberta automaticamente no navegador padrão.

O script cria um ambiente virtual (caso ainda não exista), instala as
dependências listadas em `requirements.txt` e chama `web_ui.py`. É necessário ter
o Python 3 instalado e configurado no `PATH`.

Se desejar gerar um executável independente, instale o `pyinstaller` e rode:

```bash
pyinstaller --onefile web_ui.py
```

Isso gerará `dist/web_ui.exe`, que pode ser iniciado diretamente sem o script
batch.

## Objetivo do projeto

O propósito deste repositório é demonstrar como identificar as cores predominantes de uma imagem utilizando clustering (via KMeans). 
