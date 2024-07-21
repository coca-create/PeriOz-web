import gradio as gr
from tab3 import tab3_func as t3
from tab4 import tab4_func as t4
from tab5 import tab5_func as t5
from tab7 import tab7_func as t7
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
        ### Gradio-Tab3 ###
        
        with gr.Tab("SRT/VTT→Excel"):
            gr.Markdown("> 英語と日本語を並べて読むためのツールです。文字起こしの際に作成できるexcelファイルと同じです。2つのsrtファイルはタイムスタンプが一致している必要があります。")   
            lang_for_xls_choice = gr.Radio(
                choices=["English and Japanese", "only English", "only Japanese"],
                label="どんなExcelファイル？",
                interactive=True,
                value="English and Japanese"
            )
            with gr.Row(equal_height=True):
                english_file = gr.File(label="英語のSRTファイルをアップロード", visible=True)
                japanese_file = gr.File(label="日本語のSRTファイルをアップロード", visible=True)
                
            with gr.Row():        
                submit_button = gr.Button("Excelファイル作成",variant='primary')
                clear_button = gr.Button("クリア")   
            excel_output = gr.File(label="Excelファイルをダウンロード。")       
            dataframe_output = gr.Dataframe(wrap=True)
        
            
            # クリアボタンをクリックした時にファイルをクリア
            clear_button.click(
                fn=t3.clear_all_files,
                outputs=[english_file, japanese_file, dataframe_output, excel_output]
            )

            # ラジオボタンの選択変更でファイルのクリアとコンポーネントの表示を更新
            lang_for_xls_choice.change(
                fn=t3.update_visibility_and_clear,
                inputs=[lang_for_xls_choice],
                outputs=[english_file, japanese_file, dataframe_output, excel_output]
            )
            
        # ファイルを処理してデータフレームとExcelファイルを生成する
        def process_files(english_file, japanese_file, choice):
            if english_file is None and japanese_file is None:
                return pd.DataFrame({'1': [''], '2': [''], '3': ['']}), None
            
            if choice == "only English":
                excel_path, df = t3.create_excel_from_srt(english_path=english_file)
            elif choice == "only Japanese":
                excel_path, df = t3.create_excel_from_srt(japanese_path=japanese_file)
            else:  # "English and Japanese"
                excel_path, df = t3.create_excel_from_srt(english_path=english_file, japanese_path=japanese_file)
            return df, excel_path






        ### Gradio-Tab5 ###
        with gr.Tab("Word↔SRT/VTT/TXT"):
            gr.Markdown("> 日本語のwordファイルをsrtあるいはtxt形式に戻すためのプログラムです。wordファイルは末尾が[_srt.docx][_vtt.docx][_txtnr.docx],[_txtr.docx]、あるいは[_srt (1).docx]のように（1）の付加された日本語ファイルが対象です。複数のファイルを一度に扱えますが、アップロードは1回で行う必要があります。")  
            with gr.Column():
                with gr.Row():
                    to_srttxt_input = gr.File(label="Upload docx for srt/txt", file_count="multiple", type='filepath', file_types=["docx"])
                    to_srttxt_output = gr.File(label="Converted srt")
                with gr.Row():
                    to_srttxt_button = gr.Button("DOCX　→　SRT/TXT", variant='primary')
                    to_srttxt_clear_button = gr.Button("クリア")

            gr.Markdown("> 翻訳準備として、英語のsrtあるいはtxtファイルをword形式に変換するためのプログラムです。srtまたはtxtファイルは末尾が[.srt][.vtt][_NR.txt][_R.txt]のファイルのみ入力できます。複数のファイルを一度に扱えますが、アップロードは1回で行う必要があります。")
            with gr.Row():
                various_file_input = gr.File(file_count='multiple', label="Upload srt/txt for docx")
                output_doc_files = gr.File(file_count='multiple', label="Converted docx")
                
            with gr.Row():
                submit_transform_button = gr.Button("SRT/TXT　→　DOCX",variant='primary')
                clear_transform_button = gr.Button("クリア")
                 
        
        

        def t7_clear():
            return None,None,None,None,None,None
        def t4_clear():
            return None,"","",[]

        ### Tab3 イベントリスナー　###
        submit_button.click(
                fn=process_files,
                inputs=[english_file, japanese_file, lang_for_xls_choice],
                outputs=[dataframe_output, excel_output]
            )       



        ### Tab4 イベントリスナー ###
        file_input.change(fn=t4.display_file_content, inputs=file_input, outputs=[file_content, translated_text, output_file])
        translate_button.click(fn=t4.translate, inputs=[file_input, translated_text], outputs=output_file)

        t4_clear_button.click(fn=t4_clear,inputs=[],outputs=[file_input,file_content,translated_text,output_file])
   
   
         ### Tab5 イベントリスナー ###
        to_srttxt_button.click(
        fn=t5.convert_docx_to_srttxt,
        inputs=to_srttxt_input,
        outputs=to_srttxt_output
        )
        
        to_srttxt_clear_button.click(
            fn=t5.clear_inputs,
            inputs=[],
            outputs=[to_srttxt_input, to_srttxt_output]
        )
        submit_transform_button.click(t5.process_doc_files, inputs=various_file_input, outputs=output_doc_files)
        clear_transform_button.click(t5.clear_both, inputs=None, outputs=[various_file_input, output_doc_files])   


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

       
        return UI