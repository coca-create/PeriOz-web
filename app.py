import os
import sys
import gradio as gr
from gradio_components import gr_components as gc



with gr.Blocks() as UI:
    gc.gr_components()
port = int(os.environ.get('PORT', 8000))
UI.launch(server_name="0.0.0.0", server_port=port)
