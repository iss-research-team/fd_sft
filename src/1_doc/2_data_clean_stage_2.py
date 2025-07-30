import json
import os
import re
from tqdm import tqdm
from data_gen.src.utils import data_analysis


def remove_same_part(question, answer):
    """
    去除问题和答案的相同部分
    :param question:
    :param answer:
    :return:
    """
    end_cut_bit = 0
    for i in range(len(question)):
        if question[i] == answer[i]:
            end_cut_bit += 1
        else:
            break
    answer = answer[end_cut_bit:]
    return answer


def remove_fun_words(answer):
    """
    去除答案前面的虚词
    :return: 
    """
    fun_words = ['的']
    for fun_word in fun_words:
        if answer.startswith(fun_word):
            answer = answer[len(fun_word):]
    return answer


def remove_hat(question, answer):
    """
    去除问题和答案的相同部分
    :param question:
    :param answer:
    :return:
    """
    question_hat = question.split("，")[0]
    answer_hat = answer.split("，")[0]
    if question_hat == answer_hat:
        answer = answer[len(answer_hat) + 1:]
    return answer


def remove_2hat(question, answer):
    """
    去除问题和答案的相同部分
    :param question:
    :param answer:
    :return:
    """
    question_hat = question.split("，")[:2]
    answer_hat = answer.split("，")[:2]
    if question_hat == answer_hat:
        answer = answer.replace(answer_hat[0] + '，', "").replace(answer_hat[1] + '，', "")
    return answer


def load_already(file_path):
    """
    加载已经下载的数据
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            already_down = json.load(f)
    else:
        already_down = {}
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(already_down, f, ensure_ascii=False, indent=4)
    return already_down


def load_inputs(file_path):
    """
    加载输入
    :param file_path:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        inputs_list = json.load(f)

    question2answer_list_clean = []
    pattern = re.compile(r"【问题.?】|【回答.?】")

    for qa in inputs_list:
        qa = qa.strip()
        qa_list = re.split(pattern, qa)[1:]
        for i in range(0, len(qa_list), 2):
            question = qa_list[i].strip()
            answer = qa_list[i + 1].strip()
            question2answer_list_clean.append([question, answer])
    return question2answer_list_clean


def data_clean(input_path, already_done_path, output_path):
    """
    获取输入列表
    :return:
    """
    # load data
    question2answer_list = load_inputs(input_path)
    # already_down path
    already_down = load_already(already_done_path)

    print(f"Start generating data, num: {len(question2answer_list)}")
    # save 2 json: question_clean

    index = 0
    try:
        while index < len(question2answer_list):
            question, answer = question2answer_list[index]
            question = question.strip()
            if question.startswith("（") and question.endswith("）"):
                index += 1
                continue
            if question in already_down:
                index += 1
                continue

            answer = answer.strip()

            print(f"index: {index}")
            print(f"question: {question}")
            print(f"answer  : {answer}")
            # 获取输入
            # 输入 y：执行清理
            # 输入 h：清理hat
            # 输入 r：跳过当前记录
            # 输入 l: 返回上一个记录

            inputs = input("l(ast)/r(emove): ").strip()
            print(f"inputs: {inputs}")
            if inputs == "r":
                already_down[question] = ''
                index += 1
                continue
            elif inputs == "h":
                answer = remove_hat(question, answer)
            elif inputs == "n":
                answer = remove_2hat(question, answer)
            elif inputs == "y":
                answer = remove_same_part(question, answer)
                answer = remove_fun_words(answer)
            elif inputs == "l":
                index -= 1
                # pop last
                already_down.popitem()
                continue

            else:
                pass
            already_down[question] = answer
            index += 1
    except BaseException as e:
        print(e)
        with open(already_done_path, 'w', encoding='utf-8') as f:
            json.dump(already_down, f, ensure_ascii=False, indent=4)

    with open(already_done_path, 'w', encoding='utf-8') as f:
        json.dump(already_down, f, ensure_ascii=False, indent=4)

    question2answer_list_clean = [{
        "instruction": question,
        "input": "",
        "output": answer
    } for question, answer in already_down.items() if question and answer]

    print(f"End generating data and Clean, num: {len(question2answer_list_clean)}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(question2answer_list_clean, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # data_clean(input_path="../../data/1_doc/hnc_data_1118_stage_3.json",
    #            already_done_path="../../data/1_doc/hnc_data_1118_stage_3_already.json",
    #            output_path="../../data/1_doc/hnc_data_1118_stage_4.json")

    # 数据筛查慢慢搞先导出一个用
    question2answer_list_clean = load_inputs("../../data/1_doc/hnc_data_1118_stage_3.json")
    question2answer_list_clean = [{
        "instruction": question,
        "input": "",
        "output": answer
    } for question, answer in question2answer_list_clean]

    print(f"End generating data and Clean, num: {len(question2answer_list_clean)}")
    with open("../../data/1_doc/hnc_data_1118_stage_3_output.json", 'w', encoding='utf-8') as f:
        json.dump(question2answer_list_clean, f, ensure_ascii=False, indent=4)

    data_analysis(question2answer_list_clean)
    # {50: 359, 100: 863, 150: 569, 200: 340, 250: 195, 300: 106, 350: 48, 400: 30, 450: 13, 500: 7, 550: 3, 600: 1}
