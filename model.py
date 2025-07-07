# # Copyright      2022-2023  Xiaomi Corp.        (authors: Fangjun Kuang)
# #
# # See LICENSE for clarification regarding multiple authors
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# import os
# from functools import lru_cache
# from pathlib import Path

# import sherpa_onnx
# from huggingface_hub import hf_hub_download


# def get_file(
#     repo_id: str,
#     filename: str,
#     subfolder: str = ".",
# ) -> str:
#     model_filename = hf_hub_download(
#         repo_id=repo_id,
#         filename=filename,
#         subfolder=subfolder,
#     )
#     return model_filename


# @lru_cache(maxsize=10)
# def _get_vits_vctk(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     assert repo_id == "csukuangfj/vits-vctk"

#     model = get_file(
#         repo_id=repo_id,
#         filename="vits-vctk.onnx",
#         subfolder=".",
#     )

#     lexicon = get_file(
#         repo_id=repo_id,
#         filename="lexicon.txt",
#         subfolder=".",
#     )

#     tokens = get_file(
#         repo_id=repo_id,
#         filename="tokens.txt",
#         subfolder=".",
#     )

#     tts_config = sherpa_onnx.OfflineTtsConfig(
#         model=sherpa_onnx.OfflineTtsModelConfig(
#             vits=sherpa_onnx.OfflineTtsVitsModelConfig(
#                 model=model,
#                 lexicon=lexicon,
#                 tokens=tokens,
#                 length_scale=1.0 / speed,
#             ),
#             provider="cpu",
#             debug=True,
#             num_threads=2,
#         ),
#         max_num_sentences=1,
#     )
#     tts = sherpa_onnx.OfflineTts(tts_config)

#     return tts


# @lru_cache(maxsize=10)
# def _get_vits_ljs(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     assert repo_id == "csukuangfj/vits-ljs"

#     model = get_file(
#         repo_id=repo_id,
#         filename="vits-ljs.onnx",
#         subfolder=".",
#     )

#     lexicon = get_file(
#         repo_id=repo_id,
#         filename="lexicon.txt",
#         subfolder=".",
#     )

#     tokens = get_file(
#         repo_id=repo_id,
#         filename="tokens.txt",
#         subfolder=".",
#     )

#     tts_config = sherpa_onnx.OfflineTtsConfig(
#         model=sherpa_onnx.OfflineTtsModelConfig(
#             vits=sherpa_onnx.OfflineTtsVitsModelConfig(
#                 model=model,
#                 lexicon=lexicon,
#                 tokens=tokens,
#                 length_scale=1.0 / speed,
#             ),
#             provider="cpu",
#             debug=True,
#             num_threads=2,
#         ),
#         max_num_sentences=1,
#     )
#     tts = sherpa_onnx.OfflineTts(tts_config)

#     return tts


# @lru_cache(maxsize=10)
# def _get_vits_piper(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     data_dir = "/tmp/espeak-ng-data"
#     repo_id = repo_id.split("|")[0]

#     if "coqui" in repo_id or "vits-mms" in repo_id:
#         name = "model"
#     elif "piper" in repo_id:
#         n = len("vits-piper-")
#         name = repo_id.split("/")[1][n:]
#     elif "mimic3" in repo_id:
#         n = len("vits-mimic3-")
#         name = repo_id.split("/")[1][n:]
#     else:
#         raise ValueError(f"Unsupported {repo_id}")

#     if "vits-coqui-uk-mai" in repo_id or "vits-mms" in repo_id:
#         data_dir = ""

#     model = get_file(
#         repo_id=repo_id,
#         filename=f"{name}.onnx",
#         subfolder=".",
#     )

#     tokens = get_file(
#         repo_id=repo_id,
#         filename="tokens.txt",
#         subfolder=".",
#     )

#     tts_config = sherpa_onnx.OfflineTtsConfig(
#         model=sherpa_onnx.OfflineTtsModelConfig(
#             vits=sherpa_onnx.OfflineTtsVitsModelConfig(
#                 model=model,
#                 lexicon="",
#                 data_dir=data_dir,
#                 tokens=tokens,
#                 length_scale=1.0 / speed,
#             ),
#             provider="cpu",
#             debug=True,
#             num_threads=2,
#         ),
#         max_num_sentences=1,
#     )
#     tts = sherpa_onnx.OfflineTts(tts_config)

#     return tts


# @lru_cache(maxsize=10)
# def _get_vits_mms(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     return _get_vits_piper(repo_id, speed)


# @lru_cache(maxsize=10)
# def _get_vits_zh_aishell3(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     assert repo_id == "csukuangfj/vits-zh-aishell3"

#     model = get_file(
#         repo_id=repo_id,
#         filename="vits-aishell3.onnx",
#         subfolder=".",
#     )

#     lexicon = get_file(
#         repo_id=repo_id,
#         filename="lexicon.txt",
#         subfolder=".",
#     )

#     tokens = get_file(
#         repo_id=repo_id,
#         filename="tokens.txt",
#         subfolder=".",
#     )

#     rule_fsts = ["phone.fst", "date.fst", "number.fst", "new_heteronym.fst"]

