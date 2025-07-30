import json
import logging

from src.redis_model import RedisQueue, RedisDict
from src.utils import data_gen

logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    # history
    history = [
        {'role': 'system',
         'content': '请对下列【问题】和对应的【回答】进行整理，这些问答对将用于模型微调。\n' +
                    '注意：请在保证内容完整正确的情况下，尽量简洁；整理后的内容中不要出现英文。'},
        {'role': 'user',
         'content': '【问题】 导致机床空载运行时报速偏差过大的原因可能是什么？\n' +
                    '【回答】 导致机床空载运行时报速偏差过大的原因可能是电机相序接反了。'},
        {'role': 'assistant',
         'content': '【问题】 导致机床空载运行时报速偏差过大的原因可能是什么？\n' +
                    '【回答】 可能是电机相序接反了。'},
        {'role': 'user',
         'content': '【问题】 数控系统在运行时出现主电路欠压报警的原因是什么\n' +
                    '【回答】 数控系统在运行时出现主电路欠压报警的原因是主轴电机升速时间过短导致的。'},
        {'role': 'assistant',
         'content': '【问题】 数控系统在运行时出现主电路欠压报警的原因是什么\n' +
                    '【回答】 主轴电机升速时间过短导致。'},
        {'role': 'user',
         'content': '【问题】 在处理数控系统中出现的“指令超频”报警时，应该首先检查哪些关键参数？\n' +
                    '【回答】 在处理数控系统中出现的“指令超频”报警时，应该首先检查的关键参数包括：\n\n- 参数100517“最高速度限制”设置是否合理。\n- 参数100523“控制方式选择”设置是否合理。\n- 参数100586“电机额定电流”设置是否合理。\n- 参数100587“电机额定转速”设置是否合理。\n- 参数100004和100005“电子齿轮比分子/分母”设置是否合理。\n- 参数500010“工作模式”设置是否合理。\n- 参数500016“编码器类型”设置是否合理。'},
        {'role': 'assistant',
         'content': '【问题】 在处理数控系统中出现的“指令超频”报警时，应该首先检查哪些关键参数？\n' +
                    '【回答】 应该首先检查的关键参数包括：\n- 参数100517“最高速度限制”设置是否合理。\n- 参数100523“控制方式选择”设置是否合理。\n- 参数100586“电机额定电流”设置是否合理。\n- 参数100587“电机额定转速”设置是否合理。\n- 参数100004和100005“电子齿轮比分子/分母”设置是否合理。\n- 参数500010“工作模式”设置是否合理。\n- 参数500016“编码器类型”设置是否合理。'},
    ]
    # load content2question
    with open('../../data/2_kg/kg_data_1118_stage_2.json', 'r', encoding='utf-8') as f:
        question2answer_list = json.load(f)
    inputs_list = ["【问题】 " + question + "\n" + "【回答】 " + answer
                   for question, answer in question2answer_list]

    # 初始化队列和字典
    queue_inputs = RedisQueue('queue_inputs', maxsize=32)
    dict_outputs = RedisDict('dict_outputs', maxsize=32)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(question2answer_list)}")
    question2answer_list_clean = data_gen(inputs_list, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(question2answer_list_clean)}")
    # save 2 json
    with open('../../data/2_kg/kg_data_1118_stage_3.json', 'w', encoding='utf-8') as f:
        # question2answer_list_clean = [question2answer.split('【回答】') for question2answer in question2answer_list_clean]
        # question2answer_list_clean = [[question2answer[0].replace('【问题】', '').strip(), question2answer[1].strip()]
        #                               for question2answer in question2answer_list_clean]
        json.dump(question2answer_list_clean, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
