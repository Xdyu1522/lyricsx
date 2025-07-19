import re
from datetime import timedelta
from typing import List, Tuple, Union

from lyricsx.enhanced_model import EnhancedLyricDocument, EnhancedLyricLine
from lyricsx.model import (
    CombinedLyricLine,
    LRCTime,
    LyricLine,
    LyricMeta,
    StandardLyricDocument,
)


class StandardLRCParser:
    @staticmethod
    def parse(text: str) -> StandardLyricDocument:
        lines: List[LyricLine] = []
        meta: List[LyricMeta] = []

        for line in text.splitlines():
            line = line.strip()

            tag_match = re.match(r"\[([a-zA-Z]{2,3}):([^]]+)]", line)
            if tag_match:
                meta.append(LyricMeta(tag=tag_match.group(1), value=tag_match.group(2)))
                continue

            # 歌词行，如 [00:12.34]Hello
            time_text_match = re.findall(r"\[(\d{2}):(\d{2})\.(\d{1,3})](.*)", line)
            try:
                if len(time_text_match[0]) == 4:
                    minute, sec, msec, text = time_text_match[0]
                    msec = msec.ljust(3, "0")
                    lrc_time = LRCTime(minute, sec, msec)
                    lines.append(LyricLine(lrc_time, text))
            except IndexError:
                pass

        return StandardLyricDocument(lines, meta)

    @staticmethod
    def parse_with_translate(
        origin: str, interval: int = 0, *trans: str
    ) -> StandardLyricDocument:
        parsed_origin: StandardLyricDocument = StandardLRCParser.parse(origin)
        parsed_trans: List[StandardLyricDocument] = [
            StandardLRCParser.parse(t) for t in trans
        ]
        final_lines: List[Union[LyricLine, CombinedLyricLine]] = []

        parsed_origin.lines.sort()
        for t in parsed_trans:
            t.lines.sort()

        for o in parsed_origin.lines:
            available_trans: List[LyricLine] = []

            for t in parsed_trans:
                # available_tran = list(filter(lambda x: abs(x.start_time.total_milliseconds - o.start_time.total_milliseconds) < interval, t.lines))
                available_tran = [
                    x
                    for x in t.lines
                    if abs(x.time.total_milliseconds - o.time.total_milliseconds)
                    <= interval
                ]
                if len(available_tran) > 0:
                    available_trans.append(available_tran[0])

            if not available_trans:
                final_lines.append(CombinedLyricLine(o, LyricLine.empty_line()))
            else:
                final_lines.append(CombinedLyricLine(o, *available_trans))

        final = StandardLyricDocument(final_lines, parsed_origin.meta)
        final.lines.sort()

        return final


class EnhancedLyricParser:
    @staticmethod
    def parse(text: str) -> EnhancedLyricDocument:
        lines: List[EnhancedLyricLine] = []
        meta: List[LyricMeta] = []

        for line in text.splitlines():
            line = line.strip()

            tag_match = re.match(r"\[([a-zA-Z]{2,3}):([^]]+)]", line)
            if tag_match:
                meta.append(LyricMeta(tag=tag_match.group(1), value=tag_match.group(2)))
                continue

            # 歌词行，如 [00:12.34]Hello
            pattern = r"\[(\d{2}):(\d{2})\.(\d{1,3})\]([^\[\]]*)"
            time_text_match = re.findall(pattern, line)
            if time_text_match:
                lines.append(EnhancedLyricLine.from_string(line))

        return EnhancedLyricDocument(lines, meta)

    @staticmethod
    def parse_with_translate():
        pass


if __name__ == "__main__":
    lrc = """
    [ar:Artist Name]
    [ti:Song Title]
    [00:12.34]Hello world
    [00:15.00]This is a test
    """

    doc = StandardLRCParser.parse(lrc)
    print(doc)
