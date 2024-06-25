import os

import yaml


def load_lexicon() -> dict:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'lexicon.yaml')

    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
