"""
Copyright 2022, University of Freiburg
Chair of Algorithms and Data Structures.
Sebastian Walter <swalter@cs.uni-freiburg.de>
"""

import unicodedata
from helper import edit_distance

# In the lecture we learned that standard Python strings (since Python3) are unicode strings.
# However, they sometimes can behave unintuitively when dealing with unicode
# in practice. The reason is that one (visual) character can be
# represented by multiple combinations of unicode code points. A sequence of
# code points mapping to a (visual) character is called grapheme cluster. They
# are important e.g. for text editors, because we only want the user to be able
# to move the cursor at grapheme cluster boundaries.

# Some examples:
TEST_0 = "नमस्ते"
TEST_1 = "Ç"
TEST_2 = "Ç"


def unicode():
    # Exotic characters are often only representable by a combination of multiple
    # unicode code points. In TEST_0 the last two characters actually consist of two
    # code points each. This results in Python returning a length of 6 for TEST_0 while
    # one would expect 4. When encoded into utf-8, all 6 code points require 3 bytes.
    print(f"'{TEST_0}' contains {len(TEST_0)} code points, "
          f"requiring {', '.join(str(len(c.encode('utf8'))) for c in TEST_0)} "
          f"bytes in utf-8 respectively:\n{list(TEST_0)}")

    # Unicode normalization (see https://unicode.org/reports/tr15/) with NFKC or NFC
    # tries to combine multiple code points into a single one if possible.
    # In case of TEST_0 normalization does not work (we still get the same 6 code points).
    # In Python unicode normalization is provided by the built in unicodedata package.
    norm = unicodedata.normalize("NFKC", TEST_0)
    assert norm == TEST_0

    # TEST_1 and TEST_2 seem like the same two characters for us humans,
    # but they are different under the hood:
    # TEST_1 contains two unicode code points, with 1 and 2 byte-long representations in utf-8 encoding.
    print(f"'{TEST_1}' contains {len(TEST_1)} code points, "
          f"requiring {' and '.join(str(len(c.encode('utf8'))) for c in TEST_1)} "
          f"bytes in utf-8 respectively:\n{list(TEST_1)}")
    # TEST_2 contains a single unicode code point, with a 2 byte-long representation in utf-8.
    print(f"'{TEST_2}' contains {len(TEST_2)} code point "
          f"with a {len(TEST_2[0].encode('utf8'))} byte-long utf-8 "
          f"representation:\n{list(TEST_2)}")
    # This is problematic, because e.g. a naive edit distance implementation with
    # inputs TEST_1 and TEST_2 would return an edit distance of 2, even though they are
    # visually the same.
    # Be aware of such things when using third-party packages like 'editdistance'.
    ed = edit_distance(TEST_1, TEST_2)
    assert ed == 2
    print(f"Edit distance between '{TEST_1}' and '{TEST_2}':\n{ed}")

    # However, this time we can use normalization to
    # merge the code points of TEST_1 into a single one, such that it is
    # now equivalent to TEST_2.
    norm = unicodedata.normalize("NFKC", TEST_1)
    assert (len(norm) == 1 and len(norm) == len(TEST_2))
    assert (ord(norm[0]) == ord(TEST_2[0]))
    # Computing the edit distance between TEST_2 and normalized(TEST_1)
    # returns the expected distance of 0.
    ed = edit_distance(norm, TEST_2)
    assert ed == 0
    print(f"Edit distance between normalize('{TEST_1}') and '{TEST_2}':\n{ed}")


if __name__ == "__main__":
    unicode()
