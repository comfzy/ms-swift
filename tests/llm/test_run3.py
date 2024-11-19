import os
import shutil
import tempfile
import unittest

import json

from swift.llm import MODEL_MAPPING, EncodePreprocessor, get_model_tokenizer, get_template, load_dataset


class TestRun3(unittest.TestCase):

    def setUp(self):
        print(f'Testing {type(self).__name__}.{self._testMethodName}')
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_dir = self._tmp_dir.name

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def load_ds(self, ds):
        train_dataset, val_dataset = load_dataset(
            ds,
            split_dataset_ratio=0.0,
            strict=False,
            num_proc=1,
            model_name=['小黄', 'Xiao Huang'],
            model_author=['魔搭', 'ModelScope'])
        return train_dataset.select(range(min(50, len(train_dataset))))

    # def test_model_load(self):
    #     if os.path.exists('./models.txt'):
    #         with open('./models.txt', 'r') as f:
    #             models = json.load(f)
    #     else:
    #         models = []
    #     for model_name, model_meta in MODEL_MAPPING.items():
    #         meta_requires = model_meta.requires or []
    #         for group in model_meta.model_groups:
    #             model = group.models[0]
    #             if 'skip_test' in (group.tags or []) or model.ms_model_id in models:
    #                 break
    #             requires = meta_requires + (group.requires or [])
    #             for req in requires:
    #                 os.system(f'pip install "{req}"')
    #             if not any(['transformers' in req for req in requires]):
    #                 os.system('pip install transformers -U')
    #             if not any(['accelerate' in req for req in requires]):
    #                 os.system('pip install accelerate -U')
    #             try:
    #                 model_arch_args = ''
    #                 if model_meta.model_arch:
    #                     model_arch_args = f'--model_arch {model_meta.model_arch}'
    #                 cmd = ('PYTHONPATH=. python tests/llm/load_model.py '
    #                        f'--ms_model_id {model.ms_model_id} {model_arch_args}')
    #                 if os.system(cmd) != 0:
    #                     raise RuntimeError()
    #             except Exception:
    #                 passed = False
    #             else:
    #                 passed = True
    #                 models.append(model.ms_model_id)
    #             finally:
    #                 if passed:
    #                     with open('./models.txt', 'w') as f:
    #                         json.dump(models, f)

    def test_template_load(self):
        if os.path.exists('./templates.txt'):
            with open('./templates.txt', 'r') as f:
                templates = json.load(f)
        else:
            templates = []
        for model_name, model_meta in MODEL_MAPPING.items():
            template = model_meta.template
            meta_requires = model_meta.requires or []
            for group in model_meta.model_groups:
                model = group.models[0]
                if 'skip_test' in (group.tags or []) or template in templates:
                    break
                requires = meta_requires + (group.requires or [])
                for req in requires:
                    os.system(f'pip install "{req}"')
                if not any(['transformers' in req for req in requires]):
                    os.system('pip install transformers -U')
                if not any(['accelerate' in req for req in requires]):
                    os.system('pip install accelerate -U')
                try:
                    cmd = ('PYTHONPATH=. python tests/llm/load_template.py '
                           f'--ms_model_id {model.ms_model_id} --template {template}')
                    if os.system(cmd) != 0:
                        raise RuntimeError()
                except Exception:
                    import traceback
                    print(traceback.format_exc())
                    passed = False
                else:
                    passed = True
                    templates.append(template)
                finally:
                    if passed:
                        with open('./templates.txt', 'w') as f:
                            json.dump(templates, f)


if __name__ == '__main__':
    unittest.main()
