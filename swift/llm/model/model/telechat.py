# Copyright (c) Alibaba, Inc. and its affiliates.

from ..model_arch import ModelArch
from swift.llm import TemplateType
from ..constant import LLMModelType
from ..register import Model, ModelGroup, ModelMeta, get_model_tokenizer_with_flash_attn, register_model

register_model(
    ModelMeta(
        LLMModelType.telechat,
        [
            ModelGroup([
                Model('TeleAI/TeleChat-7B', 'Tele-AI/telechat-7B'),
                Model('TeleAI/TeleChat-12B', 'Tele-AI/TeleChat-12B'),
                Model('TeleAI/TeleChat-12B-v2', 'Tele-AI/TeleChat-12B-v2'),
                Model('swift/TeleChat-12B-V2-GPTQ-Int4'),
            ]),
        ],
        TemplateType.telechat,
        get_model_tokenizer_with_flash_attn,
        model_arch=ModelArch.telechat,
        architectures=['TelechatForCausalLM'],
    ))

register_model(
    ModelMeta(
        LLMModelType.telechat2,
        [
            ModelGroup([
                Model('TeleAI/TeleChat2-115B', 'Tele-AI/TeleChat2-115B'),
            ]),
        ],
        TemplateType.telechat2,
        get_model_tokenizer_with_flash_attn,
        model_arch=ModelArch.telechat,
        architectures=['TelechatForCausalLM'],
    ))
