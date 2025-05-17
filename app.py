import os
import textwrap
from datetime import date
import gradio as gr
import google.generativeai as genai

# Configurar API
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyCJa54jrnfKHWzZoLAf39HopmLcJgUqCS8")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text.strip(), '> ', lambda _: True)

def agente_planejador(topico):
    prompt = f"""
Você é um estrategista de conteúdo.
Crie um plano de post para Instagram com base no tópico abaixo.
O plano deve conter os principais pontos, abordagem sugerida e estrutura do conteúdo.

Tópico: {topico}
"""
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def agente_redator(topico, plano):
    prompt = f"""
Você é um Redator Criativo especializado em criar posts virais para redes sociais.
Com base no plano abaixo, escreva um rascunho de post para Instagram com linguagem simples, tom humano e engajador.
Inclua de 2 a 4 hashtags no final.

Tópico: {topico}
Plano de Post: {plano}
"""
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def agente_revisor(topico, rascunho):
    prompt = f"""
Você é um revisor de conteúdo para redes sociais.
Revise o rascunho abaixo, ajustando clareza, tom e correção gramatical.
O público é jovem (18 a 30 anos) e o tom deve ser próximo, direto e motivador.

Tópico: {topico}
Rascunho: {rascunho}
"""
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def pipeline_criar_post(topico):
    data = date.today().strftime("%d/%m/%Y")
    plano = agente_planejador(topico)
    rascunho = agente_redator(topico, plano)
    revisado = agente_revisor(topico, rascunho)
    return (
        f"### 📅 Data: {data}",
        f"### 🧠 Plano de Conteúdo\n{to_markdown(plano)}",
        f"### ✍️ Rascunho Criado\n{to_markdown(rascunho)}",
        f"### ✅ Revisão Final\n{to_markdown(revisado)}"
    )

custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="amber",
    neutral_hue="gray"
)

with gr.Blocks(theme=custom_theme, css="""
    .gr-button {
        font-size: 16px !important;
        padding: 0.75em 1.5em !important;
        border-radius: 12px !important;
    }
    textarea, input {
        font-size: 16px !important;
    }
""") as demo:
    gr.Markdown("""
# 🎨 **PostCraft ✨**
### Oficina criativa de conteúdo com IA generativa

Crie conteúdos prontos para Instagram com estratégia, redação envolvente e revisão com linguagem atual.
""")

    with gr.Tab("🚀 Criar Post Completo"):
        with gr.Row():
            topico_input = gr.Textbox(label="🧩 Tópico do Post", placeholder="Ex: Como a IA pode transformar a educação")
            gerar_btn = gr.Button("✨ Gerar Post Completo")

        with gr.Accordion("📅 Resultado", open=True):
            output_data = gr.Markdown()
            output_plano = gr.Markdown()
            output_rascunho = gr.Markdown()
            output_revisado = gr.Markdown()

        gerar_btn.click(
            fn=pipeline_criar_post,
            inputs=topico_input,
            outputs=[output_data, output_plano, output_rascunho, output_revisado]
        )

    with gr.Tab("🧠 Apenas Planejamento"):
        topico_plano = gr.Textbox(label="📌 Tópico", placeholder="Ex: Marketing Digital pós-Gemini")
        btn_plano = gr.Button("Gerar Plano Criativo")
        saida_plano = gr.Markdown()

        btn_plano.click(fn=agente_planejador, inputs=topico_plano, outputs=saida_plano)

    with gr.Tab("✍️ Apenas Redação"):
        topico_redator = gr.Textbox(label="📌 Tópico")
        plano_redator = gr.Textbox(label="📋 Plano de Post", lines=4, placeholder="Cole o plano aqui...")
        btn_redator = gr.Button("Criar Rascunho")
        saida_redator = gr.Markdown()

        btn_redator.click(
            fn=agente_redator,
            inputs=[topico_redator, plano_redator],
            outputs=saida_redator
        )

    with gr.Tab("✅ Apenas Revisão"):
        topico_revisor = gr.Textbox(label="📌 Tópico")
        rascunho_revisor = gr.Textbox(label="📝 Rascunho do Post", lines=5, placeholder="Cole o rascunho aqui...")
        btn_revisor = gr.Button("Revisar Post")
        saida_revisor = gr.Markdown()

        btn_revisor.click(
            fn=agente_revisor,
            inputs=[topico_revisor, rascunho_revisor],
            outputs=saida_revisor
        )

if __name__ == "__main__":
    demo.launch()
