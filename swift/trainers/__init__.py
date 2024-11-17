# Copyright (c) Alibaba, Inc. and its affiliates.
from typing import TYPE_CHECKING

from transformers.trainer_callback import TrainerCallback
from transformers.trainer_utils import (EvaluationStrategy, FSDPOption, HPSearchBackend, HubStrategy, IntervalStrategy,
                                        SchedulerType)

from swift.utils.import_utils import _LazyModule
from . import callback

try:
    # https://github.com/huggingface/transformers/pull/25702
    from transformers.trainer_utils import ShardedDDPOption
except ImportError:
    ShardedDDPOption = None

if TYPE_CHECKING:
    from .arguments import (Seq2SeqTrainingArguments, TrainingArguments, DPOConfig, CPOConfig, KTOConfig, ORPOConfig,
                            PPOConfig)
    from .rlhf_trainer import CPOTrainer, DPOTrainer, KTOTrainer, ORPOTrainer, RLHFTrainerMixin, PPOTrainer
    from .trainer_factory import TrainerFactory
    from .trainers import Seq2SeqTrainer, Trainer
    from .mixin import SwiftMixin

else:
    _import_structure = {
        'arguments': [
            'Seq2SeqTrainingArguments', 'TrainingArguments', 'DPOConfig', 'CPOConfig', 'KTOConfig', 'ORPOConfig',
            'PPOConfig'
        ],
        'rlhf_trainer': ['CPOTrainer', 'DPOTrainer', 'KTOTrainer', 'ORPOTrainer', 'RLHFTrainerMixin', 'PPOTrainer'],
        'trainer_factory': ['TrainerFactory'],
        'trainers': ['Seq2SeqTrainer', 'Trainer'],
        'mixin': ['SwiftMixin'],
    }

    import sys

    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
