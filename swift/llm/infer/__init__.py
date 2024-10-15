# Copyright (c) Alibaba, Inc. and its affiliates.
from typing import TYPE_CHECKING

from swift.utils.import_utils import _LazyModule

if TYPE_CHECKING:
    from .deploy import deploy_main
    from .infer import infer_main, merge_lora_main, merge_lora
    from .utils import InferStats
    from .vllm import VllmEngine
    from .lmdeploy import LMDeployFramework, LmdeployGenerationConfig
    from .transformers import TransformersFramework
    from .protocol import InferRequest, RequestConfig
else:
    _extra_objects = {k: v for k, v in globals().items() if not k.startswith('_')}
    _import_structure = {
        'utils': ['InferStats'],
        'deploy': ['deploy_main'],
        'infer': ['infer_main', 'merge_lora_main', 'merge_lora'],
        'vllm': ['VllmEngine'],
        'lmdeploy': ['LMDeployFramework', 'LmdeployGenerationConfig'],
        'transformers': ['TransformersFramework'],
        'protocol': ['InferRequest', 'RequestConfig'],
    }

    import sys

    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects=_extra_objects,
    )