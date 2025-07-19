from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import timedelta
from functools import total_ordering
from typing import List, Union


@total_ordering
class LRCTime:
    def __init__(self, minutes: str, seconds: str, milliseconds: str) -> None:
        """
        Initialize an LRCTime object from string-based start_time parts.

        Args:
            minutes (str): The minute part of the LRC timestamp, e.g. "00"
            seconds (str): The second part of the LRC timestamp, e.g. "12"
            milliseconds (str): The millisecond part, can be 1–3 digits,
            e.g. "3" → "300"

        Raises:
            ValueError: If any of the start_time components are invalid or out of range
            TypeError: If any of the parameters are not strings
        """
        # Type checking
        if not all(isinstance(x, str) for x in (minutes, seconds, milliseconds)):
            raise TypeError("All start_time components must be strings")

        # Format validation
        if not all(x.isdigit() for x in (minutes, seconds, milliseconds)):
            raise ValueError("Time components must contain only digits")

        # Convert to integers with validation
        try:
            min_val = int(minutes)
            sec_val = int(seconds)
            ms_val = int(milliseconds.ljust(3, "0"))  # pad to 3 digits
        except ValueError as e:
            raise ValueError(
                f"Failed to convert start_time components to integers: {e}"
            )

        # Range validation
        if min_val < 0:
            raise ValueError("Minutes cannot be negative")
        if not (0 <= sec_val <= 59):
            raise ValueError("Seconds must be between 0 and 59")
        if not (0 <= ms_val <= 999):
            raise ValueError("Milliseconds must be between 0 and 999")

        # Create the start_time object
        self.time = timedelta(minutes=min_val, seconds=sec_val, milliseconds=ms_val)

    @classmethod
    def from_total_milliseconds(cls, milliseconds: int):
        minutes = milliseconds // 60000
        seconds = (milliseconds % 60000) // 1000
        milliseconds_val = milliseconds % 1000
        return cls(f"{minutes:02d}", f"{seconds:02d}", f"{milliseconds_val:03d}")

    @property
    def milliseconds(self) -> int:
        """
        Get the millisecond component (0–999) as it would appear in the LRC tag.

        For example:
            [00:12.340] → returns 340

        Returns:
            int: Millisecond portion of the start_time.
        """
        return self.total_milliseconds % 1000

    @property
    def seconds(self) -> int:
        """
        Get the second component (0–59) as it would appear in the LRC tag.

        For example:
            [00:12.340] → returns 12

        Returns:
            int: Second portion of the start_time.
        """
        return (self.total_milliseconds // 1000) % 60

    @property
    def minutes(self) -> int:
        """
        Get the minute component (0–...) as it would appear in the LRC tag.

        For example:
            [00:12.340] → returns 0

        Returns:
            int: Minute portion of the start_time.
        """
        return self.total_milliseconds // 60000

    @property
    def total_milliseconds(self) -> int:
        """
        Get the total start_time represented by this LRC timestamp in milliseconds.

        For example:
            [00:12.340] → returns 12340

        Returns:
            int: Total milliseconds since 0:00.000
        """
        return round(self.time.total_seconds() * 1000)

    def __str__(self) -> str:
        """
        Return the LRC-formatted start_time string.

        Returns:
            str: Formatted as [MM:SS.mmm], e.g. "00:12.340"
        """
        return f"{self.minutes:02}:{self.seconds:02}.{self.milliseconds:03}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LRCTime):
            return NotImplemented
        return self.time == other.time

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LRCTime):
            return NotImplemented
        return self.time < other.time


@total_ordering
class LyricLine:
    def __init__(self, time: LRCTime, texts: str) -> None:
        self.time = time
        self.texts = texts

    def __str__(self) -> str:
        return f"[{self.time}]{self.texts}"

    def __lt__(self, other: object):
        if not isinstance(other, LyricLine):
            return NotImplemented
        return self.time < other.time

    def __eq__(self, other: object):
        if not isinstance(other, LyricLine):
            return NotImplemented
        return self.time == other.time

    @classmethod
    def empty_line(cls) -> "LyricLine":
        return cls(LRCTime("00", "00", "000"), "")


@total_ordering
class CombinedLyricLine:
    def __init__(self, origin: LyricLine, *trans: LyricLine) -> None:
        self.origin: LyricLine = origin
        self.time: LRCTime = origin.time
        self.trans: List[LyricLine] = []

        for t in trans:
            copy_line = deepcopy(t)
            copy_line.time = self.time
            self.trans.append(copy_line)

    def __str__(self) -> str:
        if self.origin.texts == "":
            return f"[{self.time}]{self.origin.texts}"
        else:
            lyrics: List[str] = [str(self.origin)]
            lyrics.extend(str(t) for t in self.trans if t.texts != "")
            return "\n".join(lyrics)

    def __lt__(self, other) -> bool:
        if not isinstance(other, CombinedLyricLine):
            return NotImplemented
        return self.time < other.time

    def __eq__(self, other) -> bool:
        if not isinstance(other, CombinedLyricLine):
            return NotImplemented
        return self.time == other.time


class LyricMeta:
    def __init__(self, tag: str, value: str) -> None:
        if not tag or not value:
            raise ValueError("Tag and value cannot be empty.")
        self.tag: str = tag
        self.value: str = value

    def __str__(self) -> str:
        return f"[{self.tag}:{self.value}]"


class BaseLyricDocument(ABC):
    @abstractmethod
    def to_lrc(self) -> str:
        pass


class StandardLyricDocument(BaseLyricDocument):
    def __init__(
        self, lines: List[Union[CombinedLyricLine, LyricLine]], meta: List[LyricMeta]
    ) -> None:
        self.lines = lines
        self.meta = meta

    def to_lrc(self) -> str:
        lyrics: List[str] = []

        lyrics.extend(str(m) for m in self.meta)
        lyrics.extend(str(t) for t in self.lines)

        return "\n".join(lyrics)

    def to_json(self) -> str:
        pass

    def to_play_list(self):
        pass
