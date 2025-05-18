from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    img = Image.open(imagem).convert('RGB')
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
    cores = kmeans.cluster_centers_.astype(int)
    for cor in cores:
        r, g, b = cor
        print(f'#{r:02x}{g:02x}{b:02x}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python palette.py imagem.jpg")
    else:
        extrair_cores(sys.argv[1])
