# 参考graphgen，调用两个模型，一个作为老师模型，一个作为学生模型，
# 1.老师模型为每一个record生成k个的解释
# 2.学生模型为k个解释进行打分，对于每一个解释，生成一个概率值，表示该解释准确性的判断，取值范围为0-1


import json
import pandas as pd
import logging
import sys
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.insert(0, parent_dir)

from redis_model import RedisQueue, RedisDict
from utils import data_gen

logging.basicConfig(
    level=logging.INFO,
    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def data_trans(a, ap, r, s):
    content = ""
    if a != "":
        content += f"【故障现象】{a}\n"
    if ap != "":
        content += f"【故障原因】{ap}\n"
    content += f"【故障类型】{r}\n"
    content += f"【故障解决方案】{s}"
    return content


def teach_description(k):
    # 老师模型
    # 老师模型为每一个record生成k个的解释
    history = [
        {
            "role": "system",
            "content": "请根据我提供的故障诊断记录中的内容，生成意思相同的一句话，方便初入工程师理解和学习。"
            + "请保留必要的细节，但不需要过于冗长。"
            + "输出的句子应该流畅，语法正确。请直接输出改写后的句子，不需要任何附加信息。\n",
        }
    ]

    # load "../../data/2_kg/fd_data_clean_20250414.csv"
    df = (
        pd.read_csv("../../data/2_kg/fd_data_clean_20250414.csv")
        .fillna("")
        .values.tolist()
    )

    inputs = [data_trans(a, ap, r, s) for a, ap, r, s in df]

    # 初始化队列和字典
    queue_inputs = RedisQueue("queue_inputs", maxsize=60)
    dict_outputs = RedisDict("dict_outputs", maxsize=60)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(inputs)}")
    outputs = data_gen(inputs, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(outputs)}")
    # save 2 json
    with open(f"../../data/2_kg/kg_description_{k}.json", "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=4)


def student_score(k):
    # 学生模型
    # 学生模型为k个解释进行打分，对于每一个解释，生成一个概率值，表示该解释准确性的判断，取值范围为0-1
    history = [
        {
            "role": "system",
            "content": (
                "你是一个数控系统的从业人员，请根据我提供的故障诊断描述，判断你对其中涉及知识的**熟悉程度和理解能力**。\n"
                "你的任务是评估该描述的**可理解性**，而非其客观准确性。\n"
                "请输出一个0到1之间的**浮点数**作为概率值，表示你对该描述内容的理解程度。具体评分标准如下：\n"
                "- **0.0 - 0.2**: 完全无法理解，内容陌生或表述模糊。\n"
                "- **0.2 - 0.4**: 理解困难，需要大量额外信息或深入思考才能勉强理解。\n"
                "- **0.4 - 0.6**: 勉强可以理解，但仍存在不少疑问点或需反复推敲。\n"
                "- **0.6 - 0.8**: 可以比较轻松理解，大部分内容清晰明了。\n"
                "- **0.8 - 1.0**: 非常容易理解，内容清晰、准确，且与你的专业知识高度契合，无需额外解释。\n"
                "请**仅输出**该概率值，不要包含任何文字、标点符号或额外说明。"
            ),
        }
    ]

    # load "../../data/2_kg/kg_description_{k}.json"
    with open(f"../../data/2_kg/kg_description_{k}.json", "r", encoding="utf-8") as f:
        inputs = json.load(f)

    # 初始化队列和字典
    queue_inputs = RedisQueue("queue_inputs", maxsize=60)
    dict_outputs = RedisDict("dict_outputs", maxsize=60)
    queue_inputs.clear()
    dict_outputs.clear()
    logging.info(f"Start generating data, num: {len(inputs)}")
    outputs = data_gen(inputs, history, queue_inputs, dict_outputs)
    # close
    queue_inputs.close()
    dict_outputs.close()
    logging.info(f"End generating data, num: {len(outputs)}")
    # save 2 json
    with open(f"../../data/2_kg/kg_score_{k}.json", "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=4)


def get_score():
    # score 分析
    # 1. mean 分布

    scores = []
    for k in range(8):
        # load "../../data/2_kg/kg_score_{k}.json"
        with open(f"../../data/2_kg/kg_score_{k}.json", "r", encoding="utf-8") as f:
            s = json.load(f)
            s = [float(i) for i in s]
            s = [-np.log(i) for i in s]
            scores.append(s)

    scores = np.array(scores).T  # (n, 8)
    scores_mean = scores.mean(axis=1)

    # 绘制概率密度图 sns
    sns.kdeplot(scores_mean, label="mean")
    plt.savefig("scores.png")


if __name__ == "__main__":
    for k in range(8):
        teach_description(k)
        student_score(k)

    get_score()
