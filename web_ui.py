import gradio as gr
from palette import extrair_cores
import subprocess
import os


def gerar_paleta(imagem, num_cores):
    cores = extrair_cores(imagem, n_cores=num_cores)
    blocos = "".join(
        f"<div style='width:40px;height:40px;background:{c};'></div>" for c in cores
    )
    html = f"<div style='display:flex;gap:2px;'>{blocos}</div><pre>\n" + "\n".join(cores) + "</pre>"
    return html


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
        with gr.Row():
            entrada_imagem = gr.Image(type="filepath", label="Imagem")
            entrada_num_cores = gr.Slider(1, 10, value=5, step=1, label="N\u00famero de cores")
        saida = gr.HTML()
        status = gr.Textbox(label="Status", interactive=False)
        executar = gr.Button("Extrair Cores")
        atualizar = gr.Button("Atualizar Programa")
        executar.click(gerar_paleta, [entrada_imagem, entrada_num_cores], saida)
        atualizar.click(atualizar_programa, outputs=status)
    demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()
