from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import argparse

def extrair_cores(imagem, n_cores=5):
    img = Image.open(imagem).convert('RGB')
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)
    cores = kmeans.cluster_centers_.astype(int)
    for cor in cores:
        r, g, b = cor
        print(f'#{r:02x}{g:02x}{b:02x}')

def main():
    parser = argparse.ArgumentParser(
        description="Extract a color palette from an image"
    )
    parser.add_argument(
        "image",
        help="Path to the image file"
    )
    parser.add_argument(
        "n_cores",
        nargs="?",
        type=int,
        default=5,
        help="Number of colors to extract (default: 5)"
    )
    args = parser.parse_args()
    extrair_cores(args.image, args.n_cores)


if __name__ == "__main__":
    main()
