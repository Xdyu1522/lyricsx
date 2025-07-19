# lyricsx

[English README](./README.md)

一个用于解析、处理和操作 LRC 歌词文件的 Python 库。

## 功能

- 支持标准与增强型 LRC 歌词解析
- 支持带时间标签的歌词与元数据
- 歌词合并、格式化与转换
- 易于扩展和集成

## 安装

```bash
pip install .
```

## 基本用法

### 解析单行增强型歌词
```python
from lyricsx.enhanced_model import EnhancedLyricLine
line = EnhancedLyricLine.from_string("[00:19.845]つ[00:20.084]ま[00:20.286]ら[00:20.501]な[00:20.700]い[00:20.997]な[00:21.685]")
print(line.text)  # 输出歌词文本
```

### 解析完整 LRC 文件
```python
from lyricsx.parser.lrc_parser import EnhancedLyricParser
with open("yourfile.lrc", encoding="utf-8") as f:
    lrc_content = f.read()
doc = EnhancedLyricParser.parse(lrc_content)
print(doc.to_lrc())
```

## 主要类说明

- `LRCTime`：LRC 时间标签类，支持毫秒级精度，负责时间的解析、格式化与比较。
- `LyricLine`：标准歌词行，包含时间和文本。
- `CombinedLyricLine`：多语言或多行歌词的合并表示。
- `LyricMeta`：歌词元数据（如标题、艺术家等）。
- `StandardLyricDocument`：标准歌词文档，支持 LRC 格式输出。
- `EnhancedLyricLine`：增强型歌词行，支持逐字时间标签。
- `EnhancedLyricParser`：增强型歌词解析器，支持解析和序列化增强型 LRC 文件。

## 项目结构

```
lyricsx/
    model.py                # 基础时间与歌词行模型
    enhanced_model.py       # 增强型歌词模型
    utils.py                # 工具函数
    parser/
        lrc_parser.py       # LRC 歌词解析器
    tests/                  # 测试用例与样例歌词
```

## 许可证

MIT License

---
如需英文文档，请参见 [README.md](./README.md)
