from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    img = Image.open(imagem).convert('RGB')
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)
    cores = np.clip(np.rint(kmeans.cluster_centers_), 0, 255).astype(int)
    for cor in cores:
        r, g, b = cor
        print(f'#{r:02x}{g:02x}{b:02x}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python palette.py imagem.jpg")
    else:
        extrair_cores(sys.argv[1])
