from lyricsx.parser import StandardLRCParser


def test_normal_parser1():
    with open("./tests/ChiliChill - 衡山路宛平路.lrc", encoding="utf-8") as f:
        lrc = f.read()
    doc = StandardLRCParser.parse(lrc)
    assert doc.lines[12].texts == ""
    assert doc.lines[13].time.milliseconds == 363


def test_normal_parser2():
    with open(
        "./tests/ピノキオピー,鏡音リン,初音ミク - ねぇねぇねぇ。-o.lrc",
        encoding="utf-8",
    ) as f:
        lrc = f.read()
    doc = StandardLRCParser.parse(lrc)
    assert doc.lines[12].texts == "目が合わないけど"
