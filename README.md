# lyricsx

[中文说明（Chinese README）](./README.zh-CN.md)

A Python library for parsing, processing, and manipulating LRC lyrics files.

## Features

- Parse standard and enhanced LRC files
- Support for time-tagged lyrics and metadata
- Lyrics merging, formatting, and conversion
- Easy to extend and integrate

## Installation

```bash
pip install .
```

## Basic Usage

### Parse a single enhanced lyric line
```python
from lyricsx.enhanced_model import EnhancedLyricLine
line = EnhancedLyricLine.from_string("[00:19.845]つ[00:20.084]ま[00:20.286]ら[00:20.501]な[00:20.700]い[00:20.997]な[00:21.685]")
print(line.text)  # print lyric text
```

### Parse a full LRC file
```python
from lyricsx.parser.lrc_parser import EnhancedLyricParser
with open("yourfile.lrc", encoding="utf-8") as f:
    lrc_content = f.read()
doc = EnhancedLyricParser.parse(lrc_content)
print(doc.to_lrc())
```

## Main Classes

- `LRCTime`: LRC time tag class, supports millisecond precision, parsing, formatting, and comparison.
- `LyricLine`: Standard lyric line, contains time and text.
- `CombinedLyricLine`: Representation for merged multi-language or multi-line lyrics.
- `LyricMeta`: Lyric metadata (e.g., title, artist, etc.).
- `StandardLyricDocument`: Standard lyric document, supports LRC output.
- `EnhancedLyricLine`: Enhanced lyric line, supports per-character time tags.
- `EnhancedLyricParser`: Enhanced lyric parser, supports parsing and serializing enhanced LRC files.

## Project Structure

```
lyricsx/
    model.py                # Basic time and lyric line models
    enhanced_model.py       # Enhanced lyric models
    utils.py                # Utility functions
    parser/
        lrc_parser.py       # LRC lyric parser
    tests/                  # Test cases and sample lyrics
```

## License

MIT License

---
For Chinese documentation, see [README.zh-CN.md](./README.zh-CN.md)
