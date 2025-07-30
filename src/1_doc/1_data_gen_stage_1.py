import json
import os
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


def get_inputs_list(file_path):
    """
    获取输入列表
    :param file_path:
    :return:
    """
    file_list = os.listdir(file_path)
    text = ''
    for file in file_list:
        with open(os.path.join(file_path, file), "r") as f:
            text += f.read()
    # 512个字符一组
    inputs_list = []
    for i in range(0, len(text), 512):
        inputs_list.append(text[i:i + 512])

    return inputs_list


def main():
    """
    主函数
    :return:
    """
    # history
    history = [
        {'role': 'system',
         'content': f'请根据以下【相关内容】的内容设计1到2个问题，用于后续构建问答对，形成用于大模型微调的训练集。\n' +
                    '注意，提出的问题应该具有一定的挑战性，注意问题中不要出现英文，问题通过两个换行符（\n\n）连接。'}
    ]
    # 获取输入列表
    inputs_list = get_inputs_list("../../data/1_doc/848说明书_txt_clean")
    inputs_list = [x.strip() for x in inputs_list]
    # 初始化队列和字典
    queue_inputs = RedisQueue('queue_inputs', maxsize=48)
    dict_outputs = RedisDict('dict_outputs', maxsize=48)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(inputs_list)}")
    question_list = data_gen(inputs_list, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(question_list)}")
    # save 2 json
    with open('../../data/1_doc/hnc_data_250730_stage_1.json', 'w', encoding='utf-8') as f:
        content2question = list(zip(inputs_list, question_list))
        json.dump(content2question, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
