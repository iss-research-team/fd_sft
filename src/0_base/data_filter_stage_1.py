import json
import os
import logging

from src.redis_model import RedisQueue, RedisDict
from src.utils import data_gen

logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def get_inputs_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        inputs_list = json.load(f)
    inputs_list_ = []
    for inputs in inputs_list:
        if 'input' in inputs:
            inputs_list_.append('【instruction】 ' + inputs['instruction'] + '\n' +
                                '【input】 ' + inputs['input'] + '\n' +
                                '【output】 ' + inputs['output'])
        else:
            inputs_list_.append('【instruction】 ' + inputs['instruction'] + '\n' +
                                '【output】 ' + inputs['output'])

    return inputs_list_


def main():
    """
    主函数
    :return:
    """
    # history
    history = [
        {'role': 'system',
         'content': f'请帮我为以下微调数据标注标签，请帮我将与**工业|制造业（领域）**相关的记录或者**问答|推理（任务）**相关的记录标记为1，其余标记为0。' +
                    '注意：为了保证微调数据的数量，领域的要求与任务的要求满足一个即可。'},
    ]
    # 获取输入列表

    inputs_list = get_inputs_list("../../data/0_base/alpaca_gpt4_data_zh.json")
    inputs_list = [x.strip() for x in inputs_list]
    # 初始化队列和字典
    queue_inputs = RedisQueue('queue_inputs', maxsize=32)
    dict_outputs = RedisDict('dict_outputs', maxsize=32)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(inputs_list)}")
    label_list = data_gen(inputs_list, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(label_list)}")
    # save 2 json
    with open("../../data/0_base/alpaca_gpt4_data_zh_labeled.json", 'w', encoding='utf-8') as f:
        content2question = list(zip(inputs_list, label_list))
        json.dump(content2question, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
