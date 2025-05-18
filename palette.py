from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    try:
        img = Image.open(imagem).convert("RGB")
    except Exception as e:  # noqa: BLE001
        print(f"Erro ao abrir a imagem '{imagem}': {e}")
        return False

    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)
    cores = kmeans.cluster_centers_.astype(int)
    for cor in cores:
        r, g, b = cor
        print(f"#{r:02x}{g:02x}{b:02x}")

    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python palette.py imagem.jpg")
    else:
        if not extrair_cores(sys.argv[1]):
            sys.exit(1)
