import gradio as gr
from palette import extrair_cores_percentual, save_palette
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import subprocess
import os
import json

FAVORITES_FILE = "favorites.json"


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


def favoritar_paleta(nome, cores):
    if not cores:
        return "Nenhuma paleta gerada ainda.", gerar_html_favoritos()
    if not nome.strip():
        return "Informe um nome para a paleta.", gerar_html_favoritos()
    favoritos = carregar_favoritos()
    favoritos.append({"nome": nome.strip(), "cores": cores})
    salvar_favoritos(favoritos)
    return f"Paleta '{nome}' salva.", gerar_html_favoritos()


def gerar_paleta(imagem, num_cores):
    cores, porcentagens = extrair_cores_percentual(imagem, n_cores=num_cores)
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

    return html, grafico, cores


def salvar_paleta(caminho, cores):
    if not cores:
        return "Nenhuma paleta gerada ainda."
    try:
        save_palette(caminho, cores)
        return f"Paleta salva em {caminho}"
    except Exception as exc:
        return f"Erro ao salvar paleta: {exc}"


def atualizar_programa():
    """Tenta atualizar o repositório local executando `git pull`."""
    if not os.path.isdir(".git"):
        return "Repositório Git não encontrado."
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            return "Atualização concluída:\n" + result.stdout
        return "Erro ao atualizar:\n" + result.stderr
    except Exception as exc:
        return f"Falha ao executar git pull: {exc}"


def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Color Palette Extractor")
        with gr.Tabs(selected=1):
            with gr.Tab("Favoritas"):
                favoritos_html = gr.HTML(gerar_html_favoritos())
            with gr.Tab("Extrair"):
                with gr.Row():
                    entrada_imagem = gr.Image(type="filepath", label="Imagem")
                    entrada_num_cores = gr.Slider(1, 10, value=5, step=1, label="N\u00famero de cores")
                saida = gr.HTML()
                grafico = gr.Image(label="Distribuição")
                cores_state = gr.State([])
                caminho_paleta = gr.Textbox("paleta.png", label="Salvar como")
                nome_favorito = gr.Textbox(label="Nome da Paleta")
                status = gr.Textbox(label="Status", interactive=False)
                status_fav = gr.Textbox(label="Status Favorito", interactive=False)

                executar = gr.Button("Extrair Cores")
                salvar = gr.Button("Salvar Paleta")
                favoritar = gr.Button("Favoritar")
                atualizar = gr.Button("Atualizar Programa")

                executar.click(
                    gerar_paleta,
                    [entrada_imagem, entrada_num_cores],
                    [saida, grafico, cores_state],
                )
                salvar.click(salvar_paleta, [caminho_paleta, cores_state], status)
                favoritar.click(
                    favoritar_paleta,
                    [nome_favorito, cores_state],
                    [status_fav, favoritos_html],
                )
                atualizar.click(atualizar_programa, outputs=status)

    demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()
