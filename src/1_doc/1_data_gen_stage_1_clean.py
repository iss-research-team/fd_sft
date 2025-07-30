import os
import json


def data_clean():
    """
    获取输入列表
    :return:
    """
    # save 2 json
    with open('../../data/1_doc/hnc_data_1118_stage_1.json', 'r', encoding='utf-8') as f:
        content2question = json.load(f)
    # save 2 json: question_clean
    content2question_clean = []
    for content, question in content2question:
        question_ = question.split("\n\n")
        question_ = [q.strip() for q in question_]
        question_ = [q for q in question_ if q]
        for q in question_:
            if q.endswith("（"):
                q = q[:-1]
            content2question_clean.append((content, q))
    print(f"End generating data and Clean, num: {len(content2question_clean)}")
    with open('../../data/1_doc/hnc_data_1118_stage_1_clean.json', 'w', encoding='utf-8') as f:
        json.dump(content2question_clean, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data_clean()
