# -*-  coding: utf-8 -*-
"""this is a file using jieba to segment chinese word in a movie and
analyse the relations between the figures in this movie"""
import jieba
import codecs
import networkx as nx
from matplotlib import pyplot as plt


def plot_relation(node_file, relations, save_name='network.png', colors_file='colors.txt'):
    """
    plot network picture
    :param node_file: a txt file that contains all nodes need to be plot, one line one node
    :param relations: a dict, format:{node1, node2, weight}
    :param save_name: result picture name
    :param colors_file: colors
    :return: a picture
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    with codecs.open(node_file, 'r', encoding='utf-8') as f:
        # 载入字典时总是会在其实位置读入一个空字符，用isspace()去掉
        node_list = [node.strip() for node in f.readlines() if not node.isspace()]
        print 'node_list:', node_list
        DG = nx.DiGraph()  # 产生一个有向图对象
        DG.add_nodes_from(node_list)  # 添加节点
        node_num = len(node_list)
        for node1 in node_list:
            for node2 in node_list:
                if node1 == node2:
                    continue
                else:
                    try:
                        weight = relations[node1][node2]
                        for i in range(weight):  # weight越大，添加边的次数越多 边越粗，一次反应权重大小
                            DG.add_edge(node1.strip(), node2.strip())
                    except KeyError:  # 会出现处在两个节点没有关系的情况
                        continue
        with codecs.open(colors_file, 'r', encoding='utf-8') as cf:
            colors_list = [c.strip() for c in cf.readlines()]
            print colors_list
            import random  # import random至于顶部会出错
            colors = random.sample(colors_list, node_num)
        nx.draw(DG, with_labels=True, node_size=900, node_color=colors)
        plt.savefig(save_name)
        plt.show()


if __name__ == '__main__':
    relations = {}
    name_freq = {}
    para_names = []
    """
    relation是一个字典，键为人名，值为一个字典，键为人名，值为两个人名的关系强度
    name_freq是一个字典，存放人名出现的频次
    para_name是一个列表，嵌套列表，存放每段内出现过的人物 para是paragraph的简写
    """
    # #############读入人名字典################

    jieba.load_userdict('dict.txt')
    with codecs.open('dict.txt', 'r', 'utf-8') as f:
        names = [name.strip() for name in f.readlines()]
        print 'names:\n', names

    # #################读入剧本#################

    with codecs.open(u'湄公河行动.txt', 'r', 'utf-8') as f:
        movie_contents = f.read()
        movie_contents = movie_contents.replace('(VO)', '')  # 预处理
        movie_contents = movie_contents.replace('(OS)', '')
        print movie_contents
        movie_para_list = movie_contents.split('\n\r')  # 以空行为分隔，拆分出每段内容，存入list
        # for i in range(len(movie_para_list)):
        #     print movie_para_list[i]
        #     print('#####################')
    # ###########分词和统计人名出现次数##########
    """
    思路：
    1.循环剧本的每一段，对其做分词
    2.如果是人名，存入name_in_para相应段落对应的list中
    3.之后再次出现的人名，更新他们在name_freq中的出现次数。
    """

    for para in movie_para_list:
        para_names.append([])  # 为该段增加一个list存放该段出现的人名
        para_words = jieba.cut(para)  # 对每段进行分词
        for word in para_words:
            if word in names:
                para_names[-1].append(word)
                if name_freq.get(word) is None:
                    name_freq[word] = 1  # 待商榷！ 两个if是嵌套的关系，如果在name_freq里面没有，则这是第一出现，次数设为1
                    # 设置relation字典的键对应的初始值，一个待填充的空列表
                    relations[word] = {}  # 在条件为none的情况下执行，即只有当该人名是第一次出现时(name_freq中没有该名字)才添加该键，也避免了重复键
                else:
                    name_freq[word] += 1  # 如果再name_freq里已经有，则次数加1

    # 有些段落一个人名都没有出现，在第33行para_names.append([])中也添加了一个list
    # 所以要将para_names中的空list去掉
    for para_list in para_names:
        if not para_list:
            para_names.remove(para_list)
    print 'para_names:\n', para_names

    # ################计算人物关系###################

    """对于在para_names中的人名，统计他们两两共同出现的次数，将结果计入relations中
    relations的键是一个人名，值是又一个字典，该字典的键是与relations的键有关的人名，值是两者的关联程度
    关联程度的衡量：一起在某段出现的次数，一起出现的频次越高，关联越强
    """
    for name in para_names:  # name是每段中出现的所有人名的list
        for name1 in name:
            for name2 in name:  # 两个for是表示在name这个list中的任意两个人名
                if name1 == name2:  # 因为name这个list是将在该段出现的人名都append进来，所以肯定会有重复
                    continue        # 若重复，则继续下一次循环
                # 对于不同的两个人名，在relations字典中写入他们共同出现的频次
                # 如果之前没有一起出现过，则频次为1，否则在之前的基础上加1
                elif relations[name1].get(name2) is None:
                    relations[name1][name2] = 1
                else:
                    relations[name1][name2] += 1
    print 'relations:\n', relations

    # #####################写入文件#################

    with codecs.open('relations.txt', "a+", "utf-8") as f:
        f.write("Source Target Weight\r\n")
        f.write('\n')
        for name, edges in relations.items():
            for v, w in relations[name].items():
                if w > 3:
                    f.write(name + " " + v + " " + str(w) + '\r\n')
                    f.write('\n')

    # ######################可视化#####################
    plot_relation('dict.txt', relations)














