from __future__ import annotations

from copy import deepcopy

from .model import LRCTime, BaseLyricDocument, CombinedLyricLine, LyricMeta, LyricLine
from functools import total_ordering
import re
from typing import Optional, List, Iterator, Tuple, Union


@total_ordering
class TimedCharacter:
    """带时间戳的单个字符 - 基本单位类"""

    def __init__(self, time: LRCTime, character: str):
        self.time = time
        self.character = character

    @classmethod
    def standard_parse(
        cls, minutes: str, seconds: str, milliseconds: str, character: str
    ) -> "TimedCharacter":
        """从字符串解析，如 '[00:28.961]本'"""
        current_time: LRCTime = LRCTime(minutes, seconds, milliseconds)
        return cls(current_time, character)

    def is_whitespace(self) -> bool:
        """判断是否为空白字符"""
        return self.character.isspace()

    def is_empty(self) -> bool:
        """判断是否为空字符"""
        return self.character == ""

    def __str__(self) -> str:
        return f"[{self.time}]{self.character}"

    def __repr__(self) -> str:
        return f"TimedCharacter(time={self.time}, character='{self.character}')"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TimedCharacter):
            return NotImplemented
        return self.time < other.time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimedCharacter):
            return NotImplemented
        return self.time == other.time and self.character == other.character


@total_ordering
class EnhancedLyricLine:
    """歌词行，包含多个带时间戳的字符"""

    def __init__(self, characters: Optional[List[TimedCharacter]] = None):
        self.characters = characters or []
        self._end_time_override: Optional[LRCTime] = None  # 用于存储覆写的结束时间

    def add_character(self, character: TimedCharacter) -> None:
        """添加字符到行中"""
        self.characters.append(character)

    def extend_characters(self, characters: List[TimedCharacter]) -> None:
        """批量添加字符"""
        self.characters.extend(characters)

    @property
    def start_time(self) -> Optional[LRCTime]:
        """行开始时间（第一个字符的时间）"""
        if not self.characters:
            return None
        return self.characters[0].time

    @property
    def end_time(self) -> Optional[LRCTime]:
        """行结束时间（优先使用覆写时间，否则使用最后一个字符的时间）"""
        if self._end_time_override:
            return self._end_time_override
        if not self.characters:
            return None
        return self.characters[-1].time

    def set_end_time_override(self, end_time: LRCTime) -> None:
        """设置覆写的结束时间"""
        self._end_time_override = end_time

    def clear_end_time_override(self) -> None:
        """清除覆写的结束时间"""
        self._end_time_override = None

    @property
    def text(self) -> str:
        """获取完整行文本"""
        return "".join(char.character for char in self.characters)

    @property
    def text_without_whitespace(self) -> str:
        """获取去除空白字符的文本"""
        return "".join(
            char.character for char in self.characters if not char.is_whitespace()
        )

    def get_character_at_time(self, time: LRCTime) -> Optional[TimedCharacter]:
        """获取指定时间应该显示的字符"""
        current_char = None
        for char in self.characters:
            if char.time <= time:
                current_char = char
            else:
                break
        return current_char

    def get_characters_in_range(
        self, start_time: LRCTime, end_time: LRCTime
    ) -> List[TimedCharacter]:
        """获取时间范围内的所有字符"""
        return [char for char in self.characters if start_time <= char.time <= end_time]

    def split_by_whitespace(self) -> List[List[TimedCharacter]]:
        """按空白字符分割成词语组"""
        words = []
        current_word = []

        for char in self.characters:
            if char.is_whitespace() or char.is_empty():
                if current_word:
                    words.append(current_word)
                    current_word = []
            else:
                current_word.append(char)

        if current_word:
            words.append(current_word)

        return words

    def sort_characters(self) -> None:
        """按时间排序字符"""
        self.characters.sort()

    def is_empty(self) -> bool:
        """判断是否为空行"""
        return len(self.characters) == 0 or all(
            char.is_empty() for char in self.characters
        )

    def __str__(self) -> str:
        return "".join(str(char) for char in self.characters)

    def __repr__(self) -> str:
        return f"EnhancedLyricLine(characters={len(self.characters)}, text='{self.text[:20]}...')"

    def __len__(self) -> int:
        return len(self.characters)

    def __iter__(self) -> Iterator[TimedCharacter]:
        return iter(self.characters)

    def __getitem__(self, index: int | slice) -> TimedCharacter | List[TimedCharacter]:
        return self.characters[index]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, EnhancedLyricLine):
            return NotImplemented
        self_time = self.start_time
        other_time = other.start_time
        if self_time is None:
            return False
        if other_time is None:
            return True
        return self_time < other_time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnhancedLyricLine):
            return NotImplemented
        return self.start_time == other.start_time

    @classmethod
    def from_string(cls, line_str: str) -> "EnhancedLyricLine":
        """从字符串解析歌词行"""
        pattern = r"\[(\d{2}):(\d{2})\.(\d{1,3})\]([^\[\]]*)"
        matches: List[Tuple[str, str, str, str]] = re.findall(pattern, line_str)

        characters = []
        for minutes, seconds, milliseconds, char in matches:
            characters.append(
                TimedCharacter.standard_parse(minutes, seconds, milliseconds, char)
            )

        return cls(characters)

    @classmethod
    def empty_line(cls) -> "EnhancedLyricLine":
        """创建空行"""
        return cls([])

@total_ordering
class EnhancedCombinedLyricLine:
    def __init__(self, origin: EnhancedLyricLine, *trans: LyricLine) -> None:
        self.origin: EnhancedLyricLine = origin
        self.start_time: LRCTime = origin.start_time
        self.end_time: LRCTime = origin.end_time
        self.trans: List[LyricLine] = []

        for t in trans:
            copy_line = deepcopy(t)
            copy_line.time = self.start_time
            self.trans.append(copy_line)

    def __str__(self) -> str:
        if self.origin.text == "":
            return f"[{self.start_time}]{self.origin.text}"
        else:
            lyrics: List[str] = [str(self.origin)]
            lyrics.extend(str(t) for t in self.trans if t.texts != "")
            return "\n".join(lyrics)

    def __lt__(self, other) -> bool:
        if not isinstance(other, CombinedLyricLine):
            return NotImplemented
        return self.start_time < other.time

    def __eq__(self, other) -> bool:
        if not isinstance(other, CombinedLyricLine):
            return NotImplemented
        return self.start_time == other.time


class EnhancedLyricDocument(BaseLyricDocument):
    def __init__(self, lines:List[Union[EnhancedLyricLine, CombinedLyricLine]], meta: List[LyricMeta]):
        self.lines: List[Union[EnhancedLyricLine, CombinedLyricLine]] = lines
        self.meta: List[LyricMeta] = meta

    def to_lrc(self) -> str:
        lyrics: List[str] = []

        lyrics.extend(str(m) for m in self.meta)
        lyrics.extend(str(t) for t in self.lines)

        return "\n".join(lyrics)

    def to_standard_lrc(self) -> str:
        pass
