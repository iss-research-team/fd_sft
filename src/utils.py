import requests
# from zhipuai import ZhipuAI
import logging
import time
import json

logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


# def chat(inputs, history, if_local=False):
#     if if_local:
#         # 调用本地chat server
#         res = requests.post(f'http://192.168.1.115:9020//chat',
#                             json={"inputs": inputs, "history": history},
#                             timeout=60)
#         res_data = res.json()
#         outputs = res_data['data'] if res_data['code'] == 200 else "chat server error"
#     else:
#         # 调用GLM-4 api接口
#         client = ZhipuAI(api_key="3de96d0e754a7bc50352fc1f8fff76dd.yBJ5fsB4wQAJqrYi")  # 填写您自己的APIKey
#         response = client.chat.completions.create(
#             model="glm-4",  # 填写需要调用的模型名称
#             messages=[{"role": "user", "content": inputs}],
#         )
#         outputs = response.choices[0].message.content
#     return outputs


# def load_prompt():
#     # load prompt
#     role_prompt_path = "../prompt/role_prompt.txt"
#     with open(role_prompt_path, 'r', encoding='utf-8') as f:
#         role_prompt = f.read()
#     # # load example
#     # example_path = "prompt/task_prompt.json"
#     # with open(example_path, 'r', encoding='utf-8') as f:
#     #     example = json.load(f)
#     # history
#     history = [{"role": "system", "content": role_prompt}]
#     return history


def data_gen(text_list, history, queue_inputs, dict_outputs):
    """
    内容生成
    :param text_list:
    :param history:
    :param queue_inputs:
    :param dict_outputs:
    :return:
    """
    index_enqueue = 0
    index_dequeue = 0
    # start time
    logging.info(f"Start extracting keyword...")

    index_enqueue2label = dict()

    try:
        while True:
            if len(index_enqueue2label) == len(text_list):
                break

            while index_enqueue < index_dequeue + 40 and index_enqueue < len(text_list):
                text = text_list[index_enqueue]
                queue_inputs.enqueue(id_=index_enqueue, inputs=text, history=history)
                logging.info(f"Enqueue: {index_enqueue}")
                index_enqueue += 1

            if dict_outputs.size() > 20 or index_enqueue == len(text_list):
                index_enqueue_list_temp = dict_outputs.get_keys()
                for index_enqueue_ in index_enqueue_list_temp:
                    output = dict_outputs.get(index_enqueue_).decode('utf-8')
                    dict_outputs.delete(index_enqueue_)
                    logging.info(f"Dequeue: {index_dequeue}")
                    index_dequeue += 1
                    index_enqueue2label[index_enqueue_] = output
            time.sleep(0.1)
    except BaseException as e:
        logging.error(e)
    index_enqueue2label = sorted(index_enqueue2label.items(), key=lambda x: int(x[0]))
    return [x[1] for x in index_enqueue2label]


def data_analysis(inputs_list):
    """
    分析数据长度的分布
    :param data_path:
    :return:
    """

    inputs_list = [inputs['instruction'] + inputs['input'] + inputs['output'] for inputs in inputs_list]
    inputs_len_list = [len(inputs) for inputs in inputs_list]
    rank = [10 * i for i in range(1, 21)]
    rank2count = {r: 0 for r in rank}
    for inputs_len in inputs_len_list:
        for r in rank:
            if inputs_len <= r:
                rank2count[r] += 1
                break
    print(rank2count)
