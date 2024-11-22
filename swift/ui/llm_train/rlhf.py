from typing import Type

import gradio as gr

from swift.llm import MODEL_MAPPING, TEMPLATE_MAPPING, ModelType
from swift.llm.model.register import get_matched_model_meta
from swift.ui.base import BaseUI


class RLHF(BaseUI):

    group = 'llm_train'

    locale_dict = {
        'rlhf_tab': {
            'label': {
                'zh': '人类对齐参数设置',
                'en': 'RLHF settings'
            },
        },
        'rlhf_type': {
            'label': {
                'zh': '人类对齐算法类型',
                'en': 'RLHF type'
            },
        },
        'ref_model_type': {
            'label': {
                'zh': '选择ref模型',
                'en': 'Select ref model'
            },
            'info': {
                'zh': 'SWIFT已支持的模型名称',
                'en': 'Base model supported by SWIFT'
            }
        },
        'ref_model': {
            'label': {
                'zh': 'ref模型id或路径',
                'en': 'Ref model id or path'
            },
            'info': {
                'zh': '实际的模型id或路径',
                'en': 'The actual model id or path'
            }
        },
        'beta': {
            'label': {
                'zh': 'KL正则项系数',
                'en': 'KL regression ratio'
            },
        },
        'loss_type': {
            'label': {
                'zh': 'Loss类型',
                'en': 'Loss type'
            },
        },
        'rpo_alpha': {
            'label': {
                'zh': 'DPO中混合sft交叉熵的系数',
                'en': 'DPO Cross Entropy ratio'
            },
        },
        'simpo_gamma': {
            'label': {
                'zh': 'SimPO reward margin',
                'en': 'SimPO reward margin'
            },
        },
        'desirable_weight': {
            'label': {
                'zh': 'KTO符合项系数',
                'en': 'KTO desirable ratio'
            },
        },
        'undesirable_weight': {
            'label': {
                'zh': 'KTO不符合项系数',
                'en': 'KTO undesirable ratio'
            },
        }
    }

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='rlhf_tab', open=False):
            with gr.Blocks():
                with gr.Row():
                    rlhf_type = gr.Dropdown(elem_id='rlhf_type')
                    ref_model_type = gr.Dropdown(
                        elem_id='ref_model_type',
                        choices=ModelType.get_model_name_list() + cls.get_custom_name_list(),
                        scale=20)
                    ref_model = gr.Textbox(elem_id='ref_model', lines=1, scale=20)
                    model_state = gr.State({})
                with gr.Row():
                    loss_type = gr.Dropdown(elem_id='loss_type')
                    beta = gr.Slider(elem_id='beta', minimum=0., maximum=5.0, step=0.1, scale=20)
                    gr.Slider(elem_id='rpo_alpha', minimum=0., maximum=2, step=0.1, scale=20)
                    gr.Slider(elem_id='simpo_gamma', minimum=0., maximum=2.0, step=0.1, scale=20)
                    gr.Slider(elem_id='desirable_weight', minimum=0., maximum=2.0, step=0.1, scale=20)
                    gr.Slider(elem_id='undesirable_weight', minimum=0., maximum=2.0, step=0.1, scale=20)

            def update_input_model(model, model_state=None):
                if model is None:
                    return None
                model_meta = get_matched_model_meta(model)
                if model_state and model in model_state:
                    model_type = model_state[model]
                elif model_meta:
                    model_type = model_meta.model_type if model_meta else None
                else:
                    model_type = None
                return model_type

            def update_model_id_or_path(model, model_type, model_state):
                if model is None or isinstance(model, list):
                    return model_state
                model_state[model] = model_type
                return model_state

            def update_value(rlhf_type):
                beta = None
                if rlhf_type in ['dpo', 'orpo', 'kto', 'cpo']:
                    beta = 0.1
                elif rlhf_type == 'simpo':
                    beta = 2.0

                loss_type = None
                if rlhf_type in ['dpo', 'cpo']:
                    loss_type = 'sigmoid'
                elif rlhf_type == 'kto':
                    loss_type = 'kto'

                return beta, loss_type

            rlhf_type.change(update_value, inputs=[rlhf_type], outputs=[beta, loss_type])

            ref_model.change(update_input_model, inputs=[ref_model, model_state], outputs=[ref_model_type])

            ref_model.change(
                update_model_id_or_path, inputs=[ref_model, ref_model_type, model_state], outputs=[model_state])
