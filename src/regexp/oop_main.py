from oop_alt import Alt
from oop_any import Any
from oop_end import End
from oop_lit import Lit
from oop_seq import Seq
from oop_start import Start


def main():
    tests = [
        ["a", "a", true, Lit("a")],
        ["b", "a", false, Lit("b")],
        ["a", "ab", true, Lit("a")],
        ["b", "ab", true, Lit("b")],
        ["ab", "ab", true, Seq(Lit("a"), Lit("b"))],
        ["ba", "ab", false, Seq(Lit("b"), Lit("a"))],
        ["ab", "ba", false, Lit("ab")],
        ["^a", "ab", true, Seq(Start(), Lit("a"))],
        ["^b", "ab", false, Seq(Start(), Lit("b"))],
        ["a$", "ab", false, Seq(Lit("a"), End())],
        ["a$", "ba", true, Seq(Lit("a"), End())],
        ["a*", "", true, Any("a")],
        ["a*", "baac", true, Any("a")],
        ["ab*c", "ac", true, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abc", true, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abbbc", true, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abxc", false, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab|cd", "xaby", true, Alt(Lit("ab"), Lit("cd"))],
        ["ab|cd", "acdc", true, Alt(Lit("ab"), Lit("cd"))],
        ["a(b|c)d", "xabdy", true, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))],
        ["a(b|c)d", "xabady", false, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))]
    ]
    for (pattern, text, expected, matcher) in tests:
        actual = matcher.match(text)
        result = "pass" if actual == expected else "fail"
        print(f"'{regexp}' X '{text}' == {actual}: {result}")


if __name__ == "__main__":
    main()
