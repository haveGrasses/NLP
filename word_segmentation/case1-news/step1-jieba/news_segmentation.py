# coding:utf-8
import codecs
import jieba

# ######################分词#############################

jieba.load_userdict('dict.txt')  # 添加自定义词典
word_list = []  # 存放file中每行的分词结果
with codecs.open('news.txt', 'r', 'utf-8') as f:
    # file_list = [line.replace('\n', '') for line in f.readlines()]
    for line in f.readlines():
        seg_list = jieba.cut(line.strip())  # jieba.lcut 也可以;strip()是为了去掉后面的换行符，避免将其也当做一个字符
        word_list.append([])
        for word in seg_list:
            word_list[-1].append(word)
# print word_list  # 显示的是文字编码
# print world_list[0][0]  # 显示文字

# #################将分词结果写入文件#########################

with codecs.open('news_seg.txt', 'w', 'utf-8') as f:
    for i in range(len(word_list)):
        for word in word_list[i]:
            f.write(word + ' ')  # 写入的词用空格分隔
        f.write('\n')           # 一条新闻写完另起一行

    # 效果和下面这种写法一样
    # for i in word_list:
    #     for word in word_list[word_list.index(i)]:
    #         f.write(word + ' ')
    #     f.write('\n')
