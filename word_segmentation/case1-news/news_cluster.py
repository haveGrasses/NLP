# coding:utf-8
"""
interpreter: python3.5
"""
import codecs
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


def k_means(after_cut_file, cluster_upper_limit=5, save_name='kmeans_result.png',
            stopwords_path='F:/python/machine learning/NLP/word_segmentation/case2-movie/stopwords.txt'):
    # 求tfidf
    # 构建语料文档列表，一个元素为一行文档
    corpus = [line.strip() for line in open(after_cut_file, 'r', encoding='utf-8').readlines()]
    print('corpus:', corpus)
    stopwords = [stopword.strip() for stopword in open(stopwords_path, 'r', encoding='utf-8').readlines()]
    count_vec = TfidfVectorizer(binary=False, decode_error='ignore', stop_words=stopwords)
    tfidf = count_vec.fit_transform(corpus)
    word = count_vec.get_feature_names()
    weight = tfidf.toarray()
    with open('ti-idf_result.txt', 'w', encoding='utf-8') as f:
        for j in range(len(word)):
            f.write(word[j] + ' ')
        f.write('\r\n')
        for i in range(len(weight)):
            for j in range(len(word)):
                f.write(str(weight[i][j]) + ' ')
            f.write('\r\n')

    # start k-means
    # find best center numbers
    inertia = {}  # put center_nums and corresponding inertia
    for center_num in range(1, cluster_upper_limit):
        clf = KMeans(n_clusters=center_num)
        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        s = clf.fit(weight)
        inertia[center_num] = clf.inertia_
        print('inertia:', clf.inertia_)
    # 返回排序后的字典，以此决定最佳的聚类个数
    inertia_list = list(inertia.items())
    inertia_list.sort(key=lambda x: x[1])
    best_center_nums = inertia_list[0]
    if best_center_nums[0] == 1:
        best_center_nums = inertia_list[1]
    print(best_center_nums)
    # for compare
    for center_num in range(len(inertia_list)):
        print(inertia_list[center_num])
    # true k-means
    clf = KMeans(n_clusters=best_center_nums[0])
    s = clf.fit(weight)
    print('centers:', clf.cluster_centers_)
    print('labels:', clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        i = i + 1

    # plotting
    # 降维
    pca = PCA(n_components=2)  # 输出二维
    new_data = pca.fit_transform(weight)  # 载入n维数据
    print('new_data:', new_data)
    # for i in range(best_center_nums[0]):

    # 第1类
    x0 = []
    y0 = []
    # 第2类
    x1 = []
    y1 = []
    # 第3类
    x2 = []
    y2 = []
    # 第4类
    x3 = []
    y3 = []
    for i in range(len(clf.labels_)):
        if clf.labels_[i] == 1:
            x1.append(new_data[i][0])
            y1.append(new_data[i][1])
        elif clf.labels_[i] == 0:
            x0.append(new_data[i][0])
            y0.append(new_data[i][1])
        elif clf.labels_[i] == 2:
            x2.append(new_data[i][0])
            y2.append(new_data[i][1])
        else:
            x3.append(new_data[i][0])
            y3.append(new_data[i][1])
    plt.plot(x1, y1, '+r')
    plt.plot(x2, y2, '+g')
    plt.plot(x3, y3, '+k')
    plt.plot(x0, y0, '+b')
    plt.savefig(save_name)
    plt.show()


# ######################分词#############################

jieba.load_userdict('dict.txt')  # 添加自定义词典
word_list = []  # 存放file中每行的分词结果
with open('news.txt', 'r', encoding='utf-8') as f:
    # file_list = [line.replace('\n', '') for line in f.readlines()]
    for line in f.readlines():
        seg_list = jieba.cut(line.strip())  # jieba.lcut 也可以;strip()是为了去掉后面的换行符，避免将其也当做一个字符
        word_list.append([])
        for word in seg_list:
            word_list[-1].append(word)
# print word_list  # 显示的是文字编码
# print world_list[0][0]  # 显示文字

# #################将分词结果写入文件#########################

with open('news_seg.txt', 'w', encoding='utf-8') as f:
    for i in range(len(word_list)):
        for word in word_list[i]:
            f.write(word + ' ')  # 写入的词用空格分隔
        f.write('\n')           # 一条新闻写完另起一行

    # 效果和下面这种写法一样
    # for i in word_list:
    #     for word in word_list[word_list.index(i)]:
    #         f.write(word + ' ')
    #     f.write('\n')

# ######################聚类分析###########################
k_means('news_seg.txt', 4)


