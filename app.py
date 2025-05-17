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
        f"📅 **Data:** {data}",
        f"\n🧠 **Plano de Conteúdo:**\n{to_markdown(plano)}",
        f"\n✍️ **Seu Rascunho:**\n{to_markdown(rascunho)}",
        f"\n✅ **Revisão Final:**\n{to_markdown(revisado)}"
    )

custom_theme = gr.themes.Soft(primary_hue="indigo", secondary_hue="pink", neutral_hue="gray")

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("""
# 📱 InstaPost: Sua IA para posts incríveis! ✨

Crie posts para o Instagram com estratégia, redação e revisão automática. Tudo com IA. Comece agora! 🚀
""")

    with gr.Tab("🔥 Criar Post do Zero"):
        with gr.Row():
            topico_input = gr.Textbox(label="Sobre o que você quer postar?", placeholder="Ex: IA na educação")
            gerar_btn = gr.Button("Criar meu Post!")

        with gr.Accordion("Ver Resultado", open=True):
            output_data = gr.Markdown()
            output_plano = gr.Markdown()
            output_rascunho = gr.Markdown()
            output_revisado = gr.Markdown()

        gerar_btn.click(
            fn=pipeline_criar_post,
            inputs=topico_input,
            outputs=[output_data, output_plano, output_rascunho, output_revisado]
        )

    with gr.Tab("📋 Só o Planejamento"):
        topico_plano = gr.Textbox(label="Tema do post", placeholder="Ex: Marketing Digital")
        btn_plano = gr.Button("Gerar Plano!")
        saida_plano = gr.Markdown()

        btn_plano.click(fn=agente_planejador, inputs=topico_plano, outputs=saida_plano)

    with gr.Tab("📝 Só a Redação"):
        topico_redator = gr.Textbox(label="Tema do post")
        plano_redator = gr.Textbox(label="Cole o plano aqui", lines=4)
        btn_redator = gr.Button("Criar Texto!")
        saida_redator = gr.Markdown()

        btn_redator.click(fn=agente_redator, inputs=[topico_redator, plano_redator], outputs=saida_redator)

    with gr.Tab("🔍 Só a Revisão"):
        topico_revisor = gr.Textbox(label="Tema do post")
        rascunho_revisor = gr.Textbox(label="Cole o rascunho aqui", lines=5)
        btn_revisor = gr.Button("Revisar Agora!")
        saida_revisor = gr.Markdown()

        btn_revisor.click(fn=agente_revisor, inputs=[topico_revisor, rascunho_revisor], outputs=saida_revisor)

if __name__ == "__main__":
    demo.launch()