#     rule_fsts = [
#         get_file(
#             repo_id=repo_id,
#             filename=f,
#             subfolder=".",
#         )
#         for f in rule_fsts
#     ]
#     rule_fsts = ",".join(rule_fsts)

#     rule_fars = get_file(
#         repo_id=repo_id,
#         filename="rule.far",
#         subfolder=".",
#     )

#     tts_config = sherpa_onnx.OfflineTtsConfig(
#         model=sherpa_onnx.OfflineTtsModelConfig(
#             vits=sherpa_onnx.OfflineTtsVitsModelConfig(
#                 model=model,
#                 lexicon=lexicon,
#                 tokens=tokens,
#                 length_scale=1.0 / speed,
#             ),
#             provider="cpu",
#             debug=True,
#             num_threads=2,
#         ),
#         rule_fsts=rule_fsts,
#         rule_fars=rule_fars,
#         max_num_sentences=1,
#     )
#     tts = sherpa_onnx.OfflineTts(tts_config)

#     return tts


# @lru_cache(maxsize=10)
# def _get_vits_hf(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     repo_id = repo_id.split("|")[0]

#     if "fanchen" in repo_id or "vits-cantonese-hf-xiaomaiiwn" in repo_id:
#         model = repo_id.split("/")[-1]
#     elif "csukuangfj/vits-melo-tts-zh_en" == repo_id:
#         model = "model"
#     else:
#         model = repo_id.split("-")[-1]

#     if "sherpa-onnx-vits-zh-ll" in repo_id:
#         model = "model"

#     if not Path("/tmp/dict").is_dir():
#         os.system(
#             "cd /tmp; curl -SL -O https://github.com/csukuangfj/cppjieba/releases/download/sherpa-onnx-2024-04-19/dict.tar.bz2; tar xvf dict.tar.bz2"
#         )
#     os.system("ls -lh /tmp/dict")

#     model = get_file(
#         repo_id=repo_id,
#         filename=f"{model}.onnx",
#         subfolder=".",
#     )

#     lexicon = get_file(
#         repo_id=repo_id,
#         filename="lexicon.txt",
#         subfolder=".",
#     )

#     tokens = get_file(
#         repo_id=repo_id,
#         filename="tokens.txt",
#         subfolder=".",
#     )

#     rule_fars = ""

#     if "vits-cantonese-hf-xiaomaiiwn" not in repo_id:
#         rule_fsts = ["phone.fst", "date.fst", "number.fst"]

#         rule_fsts = [
#             get_file(
#                 repo_id=repo_id,
#                 filename=f,
#                 subfolder=".",
#             )
#             for f in rule_fsts
#         ]
#         rule_fsts = ",".join(rule_fsts)

#         #  rule_fars = get_file(
#         #      repo_id=repo_id,
#         #      filename="rule.far",
#         #      subfolder=".",
#         #  )
#         vits_dict_dir = "/tmp/dict"
#     else:
#         rule_fsts = get_file(
#             repo_id=repo_id,
#             filename="rule.fst",
#             subfolder=".",
#         )
#         vits_dict_dir = ""

#     tts_config = sherpa_onnx.OfflineTtsConfig(
#         model=sherpa_onnx.OfflineTtsModelConfig(
#             vits=sherpa_onnx.OfflineTtsVitsModelConfig(
#                 model=model,
#                 lexicon=lexicon,
#                 tokens=tokens,
#                 dict_dir=vits_dict_dir,
#                 length_scale=1.0 / speed,
#             ),
#             provider="cpu",
#             debug=True,
#             num_threads=2,
#         ),
#         rule_fsts=rule_fsts,
#         rule_fars=rule_fars,
#         max_num_sentences=1,
#     )
#     tts = sherpa_onnx.OfflineTts(tts_config)

#     return tts


# @lru_cache(maxsize=10)
# def get_pretrained_model(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
#     if repo_id in english_models:
#         return english_models[repo_id](repo_id, speed)
#     else:
#         raise ValueError(f"Unsupported repo_id: {repo_id}")


# english_models = {
#     "csukuangfj/vits-piper-en_GB-southern_english_male-medium|8 speakers": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-southern_english_female-medium|6 speakers": _get_vits_piper,
#     # piper, US
#     "csukuangfj/vits-piper-en_GB-sweetbbak-amy|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-amy-low|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-amy-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-arctic-medium|18 speakers": _get_vits_piper,  # 18 speakers
#     # "csukuangfj/vits-piper-en_US-danny-low|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-hfc_male-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-hfc_female-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-joe-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-kathleen-low|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-kusal-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-l2arctic-medium|24 speakers": _get_vits_piper,  # 24 speakers
#     # "csukuangfj/vits-piper-en_US-lessac-high|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-lessac-low|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-lessac-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-libritts-high|904 speakers": _get_vits_piper,  # 904 speakers
#     # "csukuangfj/vits-piper-en_US-libritts_r-medium|904 speakers": _get_vits_piper,  # 904 speakers
#     # "csukuangfj/vits-piper-en_US-ljspeech-high|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-ljspeech-medium|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-ryan-high|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-ryan-low|1 speaker": _get_vits_piper,
#     # "csukuangfj/vits-piper-en_US-ryan-medium|1 speaker": _get_vits_piper,
#     # piper, GB
#     "csukuangfj/vits-piper-en_GB-alan-low|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-alan-medium|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-alan-medium": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-cori-high|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-cori-medium|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-jenny_dioco-medium|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-northern_english_male-medium|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-semaine-medium|4 speakers": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-southern_english_female-low|1 speaker": _get_vits_piper,
#     "csukuangfj/vits-piper-en_GB-vctk-medium|109 speakers": _get_vits_piper,
# }


