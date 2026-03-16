# 人民网文章词云分析

基于Python的人民网文章爬取与词云可视化项目。

## 📋 项目简介

本项目爬取人民网（people.cn）的文章内容，使用jieba进行中文分词，生成词云图，直观展示文章关键词分布。

## 🎯 功能特性

- **文章爬取**：自动爬取人民网指定页面文章
- **中文分词**：使用jieba进行智能分词
- **关键词提取**：基于TF-IDF算法提取关键词
- **词云生成**：生成美观的词云图
- **停用词过滤**：自动过滤无效词汇

## 🛠️ 技术栈

- **Python 3.12**
- **requests**：HTTP请求
- **BeautifulSoup**：HTML解析
- **jieba**：中文分词
- **wordcloud**：词云生成
- **matplotlib**：数据可视化

## 📦 安装依赖

```bash
pip install requests beautifulsoup4 jieba wordcloud matplotlib
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/wjsv1/people-cn-wordcloud.git
cd people-cn-wordcloud
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行项目

```bash
python crawler.py
```

## 📊 运行结果

程序将生成以下文件：

- `articles.txt`：爬取的文章内容
- `wordcloud.png`：词云图
- `wordcloud_final.png`：高清版词云图

## 🔍 词云示例

本项目爬取了人民网的文章，生成的词云展示了以下关键词：

- **求是**：最高频词
- **金融**：经济相关
- **茶话会**、**新年**：时政活动
- **全国政协**、**特色**：政治特色
- **强国**、**建设**：发展目标

## 📝 代码说明

### 主要函数

#### `crawl_articles(url, headers)`
爬取指定URL的文章内容，返回文章列表。

#### `extract_keywords(text, topK=100)`
使用jieba提取关键词，过滤停用词，返回词频字典。

#### `generate_wordcloud(word_freq, output_file, title)`
生成词云图并保存为图片文件。

### 停用词处理

项目内置了完整的停用词列表，包括：
- 常见虚词：的、了、在、是...
- 特定词汇：来源、人民网、新华社...
- 数字和标点

## 🎨 自定义配置

你可以修改 `crawler.py` 中的以下参数：

```python
# 修改目标URL
url = "http://jhsjk.people.cn/result/1?form=706&else=501"

# 修改提取关键词数量
tags = jieba.analyse.extract_tags(text, topK=100, withWeight=True)

# 修改词云尺寸
wordcloud = WordCloud(
    width=1200,
    height=800,
    max_words=100
)
```

## ⚠️ 注意事项

1. **网络连接**：需要稳定的网络连接访问人民网
2. **反爬机制**：请合理设置请求间隔，避免频繁访问
3. **字体问题**：系统需要安装中文字体才能正常显示中文词云

## 📄 许可证

本项目仅供学习交流使用。

## 👨‍💻 作者

- **作者**：王豪博
- **日期**：2026-03-16

## 🙏 致谢

- [jieba](https://github.com/fxsjy/jieba) - 中文分词库
- [wordcloud](https://github.com/amueller/word_cloud) - 词云生成库
- [人民网](http://www.people.com.cn/) - 数据来源
