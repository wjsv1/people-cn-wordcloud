#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人民网文章词云生成器
====================
爬取人民网文章，使用jieba分词生成词云图

作者: 王豪博
日期: 2026-03-16
"""

import requests
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


def crawl_articles(url, headers=None):
    """
    爬取人民网文章
    
    Args:
        url: 目标网页URL
        headers: HTTP请求头
        
    Returns:
        list: 文章标题列表
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    print(f"正在爬取: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    
    print(f"状态码: {response.status_code}")
    print(f"内容长度: {len(response.text)} 字符")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取文章标题
    articles = []
    for item in soup.find_all(['a', 'h2', 'h3', 'li']):
        text = item.get_text(strip=True)
        if text and len(text) > 10 and 'http' not in text:
            articles.append(text)
    
    print(f"找到 {len(articles)} 篇文章")
    return articles


def extract_keywords(text, topK=100):
    """
    使用jieba提取关键词
    
    Args:
        text: 文本内容
        topK: 提取关键词数量
        
    Returns:
        dict: 关键词及权重
    """
    # 停用词列表
    stopwords = set([
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', 
        '自己', '这', '那', '这些', '那些', '这个', '那个', '之', '与', '及', '等', '或', 
        '但', '而', '如果', '因为', '所以', '虽然', '但是', '然而', '因此', '于是', '从而', 
        '而且', '并且', '或者', '还是', '要么', '假如', '假定', '譬如', '例如', '比如', 
        '像是', '像', '似的', '似乎', '一样', '一般', '通常', '常常', '经常', '往往', 
        '一直', '总是', '千万', '万一', '一下', '一些', '一点', '一方面', '一直', '一切',
        # 特定停用词
        '来源', '人民网', '人民日报', '新华社', '北京', '日电', '杂志', '发表', '重要', 
        '文章', '推动', '发展', '讲话', '习近平', '总书记'
    ])
    
    # 提取关键词
    tags = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
    
    # 过滤停用词
    word_freq = {}
    for word, weight in tags:
        if word not in stopwords and len(word) > 1 and not word.isdigit():
            word_freq[word] = weight
    
    return word_freq


def generate_wordcloud(word_freq, output_file='wordcloud.png', title='词云图'):
    """
    生成词云图
    
    Args:
        word_freq: 词频字典
        output_file: 输出文件名
        title: 图表标题
    """
    # 生成词云（使用项目中文字体）
    font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')
    wordcloud = WordCloud(
        font_path=font_path,
        width=1200,
        height=800,
        background_color='white',
        max_words=100,
        relative_scaling=0.5,
        colormap='viridis'
    ).generate_from_frequencies(word_freq)
    
    # 保存词云图
    wordcloud.to_file(output_file)
    print(f"✅ 词云图已保存: {output_file}")
    
    # 使用matplotlib保存高质量版本
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=20, pad=20)
    plt.tight_layout()
    
    final_file = output_file.replace('.png', '_final.png')
    plt.savefig(final_file, dpi=300, bbox_inches='tight')
    print(f"✅ 高清版本已保存: {final_file}")
    
    return wordcloud


def main():
    """主函数"""
    # 目标URL
    url = "http://jhsjk.people.cn/result/1?form=706&else=501"
    
    # 1. 爬取文章
    print("=" * 50)
    print("步骤 1: 爬取文章")
    print("=" * 50)
    articles = crawl_articles(url)
    
    # 保存原始文章
    with open('articles.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(articles))
    print(f"✅ 文章已保存到 articles.txt\n")
    
    # 2. 提取关键词
    print("=" * 50)
    print("步骤 2: 提取关键词")
    print("=" * 50)
    text = '\n'.join(articles)
    word_freq = extract_keywords(text)
    print(f"提取到 {len(word_freq)} 个关键词")
    
    # 显示Top 15关键词
    print("\nTop 15 关键词:")
    for i, (word, freq) in enumerate(
        sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15], 1
    ):
        print(f"{i}. {word}: {freq:.4f}")
    print()
    
    # 3. 生成词云
    print("=" * 50)
    print("步骤 3: 生成词云")
    print("=" * 50)
    generate_wordcloud(word_freq, 'wordcloud.png', '人民网文章词云分析')
    
    print("\n" + "=" * 50)
    print("完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
