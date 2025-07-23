import json
import os
import logging

from src.redis_model import RedisQueue, RedisDict
from src.utils import data_analysis

logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    with open('../../data/0_base/alpaca_gpt4_data_zh.json', 'r', encoding='utf-8') as f:
        inputs_list = json.load(f)
    with open('../../data/0_base/alpaca_gpt4_data_zh_labeled.json', 'r', encoding='utf-8') as f:
        label_list = json.load(f)
    inputs_list_clean = []
    for inputs, label in zip(inputs_list, label_list):
        if label[1].startswith('1'):
            inputs_list_clean.append(inputs)

    print(len(inputs_list_clean))

    # save
    # with open('../../data/0_base/alpaca_gpt4_data_zh_clean.json', 'w', encoding='utf-8') as f:
    #     json.dump(inputs_list_clean, f, ensure_ascii=False, indent=4)

    data_analysis(inputs_list_clean)
    # {50: 99, 100: 220, 150: 281, 200: 388, 250: 351, 300: 417, 350: 599, 400: 653, 450: 521, 500: 339, 550: 149, 600: 59, 650: 23, 700: 17, 750: 13, 800: 9, 850: 12, 900: 8, 950: 10, 1000: 6}


if __name__ == '__main__':
    main()
