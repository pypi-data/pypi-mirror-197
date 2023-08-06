# **ckip-2-tei**

This project segments the title, body, and comments from a JSON file and writes them to a TEI XML file, and
leverages asynchronous programming to achieve high performance and speed.

## Installation
The source code is currently hosted on GitHub at: https://github.com/Taiwan-Social-Media-Corpus/ckip-2-tei

Binary installers for the latest released version are available at the [Python Package Index (PyPI)](https://pypi.org/project/ckip-2-tei/).

```bash
pip install ckip2tei
```

## Documentation
### 1. Import module
```python
from ckip2tei import generate_tei_xml
```
If you are working on Jupyter Notebook, you need to add two additional code lines beforehand:

```python
import nest_asyncio
nest_asyncio.apply()
```

Since `ckip2tei` is built with Python asynchronous frameworks, it cannot run properly on Jupyter Notebook due to the fact that Jupyter [(IPython ≥ 7.0)](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7) is already running an event loop. Visit [this question](https://stackoverflow.com/questions/56154176/runtimeerror-asyncio-run-cannot-be-called-from-a-running-event-loop-in-spyd) asked in StackOverflow for further details.

### 2. Run pipeline
Provide the function `generate_tei_xml` with two arguments:

- `post_data`: the data to be segmented
- `media`: the source of the data

The `post_data` argument should be in the following format:

```python
{
    "board": "Soft_Job",
    "post_id": "ABCD",
    "date": "1183186255",
    "title": "[請益] 最愛的程式?",
    "author": "Retr0327",
    "body": "這是一篇測試文章\n我喜歡 Python 和 TypeScript",
    "post_vote": {"推 (pos)": 2, "噓 (neg)": 0, "→ (neu)": 0},
    "comments": [
        {
            "type": "pos",
            "author": "Uncle",
            "content": "我愛 TypeScript",
            "order": "1",
        },
        {
            "type": "pos",
            "author": "Bob",
            "content": "我也很愛 Python",
            "order": "2",
        },
    ],
}
```

After filling the arguments, do it as follows:


```python
post_data = {
    "board": "Soft_Job",
    "post_id": "ABCD",
    "date": "1183186255",
    "title": "[請益] 最愛的程式?",
    "author": "Retr0327",
    "body": "這是一篇測試文章\n我喜歡 Python 和 TypeScript",
    "post_vote": {"推 (pos)": 2, "噓 (neg)": 0, "→ (neu)": 0},
    "comments": [
        {
            "type": "pos",
            "author": "Uncle",
            "content": "我愛 TypeScript",
            "order": "1",
        },
        {
            "type": "pos",
            "author": "Bob",
            "content": "我也很愛 Python",
            "order": "2",
        },
    ],
}

generate_tei_xml(post_data, "ptt")
```

This prints:

```xml
<TEI.2>
   <teiHeader>
      <metadata name="media">ptt</metadata>
      <metadata name="author">Retr0327</metadata>
      <metadata name="post_id">ABCD</metadata>
      <metadata name="year">2007</metadata>
      <metadata name="board">Soft_Job</metadata>
      <metadata name="title">[請益] 最愛的程式?</metadata>
   </teiHeader>
   <text>
      <title author="Retr0327">
         <s>
            <w type="PARENTHESISCATEGORY">[</w>
            <w type="VB">請益</w>
            <w type="PARENTHESISCATEGORY">]</w>
            <w type="WHITESPACE"> </w>
            <w type="Dfa">最</w>
            <w type="VL">愛</w>
            <w type="DE">的</w>
            <w type="Na">程式</w>
            <w type="QUESTIONCATEGORY">?</w>
         </s>
      </title>
      <body author="Retr0327">
        ...
   </text>
</TEI.2>
```


## Contact Me
If you have any suggestion or question, please do not hesitate to email me at lixingyang.dev@gmail.com
