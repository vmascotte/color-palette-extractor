from PIL import Image, UnidentifiedImageError
import numpy as np
from sklearn.cluster import KMeans
import argparse
import sys

def extrair_cores(imagem, n_cores=5):
    try:
        img = Image.open(imagem).convert('RGB')
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        print(f"Error: file '{imagem}' not found or cannot be opened.", file=sys.stderr)
        sys.exit(1)
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    n_cores_max = len(np.unique(pixels, axis=0))
    if n_cores > n_cores_max:
        print(
            f"Número de cores solicitado ({n_cores}) excede o máximo possível ({n_cores_max}). "
            f"Ajustando para {n_cores_max}."
        )
        n_cores = n_cores_max
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)
    cores = np.clip(np.rint(kmeans.cluster_centers_), 0, 255).astype(int)
    for cor in cores:
        r, g, b = cor
        print(f'#{r:02x}{g:02x}{b:02x}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extrai as cores dominantes de uma imagem.'
    )
    parser.add_argument('imagem', help='Caminho da imagem.')
    parser.add_argument(
        '-n', '--num-cores', type=int, default=5,
        help='N\u00famero de cores desejado.'
    )
    args = parser.parse_args()

    extrair_cores(args.imagem, args.num_cores)
