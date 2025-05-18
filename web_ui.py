import gradio as gr
from palette import extrair_cores


def gerar_paleta(imagem, num_cores):
    cores = extrair_cores(imagem, n_cores=num_cores)
    blocos = "".join(
        f"<div style='width:40px;height:40px;background:{c};'></div>" for c in cores
    )
    html = f"<div style='display:flex;gap:2px;'>{blocos}</div><pre>\n" + "\n".join(cores) + "</pre>"
    return html


def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Color Palette Extractor")
        with gr.Row():
            entrada_imagem = gr.Image(type="filepath", label="Imagem")
            entrada_num_cores = gr.Slider(1, 10, value=5, step=1, label="N\u00famero de cores")
        saida = gr.HTML()
        executar = gr.Button("Extrair Cores")
        executar.click(gerar_paleta, [entrada_imagem, entrada_num_cores], saida)
    demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()
