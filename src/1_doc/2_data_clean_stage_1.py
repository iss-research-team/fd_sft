import json
import logging
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.insert(0, parent_dir)

from redis_model import RedisQueue, RedisDict
from utils import data_gen

logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    # history
    history = [
        {'role': 'system',
         'content': '请对下列【问题】和对应的【回答】进行整理，这些问答对将用于模型微调。\n' +
                    '注意：请在保证内容完整正确的情况下，尽量简洁；整理后的内容中不要出现英文。'},
    ]
    # load content2question
    with open('../../data/1_doc/hnc_data_1118_stage_2.json', 'r', encoding='utf-8') as f:
        question2answer_list = json.load(f)
    inputs_list = ["【问题】 " + question + "\n" + "【回答】 " + answer
                   for question, answer in question2answer_list]

    # 初始化队列和字典
    queue_inputs = RedisQueue('queue_inputs', maxsize=48)
    dict_outputs = RedisDict('dict_outputs', maxsize=48)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(question2answer_list)}")
    question2answer_list_clean = data_gen(inputs_list, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(question2answer_list_clean)}")
    # save 2 json
    with open('../../data/1_doc/hnc_data_1118_stage_3.json', 'w', encoding='utf-8') as f:
        # question2answer_list_clean = [question2answer.split('【回答】') for question2answer in question2answer_list_clean]
        # question2answer_list_clean = [[question2answer[0].replace('【问题】', '').strip(), question2answer[1].strip()]
        #                               for question2answer in question2answer_list_clean]
        json.dump(question2answer_list_clean, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
