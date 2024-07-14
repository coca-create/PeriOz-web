import gradio as gr
from tab7 import tab7_func as t7
from tab4 import tab4_func as t4
import pandas as pd

def gr_components():
    with gr.Blocks() as UI:
        with gr.Tab("original字幕の再編"):
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
                    dummy_file=gr.File(visible=False)       

        with gr.Tab("翻訳ファイルの作成補助"):
            gr.Markdown(
                """
                # ピリオドによる再編成はしません。翻訳ファイル作成のお手伝いのみです。
                <p style="color:gray; letter-spacing:0.05em;">SRTファイル、VTTファイルをアップロードしてね。日本語字幕ファイルをダウンロードしたら、Subtitle Editなどのアプリで開きます。長い文の自動分割機能を使うと読みやすくなります。</p>
                """)        
            gr.Markdown("> srt,vtt,txt,docxのいずれかの英文ファイルをアップロードすると内容が表示されます。次にGoogle翻訳で得た翻訳をテキストエリアに入力します。「翻訳ファイルを作成」ボタンを押して、入力ファイルと同形式のファイルに保存します。ファイル名に _ja が付加されます。")
            with gr.Row():
                file_input = gr.File(label="Upload file", file_count="single", file_types=['docx', 'txt', 'srt','vtt'])
                output_file = gr.File(label="Translated file" ,type='filepath')
            
            with gr.Row():
                t4_clear_button=gr.Button("クリア")
                translate_button = gr.Button("翻訳ファイル作成", variant='primary')
            
            with gr.Row():
                file_content = gr.HTML(label="File content")
                translated_text = gr.TextArea(label="Translated text")



        def t7_clear():
            return None,None,None,None,None,None
        def t4_clear():
            return None,"","",[]
        

        ### Tab7 イベントリスナー ###
        vtt_input.upload(
        fn=t7.process_file, inputs=[vtt_input], outputs=[vtt_output_1, vtt_output_2,dummy_file]
    )
        t7_translate_button.click(
            fn=t7.vtt_translate,
            inputs=[vtt_input, vtt_translated_content,dummy_file],
            outputs=[vtt_translated_file]
        )
        t7_clear_button.click(
            fn=t7_clear,
            inputs=[],
            outputs=[vtt_input,vtt_translated_content,vtt_translated_file,vtt_output_1,vtt_output_2,dummy_file]
        )


        ### Tab4 イベントリスナー ###
        file_input.change(fn=t4.display_file_content, inputs=file_input, outputs=[file_content, translated_text, output_file])
        translate_button.click(fn=t4.translate, inputs=[file_input, translated_text], outputs=output_file)

        t4_clear_button.click(fn=t4_clear,inputs=[],outputs=[file_input,file_content,translated_text,output_file])        
        return UI