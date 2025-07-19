from lyricsx.parser import StandardLRCParser


def a():
    with open(
        "./tests/ピノキオピー,鏡音リン,初音ミク - ねぇねぇねぇ。-o.lrc",
        encoding="utf-8",
    ) as f:
        origin = f.read()
    with open(
        "./tests/ピノキオピー,鏡音リン,初音ミク - ねぇねぇねぇ。-t.lrc",
        encoding="utf-8",
    ) as f:
        trans = f.read()
    parsed = StandardLRCParser.parse_with_translate(origin, 0, trans)
    print(parsed.to_lrc())


if __name__ == "__main__":
    a()