# language_to_models = {
#     "English": list(english_models.keys()),
# }


# friendly_model_names = {
#     "southern_english_male_medium": "csukuangfj/vits-piper-en_GB-southern_english_male-medium|8 speakers",
#     "southern_english_female_medium": "csukuangfj/vits-piper-en_GB-southern_english_female-medium|6 speakers",
#     "sweetbbak_amy": "csukuangfj/vits-piper-en_GB-sweetbbak-amy|1 speaker",
#     "alan_low": "csukuangfj/vits-piper-en_GB-alan-low|1 speaker",
#     "alan_medium": "csukuangfj/vits-piper-en_GB-alan-medium|1 speaker",
#     "cori_high": "csukuangfj/vits-piper-en_GB-cori-high|1 speaker",
#     "cori_medium": "csukuangfj/vits-piper-en_GB-cori-medium|1 speaker",
#     "jenny_dioco_medium": "csukuangfj/vits-piper-en_GB-jenny_dioco-medium|1 speaker",
#     "northern_english_male_medium": "csukuangfj/vits-piper-en_GB-northern_english_male-medium|1 speaker",
#     "semaine_medium": "csukuangfj/vits-piper-en_GB-semaine-medium|4 speakers",
#     "southern_english_female_low": "csukuangfj/vits-piper-en_GB-southern_english_female-low|1 speaker",
#     "vctk_medium": "csukuangfj/vits-piper-en_GB-vctk-medium|109 speakers"
# }

import os
from functools import lru_cache
from pathlib import Path

import sherpa_onnx
from huggingface_hub import hf_hub_download


def get_file(repo_id: str, filename: str, subfolder: str = ".") -> str:
    return hf_hub_download(repo_id=repo_id, filename=filename, subfolder=subfolder)


@lru_cache(maxsize=10)
def _get_vits_piper(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
    data_dir = "/tmp/espeak-ng-data"
    repo_id = repo_id.split("|")[0]

    name = repo_id.split("/")[1].replace("vits-piper-", "")

    model = get_file(repo_id, f"{name}.onnx")
    tokens = get_file(repo_id, "tokens.txt")

    tts_config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=model,
                lexicon="",
                data_dir=data_dir,
                tokens=tokens,
                length_scale=1.0 / speed,
            ),
            provider="cpu",
            debug=False,
            num_threads=2,
        ),
        max_num_sentences=1,
    )
    return sherpa_onnx.OfflineTts(tts_config)


@lru_cache(maxsize=10)
def get_pretrained_model(repo_id: str, speed: float) -> sherpa_onnx.OfflineTts:
    if repo_id in english_models:
        return english_models[repo_id](repo_id, speed)
    raise ValueError(f"Unsupported repo_id: {repo_id}")


# ✅ Friendly name mapping
friendly_model_names = {
    "southern_english_male_medium": "csukuangfj/vits-piper-en_GB-southern_english_male-medium|8 speakers",
    "southern_english_female_medium": "csukuangfj/vits-piper-en_GB-southern_english_female-medium|6 speakers",
    "sweetbbak_amy": "csukuangfj/vits-piper-en_GB-sweetbbak-amy|1 speaker",
    "alan_low": "csukuangfj/vits-piper-en_GB-alan-low|1 speaker",
    "alan_medium": "csukuangfj/vits-piper-en_GB-alan-medium|1 speaker",
    "cori_high": "csukuangfj/vits-piper-en_GB-cori-high|1 speaker",
    "cori_medium": "csukuangfj/vits-piper-en_GB-cori-medium|1 speaker",
    "jenny_dioco_medium": "csukuangfj/vits-piper-en_GB-jenny_dioco-medium|1 speaker",
    "northern_english_male_medium": "csukuangfj/vits-piper-en_GB-northern_english_male-medium|1 speaker",
    "semaine_medium": "csukuangfj/vits-piper-en_GB-semaine-medium|4 speakers",
    "southern_english_female_low": "csukuangfj/vits-piper-en_GB-southern_english_female-low|1 speaker",
    "vctk_medium": "csukuangfj/vits-piper-en_GB-vctk-medium|109 speakers"
}

# ✅ Registered models
english_models = {
    repo_id: _get_vits_piper
    for repo_id in friendly_model_names.values()
}

def get_available_speakers(id) -> list[str]:
    """Return a list of available speakers."""
    speakers = friendly_model_names.get(id, None)
    if speakers is None:
        raise ValueError(f"Unknown model ID: {id}")
    num_speakers = speakers.split("|")[-1].strip()

    return num_speakers.split(" ")[0].split("_")[0]