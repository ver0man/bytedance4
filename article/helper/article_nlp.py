from bs4 import BeautifulSoup as bs
from jieba.analyse import *
from rake_nltk import Rake
from textblob import TextBlob


def get_keyword(article, *args, **kwargs):
    """
    Make use of text blob as well. Ref: https://textblob.readthedocs.io/.
    :param article:
    :param args:
    :param kwargs:
    :return:
    """
    soup = bs(article, 'html.parser')
    b = TextBlob(soup.text)
    if b.detect_language() == 'zh-CN':
        return get_keyword_html_chinese(article, *args, **kwargs)
    else:
        return get_keyword_html_english(article, *args, **kwargs)


def get_keyword_html_chinese(article, *args, **kwargs):
    """
    Extract keyword from chinese article in html, with jieba help. Reference: https://github.com/fxsjy/jieba
    :param article: chinese article in html
    :param args:
    :param kwargs: topK, withWeight
    :return: keywords
    """
    withWeight = kwargs['withWeight'] if 'withWeight' in kwargs.keys() else False
    topK = kwargs['topK'] if 'withWeight' in kwargs.keys() else 20

    # 基于 TF-IDF 算法的关键词抽取
    soup = bs(article, 'html.parser')
    keyword = extract_tags(soup.text, topK=topK, withWeight=withWeight)

    # 基于
    # TextRank
    # 算法的关键词抽取
    # jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
    # 直接使用，接口相同，注意默认过滤词性。
    # jieba.analyse.TextRank()
    # 新建自定义
    # TextRank
    # 实例

    return keyword


def get_keyword_html_english(article, *args, **kwargs):
    """

    :param article:
    :param args:
    :param kwargs:
    :return:
    """
    soup = bs(article, 'html.parser')
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the text.
    r.extract_keywords_from_text(soup.text)

    # Extraction given the list of strings where each string is a sentence.
    # r.extract_keywords_from_sentences( < list of sentences >)

    # To get keyword phrases ranked highest to lowest.
    keywords = r.get_ranked_phrases()

    # To get keyword phrases ranked highest to lowest with scores.
    # r.get_ranked_phrases_with_scores()

    return keywords

# nltk.download('stopwords')
# test = 'RAKE short for Rapid Automatic Keyword Extraction algorithm, is a domain independent keyword extraction algorithm which tries to determine key phrases in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text.'
# get_keyword_html_english(test)
