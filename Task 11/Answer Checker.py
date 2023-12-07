#
# Copyright 2021 McAfee, LLC
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import hashlib

answer_hashes = {
    234477946232473599274174012364356848169: "Well done, those are the right answers for Challenge 1!",
    220295206644943406791765746444313403020: "Well done, those are the right answers for Challenge 2!",
    9708157056665334647321382212033920597: "Well done, those are the right answers for Challenge 3!",
    312524006896530783592800948131586876503: " That was the demo code, now go find the answers! :-)  "
}


def sort_file_ids(chars):
    assert len(chars) % 4 == 0
    chunks = []
    for i in range(0, len(chars), 4):
        chunks.append(chars[i: i + 4])
    return "".join(sorted(chunks))


def normalise(chars: str) -> str:
    chars = chars.strip()
    chars = chars.upper()
    # Replacements in case of typos:
    chars = chars.replace("O", "0")  # There no Os so assume they meant 0.
    chars = chars.replace("L", "1")  # There no Ls so assume they meant mistook 1 for lowercase L.
    chars = chars.replace("S", "5")  # There no Ss so assume they meant mistook 5 for lowercase S.
    chars_to_remove = [" ", "\n", "\t", "\r", ".", "T", "X"]
    for c in chars_to_remove:
        chars = chars.replace(c, "")
    return chars


def main():
    print("                   -- Answer Checker --")
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n"
          "# Enter the 4-character codes of the files you've found.  #\n"
          "# eg. 'AB12' and 'CD34' becomes 'AB12 CD34'               #\n"
          "# (don't worry about the order of the codes)              #\n"
          "# Don't try and check answers for more than one challenge #\n"
          "# at a time.                                              #\n"
          "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")

    while True:
        resp = input("Enter your answers: ")
        norm = normalise(resp)
        if len(norm) == 0:
            pass
        elif len(norm) % 4 != 0:
            print("- Sorry, that doesn't appear to be a valid set of files names.\n"
                  "  Each one should be 4 characters of 0-9 or A-F. Check you typed them correctly.\n")
        else:
            h = int(
                hashlib.md5(
                    sort_file_ids(norm).encode()
                ).hexdigest(),
                16
            )
            if h in answer_hashes:
                print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n"
                      "* {} *\n"
                      "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n".format(answer_hashes[h]))
            else:
                print("- Sorry, that doesn't match the correct answers for any of the challenges.\n"
                      "  You might be missing a code, check that you've found as many as the challenge ask for.\n")


if __name__ == '__main__':
    main()
