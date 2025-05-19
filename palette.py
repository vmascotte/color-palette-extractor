#!/usr/bin/env python3
from PIL import Image, UnidentifiedImageError, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import sys


def extrair_cores_percentual(imagem, n_cores=5, random_state=None):
    """Extrai as cores dominantes e o percentual de ocorrência de cada uma.

    Parameters
    ----------
    imagem : str
        Caminho da imagem.
    n_cores : int, optional
        Quantidade de cores desejada.
    random_state : int | None, optional
        Valor para o random_state do KMeans.

    Returns
    -------
    tuple[list[str], np.ndarray]
        Lista de cores em hexadecimal e vetor com as frações correspondentes.

    Raises
    ------
    FileNotFoundError
        Se o arquivo da imagem não existir.
    ValueError
        Se o arquivo não puder ser aberto como imagem ou se ``n_cores`` for menor que 1.
    """

    try:
        img = Image.open(imagem).convert("RGB")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo '{imagem}' não encontrado.") from e
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError(f"Arquivo '{imagem}' não pôde ser aberto como imagem.") from e

    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)

    if n_cores < 1:
        raise ValueError("Número de cores deve ser no mínimo 1.")

    n_cores_max = len(np.unique(pixels, axis=0))
    if n_cores > n_cores_max:
        print(
            f"Número de cores solicitado ({n_cores}) excede o máximo possível ({n_cores_max}). "
            f"Ajustando para {n_cores_max}."
        )
        n_cores = n_cores_max

    kmeans = KMeans(n_clusters=n_cores, n_init="auto", random_state=random_state)
    kmeans.fit(pixels)

    cores = np.clip(np.rint(kmeans.cluster_centers_), 0, 255).astype(int)
    hex_cores = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in cores]

    counts = np.bincount(kmeans.labels_, minlength=n_cores)
    porcentagens = counts / len(pixels)

    return hex_cores, porcentagens

def extrair_cores(imagem, n_cores=5, random_state=None):
    """Mantém compatibilidade e retorna apenas as cores.

    Este método propaga as exceções levantadas por
    :func:`extrair_cores_percentual`.
    """
    hex_cores, _ = extrair_cores_percentual(imagem, n_cores, random_state)
    return hex_cores


def save_palette(img_path, hexes):
    """Gera uma imagem PNG com blocos coloridos da paleta.

    Parameters
    ----------
    img_path : str
        Caminho do arquivo PNG a ser salvo.
    hexes : list[str]
        Lista de cores em formato hexadecimal (#rrggbb).

    Raises
    ------
    ValueError
        Se ``hexes`` estiver vazio.
    """

    if not hexes:
        raise ValueError("Lista de cores vazia.")

    block_size = 50
    width = block_size * len(hexes)
    height = block_size
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    for idx, color in enumerate(hexes):
        x0 = idx * block_size
        draw.rectangle([x0, 0, x0 + block_size, height], fill=color)
    img.save(img_path, format="PNG")


def overlay_palette_on_image(img_path, hexes, position="bottom_right"):
    """Sobrep\u00f5e a paleta sobre a imagem de entrada.

    Parameters
    ----------
    img_path : str
        Caminho da imagem base.
    hexes : list[str]
        Lista de cores em formato hexadecimal.
    position : str, optional
        Posi\u00e7\u00e3o da paleta (``top_left``, ``top_right``, ``bottom_left``,
        ``bottom_right`` ou ``center``).

    Returns
    -------
    PIL.Image.Image
        Imagem resultante com a paleta sobreposta.
    """

    if not hexes:
        raise ValueError("Lista de cores vazia.")

    base = Image.open(img_path).convert("RGB")
    block_size = 50
    width = block_size * len(hexes)
    height = block_size
    pal_img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(pal_img)
    for idx, color in enumerate(hexes):
        x0 = idx * block_size
        draw.rectangle([x0, 0, x0 + block_size, height], fill=color)

    bw, bh = base.size
    positions = {
        "top_left": (0, 0),
        "top_right": (bw - width, 0),
        "bottom_left": (0, bh - height),
        "bottom_right": (bw - width, bh - height),
        "center": ((bw - width) // 2, (bh - height) // 2),
    }
    x, y = positions.get(position, positions["bottom_right"])

    base.paste(pal_img, (x, y))
    return base


def plot_pie_chart(hexes, porcentagens):
    """Exibe um gráfico de pizza com as porcentagens das cores."""
    fig, ax = plt.subplots()
    labels = [f"{p*100:.1f}%" for p in porcentagens]
    ax.pie(porcentagens, colors=hexes, labels=labels, startangle=90)
    ax.axis("equal")
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extrai as cores dominantes de uma imagem.'
    )
    parser.add_argument('imagem', help='Caminho da imagem.')
    parser.add_argument(
        '-n', '--num-cores', type=int, default=5,
        help='N\u00famero de cores desejado.'
    )
    parser.add_argument(
        '-r', '--random-state', type=int, default=None,
        help='Valor para o random_state do KMeans.'
    )
    parser.add_argument(
        '--grafico', action='store_true',
        help='Exibe gráfico de pizza com a porcentagem de cada cor.'
    )
    args = parser.parse_args()

    try:
        hexes, porcentagens = extrair_cores_percentual(
            args.imagem, args.num_cores, args.random_state
        )
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    for cor in hexes:
        print(cor)
    if args.grafico:
        plot_pie_chart(hexes, porcentagens)
