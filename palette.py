from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    """Extrai uma paleta de cores de uma imagem.

    Retorna uma lista de cores em formato hexadecimal.
    """

    if not isinstance(n_cores, int) or n_cores <= 0:
        raise ValueError("n_cores deve ser um inteiro positivo")

    img = Image.open(imagem).convert('RGB')
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)
    cores = kmeans.cluster_centers_.astype(int)

    hex_cores = []
    for cor in cores:
        r, g, b = cor
        hex_cores.append(f"#{r:02x}{g:02x}{b:02x}")

    return hex_cores

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python palette.py imagem.jpg")
    else:
        for cor in extrair_cores(sys.argv[1]):
            print(cor)
