import os
import sys
import gradio as gr
from gradio_components import gr_components as gc



with gr.Blocks() as UI:
    gc.gr_components()

UI.launch(debug=True, inbrowser=True, server_name="0.0.0.0", server_port=7860)
