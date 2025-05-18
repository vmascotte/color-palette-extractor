from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys

def extrair_cores(imagem, n_cores=5):
    """Extrai uma paleta de cores dominante de uma imagem.

    Parameters
    ----------
    imagem : str
        Caminho para a imagem que terá sua paleta extraída.
    n_cores : int, optional
        Número de cores desejadas, por padrão 5.

    Returns
    -------
    None
        Apenas imprime as cores encontradas em hexadecimal na saída padrão.

    """

    # Carrega a imagem convertendo para RGB, garantindo um formato conhecido
    img = Image.open(imagem).convert('RGB')

    # Redimensiona para reduzir a quantidade de pixels analisados
    img = img.resize((200, 200))

    # Converte para um array Nx3 (R, G, B) utilizado pelo KMeans
    pixels = np.array(img).reshape(-1, 3)

    # Aplica o algoritmo de clusterização para descobrir cores dominantes
    kmeans = KMeans(n_clusters=n_cores, n_init="auto")
    kmeans.fit(pixels)

    # Obtém as cores centrais e as transforma em inteiros
    cores = kmeans.cluster_centers_.astype(int)

    # Imprime cada cor em formato hexadecimal
    for cor in cores:
        r, g, b = cor
        print(f'#{r:02x}{g:02x}{b:02x}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python palette.py imagem.jpg")
    else:
        extrair_cores(sys.argv[1])
