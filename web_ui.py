#!/usr/bin/env python3
import gradio as gr
from palette import extrair_cores_percentual, save_palette, overlay_palette_on_image
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import subprocess
import os
import json

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

FAVORITES_FILE = "favorites.json"


def find_git_root(start_path: str) -> str | None:
    """Retorna o caminho do repositório Git mais próximo ou ``None``."""
    path = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(path, ".git")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def carregar_favoritos():
    if os.path.isfile(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception:
            return []
    return []


def salvar_favoritos(favoritos):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as fp:
        json.dump(favoritos, fp, ensure_ascii=False, indent=2)


def gerar_html_favoritos():
    favoritos = carregar_favoritos()
    if not favoritos:
        return "Nenhuma paleta favoritada."
    partes = []
    for fav in favoritos:
        blocos = "".join(
            f"<div style='width:20px;height:20px;background:{c};display:inline-block;margin-right:2px'></div>"
            for c in fav.get("cores", [])
        )
        cores = " ".join(fav.get("cores", []))
        partes.append(f"<div><b>{fav.get('nome')}</b>: {blocos} <code>{cores}</code></div>")
    return "<br>".join(partes)


def lista_nomes_favoritos():
    """Retorna somente os nomes das paletas favoritadas."""
    return [fav.get("nome") for fav in carregar_favoritos()]


def montar_paleta_html_grafico(cores, porcentagens):
    """Gera o HTML e o grafico da paleta."""
    blocos = "".join(
        f"<div style='width:40px;height:40px;background:{c};'></div>" for c in cores
    )
    html = (
        f"<div style='display:flex;gap:2px;'>{blocos}</div><pre>\n"
        + "\n".join(cores)
        + "</pre>"
    )

    fig, ax = plt.subplots()
    labels = [f"{p*100:.1f}%" for p in porcentagens]
    ax.pie(porcentagens, colors=cores, labels=labels, startangle=90)
    ax.axis("equal")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    grafico = Image.open(buf)
    return html, grafico


def carregar_favorito(nome):
    favoritos = carregar_favoritos()
    for fav in favoritos:
        if fav.get("nome") == nome:
            html, graf = montar_paleta_html_grafico(fav["cores"], fav["porcentagens"])
            return (
                html,
                graf,
                fav["imagem"],
                fav["cores"],
                fav["porcentagens"],
                gr.Tabs.update(selected="Extrair"),
            )
    return "", None, None, [], [], gr.Tabs.update()


def favoritar_paleta(nome, cores, imagem, porcentagens):
    if not cores:
        return "Nenhuma paleta gerada ainda.", gerar_html_favoritos(), []
    if not nome.strip():
        return "Informe um nome para a paleta.", gerar_html_favoritos(), []
    if not imagem:
        return "Nenhuma imagem carregada.", gerar_html_favoritos(), []
    favoritos = carregar_favoritos()
    favoritos.append(
        {
            "nome": nome.strip(),
            "cores": cores,
            "imagem": imagem,
            "porcentagens": porcentagens,
        }
    )
    salvar_favoritos(favoritos)
    return f"Paleta '{nome}' salva.", gerar_html_favoritos(), lista_nomes_favoritos()


def gerar_paleta(imagem, num_cores):
    try:
        cores, porcentagens = extrair_cores_percentual(imagem, n_cores=num_cores)
    except BaseException as exc:  # noqa: BLE001
        html = f"<p style='color:red'>Erro ao extrair cores: {exc}</p>"
        return html, None, [], []
    html, grafico = montar_paleta_html_grafico(cores, porcentagens)
    return html, grafico, cores, porcentagens


def salvar_paleta(diretorio, nome_arquivo, cores):
    """Salva a imagem da paleta no diretório escolhido."""
    if not cores:
        return "Nenhuma paleta gerada ainda."

    if os.path.isabs(nome_arquivo):
        caminho = nome_arquivo
    else:
        caminho = os.path.join(diretorio, nome_arquivo)

    try:
        save_palette(caminho, cores)
        return f"Paleta salva em {os.path.abspath(caminho)}"
    except Exception as exc:
        return f"Erro ao salvar paleta: {exc}"


def salvar_paleta_sobre_imagem(diretorio, nome_arquivo, imagem, cores, pos):
    """Salva a imagem original com a paleta sobreposta no local escolhido."""
    if not cores or not imagem:
        return "Gere a paleta primeiro e carregue uma imagem."

    if os.path.isabs(nome_arquivo):
        caminho = nome_arquivo
    else:
        caminho = os.path.join(diretorio, nome_arquivo)

    try:
        img = overlay_palette_on_image(imagem, cores, pos)
        img.save(caminho)
        return f"Imagem salva em {os.path.abspath(caminho)}"
    except Exception as exc:  # noqa: BLE001
        return f"Erro ao salvar: {exc}"


def atualizar_programa():
    """Tenta atualizar o repositório local executando `git pull`."""
    repo_dir = find_git_root(REPO_DIR)
    if repo_dir is None:
        return "Repositório Git não encontrado."
    try:
        result = subprocess.run(
            ["git", "pull"], cwd=repo_dir, capture_output=True, text=True
        )
        if result.returncode == 0:
            return "Atualização concluída:\n" + result.stdout
        return "Erro ao atualizar:\n" + result.stderr
    except Exception as exc:
        return f"Falha ao executar git pull: {exc}"


def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Color Palette Extractor")
        with gr.Tabs(selected="Extrair") as abas:
            with gr.Tab("Favoritas"):
                fav_dropdown = gr.Dropdown(
                    choices=lista_nomes_favoritos(), label="Paletas Salvas"
                )
                carregar_fav = gr.Button("Carregar")
                favoritos_html = gr.HTML(gerar_html_favoritos())
            with gr.Tab("Extrair"):
                with gr.Row():
                    with gr.Column():
                        entrada_imagem = gr.Image(type="filepath", label="Imagem")
                        entrada_num_cores = gr.Slider(1, 10, value=5, step=1, label="Número de cores")
                        caminho_paleta = gr.Textbox("paleta.png", label="Nome do arquivo")
                        diretorio_paleta = gr.Textbox(".", label="Diretório da paleta")
                        caminho_overlay = gr.Textbox("overlay.png", label="Nome do arquivo da imagem")
                        diretorio_overlay = gr.Textbox(".", label="Diretório da imagem gerada")
                        pos_overlay = gr.Dropdown([
                            "top_left",
                            "top_right",
                            "bottom_left",
                            "bottom_right",
                            "center",
                        ], value="bottom_right", label="Posição da Paleta")
                        nome_favorito = gr.Textbox(label="Nome da Paleta")
                        executar = gr.Button("Extrair Cores")
                        salvar = gr.Button("Salvar Paleta")
                        salvar_overlay = gr.Button("Salvar Sobre Imagem")
                        favoritar = gr.Button("Favoritar")
                        atualizar = gr.Button("Atualizar Programa")
                    with gr.Column():
                        saida = gr.HTML()
                        grafico = gr.Image(label="Distribuição")
                        status = gr.Textbox(label="Status", interactive=False)
                        status_fav = gr.Textbox(label="Status Favorito", interactive=False)
                cores_state = gr.State([])
                porcent_state = gr.State([])

                executar.click(
                    gerar_paleta,
                    [entrada_imagem, entrada_num_cores],
                    [saida, grafico, cores_state, porcent_state],
                )
                salvar.click(
                    salvar_paleta,
                    [diretorio_paleta, caminho_paleta, cores_state],
                    status,
                )
                salvar_overlay.click(
                    salvar_paleta_sobre_imagem,
                    [
                        diretorio_overlay,
                        caminho_overlay,
                        entrada_imagem,
                        cores_state,
                        pos_overlay,
                    ],
                    status,
                )
                carregar_fav.click(
                    carregar_favorito,
                    fav_dropdown,
                    [saida, grafico, entrada_imagem, cores_state, porcent_state, abas],
                )
                favoritar.click(
                    favoritar_paleta,
                    [nome_favorito, cores_state, entrada_imagem, porcent_state],
                    [status_fav, favoritos_html, fav_dropdown],
                )
                atualizar.click(atualizar_programa, outputs=status)

    demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()
