# coding: utf-8
"""
interpreter: python2.7
use the comments of books from douban to plot word cloud
"""
from os import path
from word_cloud import *
comment_path = 'F:/python/crawler/Python3/myscrapy/exer/Spider/book_comment'

with codecs.open(path.join(comment_path, 'book_douban.txt'), 'r', encoding='utf-8') as f:
    # remove header, only get the book_name in the txt file
    book_info = [info.strip() for info in f.readlines()[1:]]
    book_name_list = [info.split(' ')[0] for info in book_info if info.split(' ')[0] != '']
    print(book_name_list)

file_list = ['comments_of_%s.txt' % book_name for book_name in book_name_list[:6]]
for f in file_list:
    index = file_list.index(f)
    save_name_list = ['%s.png'% book_name for book_name in book_name_list[:6]]
    plot_wordcloud(pic_path='sun.jpg', file_path=path.join(comment_path, f), max_words=200, keep_name=True,
                   save_name=save_name_list[index])


