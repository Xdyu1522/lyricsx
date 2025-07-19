import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from lyricsx.enhanced_model import EnhancedLyricLine
from lyricsx.parser.lrc_parser import EnhancedLyricParser


def test_enhanced():
    lrc_path = os.path.join(os.path.dirname(__file__), "tests", "YOASOBI - 群青.lrc")
    with open(lrc_path, encoding="utf-8") as f:
        lrc = f.read().split("\n")

    obj = EnhancedLyricLine.from_string(lrc[10])
    assert obj.text == "つまらないな"
    assert obj.start_time.milliseconds == 845
    assert obj.end_time.milliseconds == 685
    assert (
        str(obj)
        == """[00:19.845]つ[00:20.084]ま[00:20.286]ら[00:20.501]な[00:20.700]
        い[00:20.997]な[00:21.685]"""
    )


def test_enhanced_2():
    lrc_path = os.path.join(os.path.dirname(__file__), "tests", "YOASOBI - 群青.lrc")
    with open(lrc_path, encoding="utf-8") as f:
        lrc = f.read()

    obj = EnhancedLyricParser.parse(lrc)
    assert obj.to_lrc() == lrc
