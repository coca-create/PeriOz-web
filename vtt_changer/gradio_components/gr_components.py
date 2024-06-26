import gradio as gr
from tab7 import tab7_func as t7
import pandas as pd

def gr_components():
    with gr.Blocks() as UI:
        gr.Markdown(
            """
            # 既存の字幕ファイルをピリオド区切りに再編します。
            <p style="color:gray; letter-spacing:0.05em;">SRTファイル、VTTファイルをアップロードしてね。日本語字幕ファイルをダウンロードしたら、Subtitle Editなどのアプリで開きます。長い文の自動分割機能を使うと読みやすくなります。</p>
            """)        
        
        ### Gradio-Tab7 ###
        with gr.Column():
            gr.Markdown("> original動画に付属する字幕をピリオド区切りに再編し、翻訳した字幕ファイルを作ります。")
            with gr.Row():
                vtt_input = gr.File(label="vtt/srtファイルをアップロードしてください。")  # input用のoriginal vtt,srt
                with gr.Column():
                    vtt_output_2 = gr.File(label="ピリオド区切りの英語字幕ファイルとワードファイルです。",file_count="multiple")  # 分割・結合処理後のvtt,srtファイル
                    vtt_translated_file = gr.File(label="ピリオド区切りの英文から作った日本語字幕ファイルです。")  # 翻訳されたvtt,srtファイルの出力
            with gr.Row():
                t7_clear_button = gr.Button("クリア")  
                t7_translate_button = gr.Button("日本語vtt,srtの作成",variant='primary')
            with gr.Row():
                vtt_output_1 = gr.HTML()  # 分割・結合処理後のHTML表示
                vtt_translated_content = gr.TextArea(label="翻訳された字幕情報を貼り付けてください。")  # 翻訳処理後の内容を貼り付け。        

        def t7_clear():
            return None,None,None,None,None

        ### Tab7 イベントリスナー ###
        vtt_input.upload(
        fn=t7.process_file, inputs=[vtt_input], outputs=[vtt_output_1, vtt_output_2]
    )
        t7_translate_button.click(
            fn=t7.vtt_translate,
            inputs=[vtt_input, vtt_translated_content],
            outputs=[vtt_translated_file]
        )
        t7_clear_button.click(
            fn=t7_clear,
            inputs=[],
            outputs=[vtt_input,vtt_translated_content,vtt_translated_file,vtt_output_1,vtt_output_2]
        )
        return UI