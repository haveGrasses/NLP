# coding:utf-8
import codecs
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
# #####################另一个分析方法:对剧本分词后绘制词云######################

# 读取剧本
with codecs.open(u'湄公河行动.txt', 'r', 'utf-8') as f:
    play_text = f.read()
    play_text = play_text.replace('\r\n', '')
# print play_text
# jieba分词
text_after = ' '.join(jieba.cut(play_text))
# print text_after

# 绘制词云
wordcloud = WordCloud(font_path=u'微软雅黑.ttf', mask=imread('bg.jpg'), background_color='#87CEEB').generate(text_after)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 效果不太好，还有OS,VO这些无关词汇
# 下次尝试提取词频再画