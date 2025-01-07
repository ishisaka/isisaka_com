---
date: 2025-01-07 15:29
---

# Sphinx TIPS

## 公式ドキュメント

[Sphinx — Sphinx documentation](https://www.sphinx-doc.org/ja/master/index.html)

### Myst

* [MyST - Markedly Structured Text - Parser](https://myst-parser.readthedocs.io/en/latest/index.html)
* [MyST \- Markedly Structured Text](https://myst-parser.readthedocs.io/en/v0.17.2/index.html)（旧版）
  * [Sphinx-specific page front matter](https://myst-parser.readthedocs.io/en/v0.17.2/sphinx/use.html#sphinx-specific-page-front-matter)

## その他ドキュメント

* [Python製静的サイトジェネレーターSphinxでWebサイトを構築して公開 \| gihyo\.jp](https://gihyo.jp/article/2024/06/monthly-python-2406)

## 拡張

* [Mermaid拡張](https://github.com/mgaitan/sphinxcontrib-mermaid)
* [RSS Feed](https://github.com/lsaffre/sphinxfeed)

### RSS Feed拡張(sphinxfeed)の使い方

1. インストール

```bash
pip install sphinxfeed-lsaffre
```

2. `conf.py`に追加

```python
extensions = [
    'sphinxfeed',
]
...
feed_base_url = 'https://YOUR_HOST_URL'
feed_author = 'YOUR NAME'
feed_description = "A longer description"
# optional options
feed_field_name = 'date'  # default value is "Publish Date"
feed_use_atom = False
use_dirhtml = False
```

3. rstファイルの先頭に以下を追加

```rst
:date: 2025-01-06
```

MystのMarkdown形式の場合は以下のようにファイルの先頭に追加する。

```text
---
date: 2025-01-05
---

```

4. ビルド

```bash
make html
```

注意点としては、`:date`フィールドの値がrss.xmlの日付より未来の場合のみ、rss.xmlに追加されることと対象がrstファイルのみである事。

## HTML TIPS

* [SphinxのHTMLにfaviconを設定する \- nikkie\-memos](https://scrapbox.io/nikkie-memos/Sphinx%E3%81%AEHTML%E3%81%ABfavicon%E3%82%92%E8%A8%AD%E5%AE%9A%E3%81%99%E3%82%8B)

### テーマ

* [Furo](https://sphinx-themes.org/sample-sites/furo/)
