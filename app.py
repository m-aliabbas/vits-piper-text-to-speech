#!/usr/bin/env python3
#
# Copyright      2022-2023  Xiaomi Corp.        (authors: Fangjun Kuang)
#
# See LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# References:
# https://gradio.app/docs/#dropdown

import os
import time
import uuid
from datetime import datetime

import gradio as gr
import soundfile as sf

from model import get_pretrained_model, language_to_models


def MyPrint(s):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{date_time}: {s}")


title = "# Next-gen Kaldi: Text-to-speech (TTS)"

description = """
This space shows how to convert text to speech with Next-gen Kaldi.

It is running on CPU within a docker container provided by Hugging Face.

See more information by visiting the following links:

- <https://github.com/k2-fsa/sherpa-onnx>

If you want to deploy it locally, please see
<https://k2-fsa.github.io/sherpa/>

If you want to use Android APKs, please see
<https://k2-fsa.github.io/sherpa/onnx/tts/apk.html>

If you want to use Android text-to-speech engine APKs, please see
<https://k2-fsa.github.io/sherpa/onnx/tts/apk-engine.html>

If you want to download an all-in-one exe for Windows, please see
<https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models>

"""

# css style is copied from
# https://huggingface.co/spaces/alphacep/asr/blob/main/app.py#L113
css = """
.result {display:flex;flex-direction:column}
.result_item {padding:15px;margin-bottom:8px;border-radius:15px;width:100%}
.result_item_success {background-color:mediumaquamarine;color:white;align-self:start}
.result_item_error {background-color:#ff7070;color:white;align-self:start}
"""

examples = [
    [
        "Chinese (Mandarin, 普通话)",
        "csukuangfj/vits-zh-hf-fanchen-wnj|1",
        "在一个阳光明媚的夏天，小马、小羊和小狗它们一块儿在广阔的草地上，嬉戏玩耍，这时小猴来了，还带着它心爱的足球活蹦乱跳地跑前、跑后教小马、小羊、小狗踢足球。",
        0,
        1.0,
    ],
    [
        "Chinese (Mandarin, 普通话)",
        "csukuangfj/vits-zh-hf-fanchen-C|187",
        '小米的使命是，始终坚持做"感动人心、价格厚道"的好产品，让全球每个人都能享受科技带来的美好生活。',
        0,
        1.0,
    ],
    ["Min-nan (闽南话)", "csukuangfj/vits-mms-nan", "ài piaǸ chiah ē iaN̂", 0, 1.0],
    ["Thai", "csukuangfj/vits-mms-tha", "ฉันรักคุณ", 0, 1.0],
    [
        "Chinese (Mandarin, 普通话)",
        "csukuangfj/sherpa-onnx-vits-zh-ll|5",
        "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与温柔。",
        2,
        1.0,
    ],
]


def update_model_dropdown(language: str):
    if language in language_to_models:
        choices = language_to_models[language]
        return gr.Dropdown(
            choices=choices,
            value=choices[0],
            interactive=True,
        )

    raise ValueError(f"Unsupported language: {language}")


def build_html_output(s: str, style: str = "result_item_success"):
    return f"""
    <div class='result'>
        <div class='result_item {style}'>
          {s}
        </div>
    </div>
    """


def process(language: str, repo_id: str, text: str, sid: str, speed: float):
    MyPrint(f"Input text: {text}. sid: {sid}, speed: {speed}")
    sid = int(sid)
    tts = get_pretrained_model(repo_id, speed)

    start = time.time()
    audio = tts.generate(text, sid=sid)
    end = time.time()

    if len(audio.samples) == 0:
        raise ValueError(
            "Error in generating audios. Please read previous error messages."
        )

    duration = len(audio.samples) / audio.sample_rate

    elapsed_seconds = end - start
    rtf = elapsed_seconds / duration

    info = f"""
    Wave duration  : {duration:.3f} s <br/>
    Processing time: {elapsed_seconds:.3f} s <br/>
    RTF: {elapsed_seconds:.3f}/{duration:.3f} = {rtf:.3f} <br/>
    """

    MyPrint(info)
    MyPrint(f"\nrepo_id: {repo_id}\ntext: {text}\nsid: {sid}\nspeed: {speed}")

    filename = str(uuid.uuid4())
    filename = f"{filename}.wav"
    sf.write(
        filename,
        audio.samples,
        samplerate=audio.sample_rate,
        subtype="PCM_16",
    )

    return filename, build_html_output(info)


demo = gr.Blocks(css=css)


with demo:
    gr.Markdown(title)
    language_choices = list(language_to_models.keys())

    language_radio = gr.Radio(
        label="Language",
        choices=language_choices,
        value=language_choices[0],
    )

    model_dropdown = gr.Dropdown(
        choices=language_to_models[language_choices[0]],
        label="Select a model",
        value=language_to_models[language_choices[0]][0],
    )

    language_radio.change(
        update_model_dropdown,
        inputs=language_radio,
        outputs=model_dropdown,
    )

    with gr.Tabs():
        with gr.TabItem("Please input your text"):
            input_text = gr.Textbox(
                label="Input text",
                info="Your text",
                lines=3,
                placeholder="Please input your text here",
            )

            input_sid = gr.Textbox(
                label="Speaker ID",
                info="Speaker ID",
                lines=1,
                max_lines=1,
                value="0",
                placeholder="Speaker ID. Valid only for mult-speaker model",
            )

            input_speed = gr.Slider(
                minimum=0.1,
                maximum=10,
                value=1,
                step=0.1,
                label="Speed (larger->faster; smaller->slower)",
            )

            input_button = gr.Button("Submit")

            output_audio = gr.Audio(label="Output")

            output_info = gr.HTML(label="Info")

            gr.Examples(
                examples=examples,
                fn=process,
                inputs=[
                    language_radio,
                    model_dropdown,
                    input_text,
                    input_sid,
                    input_speed,
                ],
                outputs=[
                    output_audio,
                    output_info,
                ],
            )

        input_button.click(
            process,
            inputs=[
                language_radio,
                model_dropdown,
                input_text,
                input_sid,
                input_speed,
            ],
            outputs=[
                output_audio,
                output_info,
            ],
        )

    gr.Markdown(description)


def download_espeak_ng_data():
    os.system(
        """
    cd /tmp
    wget -qq https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2
    tar xf espeak-ng-data.tar.bz2
    """
    )


if __name__ == "__main__":
    download_espeak_ng_data()
    formatter = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"

    demo.launch(share=True)
