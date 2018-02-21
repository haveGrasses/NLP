# coding:utf-8
'''
interpreter:python2.7
segment the words in play text and plot word cloud
'''
import codecs
import jieba
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator


# read the content
def load_text(file_path):
    "return string"
    with codecs.open(file_path, 'r', 'utf-8') as f:
        content = f.read()
        text = content.replace('\r\n', '')
    print text
    return text


# load stopwords
def load_stopwords(stopwords_path):
    "return a set"
    stopwords = set(line.strip() for line in codecs.open('stopwords.txt', encoding='utf-8'))
    print stopwords
    return stopwords


# jieba segmentation
def jieba_cut(text, stopwords, user_dict, add_dict=[]):
    '''
    text: string
    stopwords: list
    add_dict: list, add users' own dictionary
    return: list
    '''
    word_list = []
    if not add_dict == []:
        for item in add_dict:
            jieba.add_word(item)
    jieba.load_userdict(user_dict)
    text_after_list = pseg.cut(text)
    for word, flag in text_after_list:
        # remove stopwords and meaningless ones and only keep noun because nouns often carries more meaning
        if not word.strip() in stopwords and len(word.strip()) > 1 and flag == 'n':
            word_list.append(word)
    return word_list


# begin plotting
def plot_wordcloud(pic_path, file_path, stopwords_path='stopwords.txt',
                   font_path=u'微软雅黑.ttf', color='white'):
    text = load_text(file_path)
    stopwords = load_stopwords(stopwords_path)
    word_list = jieba_cut(text=text, stopwords=stopwords, user_dict='dict.txt')
    plot_content = ' '.join(word_list)
    # set word cloud
    background_pic = imread(pic_path)
    wc = WordCloud(font_path=font_path,
                   background_color=color,  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=background_pic,  # 设置背景图片
                   max_font_size=100,  # 字体最大值
                   random_state=42,
                   # width=1000, height=860, margin=2,
                   )
    wc.generate(plot_content)
    image_colors = ImageColorGenerator(background_pic)  # extract colors from background picture
    plt.imshow(wc)
    plt.axis("off")
    # plot with new color
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    # 绘制背景图片为颜色的图片
    plt.figure()
    plt.imshow(background_pic, cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()
    # save figure
    wc.to_file('word_cloud.png')


if __name__ == "__main__":
    plot_wordcloud(pic_path='bg.jpg', file_path=u'湄公河行动.txt')