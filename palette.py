from PIL import Image, UnidentifiedImageError
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    try:
        img = Image.open(imagem).convert('RGB')
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        print(f"Error: file '{imagem}' not found or cannot be opened.", file=sys.stderr)
        sys.exit(1)
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
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
