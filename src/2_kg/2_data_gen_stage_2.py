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
         'content': '请根据【数控系统故障诊断记录】中的内容回答【问题】。\n' +
                    '注意：回答需要注意与【数控系统故障诊断记录】的关联性，尽量简洁易懂；回答中不要重复问题中的内容；回答内容中不要出现英文。'}
    ]
    # load content2question
    with open('../../data/2_kg/kg_data_1118_stage_1_clean.json', 'r', encoding='utf-8') as f:
        content2question_list = json.load(f)
    inputs_list = ["【数控系统故障诊断记录】 " + content + "\n" + "【问题】 " + question + "\n" + "【回答】 "
                   for content, question in content2question_list]

    # 初始化队列和字典
    queue_inputs = RedisQueue('queue_inputs', maxsize=60)
    dict_outputs = RedisDict('dict_outputs', maxsize=60)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(content2question_list)}")
    answer_list = data_gen(inputs_list, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(answer_list)}")
    # save 2 json
    with open('../../data/2_kg/kg_data_1118_stage_2.json', 'w', encoding='utf-8') as f:
        question_list = [question for _, question in content2question_list]
        question2answer_list = list(zip(question_list, answer_list))
        json.dump(question2answer_list, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
