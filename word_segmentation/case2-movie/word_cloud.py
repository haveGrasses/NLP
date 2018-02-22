# coding:utf-8
'''
interpreter:python2.7
segment the words in a file and plot word cloud
'''
import codecs
import jieba
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator


# read the content
def load_text(file_path):
    """
    :param file_path: filename in in the current path
    :return: string
    """
    with codecs.open(file_path, 'r', 'utf-8') as f:
        content = f.read()
        text = content.replace('\r\n', '')
        text = text.replace('\n', '')
    print text
    return text


# load stopwords
def load_stopwords(stopwords_path):
    """
    :param stopwords_path: filename in in the current path
    :return: set
    """
    stopwords = set(line.strip() for line in codecs.open(stopwords_path, 'r', encoding='utf-8'))
    print stopwords
    return stopwords


# jieba segmentation
def jieba_cut(text, stopwords, user_dict, keep_name=True, add_dict=[]):
    """
    :param text: string
    :param stopwords: list
    :param user_dict: add user_dict
    :param keep_name: bool, keep name in the text or not
    :param add_dict: list, add users' own dictionary
    :return: list
    """
    word_list = []
    if not add_dict == []:
        for item in add_dict:
            jieba.add_word(item)
    jieba.load_userdict(user_dict)
    text_after_list = pseg.cut(text)
    # for word, flag in text_after_list:  # ???:add these two lines wil cause error
    #     print '%s %s' % (word, flag)
    for word, flag in text_after_list:
        # remove stopwords and meaningless ones and only keep noun because nouns often carries more meaning
        if keep_name:
            if (not word.strip() in stopwords) and len(word.strip()) > 1 and (
                    flag == 'n' or flag == 'x' or flag == 'nr'):
                word_list.append(word)
                print word
        else:
            if (not word.strip() in stopwords) and len(word.strip()) > 1 and flag == 'n':
                word_list.append(word)
                print word
    return word_list


# begin plotting
def plot_wordcloud(pic_path, file_path, stopwords_path='stopwords.txt', keep_name=True,
                   font_path=u'微软雅黑.ttf', color='grey', max_words=2000, save_name=''):
    """
    :param pic_path: picture name
    :param file_path: file name
    :param stopwords_path: file name
    :param keep_name: bool, whether keep name in jieba_cut()
    :param font_path: font name
    :param color: background color
    :param max_words: max words to show
    :param save_name: picture name
    :return: none
    """

    text = load_text(file_path)
    stopwords = load_stopwords(stopwords_path)
    if keep_name:  # ???: need to find a easier way
        word_list = jieba_cut(text=text, stopwords=stopwords, keep_name=True, user_dict='dict.txt')
    else:
        word_list = jieba_cut(text=text, stopwords=stopwords, keep_name=False, user_dict='dict.txt')
    plot_content = ' '.join(word_list)
    # set word cloud
    background_pic = imread(pic_path)
    wc = WordCloud(font_path=font_path,
                   background_color=color,  # background color
                   max_words=max_words,
                   mask=background_pic,  # background pic
                   max_font_size=100,
                   random_state=42,
                   # width=1000, height=860, margin=2,
                   )
    wc.generate(plot_content)
    image_colors = ImageColorGenerator(background_pic)  # extract colors from background picture
    plt.imshow(wc)
    plt.axis("off")
    # plot in new color
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    # show bg pic
    # plt.figure()
    # plt.imshow(background_pic, cmap=plt.cm.gray)
    # plt.axis("off")
    # save figure
    if not save_name:
        if keep_name:
            save_name = 'wc_name.png'
        else:
            save_name = 'wc_content.png'
        wc.to_file(save_name)
    else:
        save_name = save_name
        wc.to_file(save_name)
    plt.show()


if __name__ == "__main__":
    plot_wordcloud(pic_path='sun.jpg', file_path=u'湄公河行动.txt', max_words=200, keep_name=False)

