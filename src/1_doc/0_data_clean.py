import os


def data_clean4each_file(text_list):
    """
    清洗文本
    :param text_list:
    :return:
    """
    clean_sign_list = [
        '华中8型数控系统用户说明书',
        '华中8型数控系统编程说明书',
        '华中8型数控系统参数说明书',
        '华中8型数控系统操作说明书'
    ]
    text = ''
    for line in text_list:
        flag = False
        for sign in clean_sign_list:
            if sign in line:
                flag = True
                break
        if flag:
            continue
        text += line
    return text


def data_clean(inputs_path, output_path):
    """
    获取输入列表
    :param inputs_path
    :param output_path:
    :return:
    """
    file_list = os.listdir(inputs_path)
    for file in file_list:
        file_path = os.path.join(inputs_path, file)
        with open(file_path, "r") as f:
            text_list = f.readlines()
        text = data_clean4each_file(text_list)
        with open(os.path.join(output_path, file), "w") as f:
            f.write(text)


if __name__ == '__main__':
    data_clean("../../data/1_doc/848说明书_txt", "../../data/1_doc/848说明书_txt_clean")
