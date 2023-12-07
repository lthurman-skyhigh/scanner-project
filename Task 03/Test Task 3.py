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

from random import randint
from time import sleep
import os


def load_function():
    print("Finding method get_hits()... ", end="", flush=True)
    sleep(1)
    try:
        from task_3_work import get_hits
        print("- Passed", flush=True)
    except ImportError:
        print("- Failed. Could not find get_hits(), stopping test.", flush=True)
        try:
            import task_3_work
            print("The file task_3_work.py was found but was missing the function get_hits", flush=True)
        except ImportError:
            print("Could not find the file task_3_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    return get_hits


def test_task() -> int:
    get_hits = load_function()
    if get_hits == 1:
        return 1

    print("Testing your function... ", end="", flush=True)
    sleep(1)

    # Generate test files.
    m = randint(5, 20)
    n = randint(5, 20)
    tests = [
        (os.path.abspath(os.path.join("test_data", "test_1.txt")), ["is", "not"], [3, 1]),
        (os.path.abspath(os.path.join("test_data", "test_2.txt")), ["confidential"], [1]),
        (os.path.abspath(os.path.join("test_data", "test_3.txt")), ["hello", "world"], [m, n])
    ]

    before = [
        "This is a test sentence which is not particularly interesting.",
        "This sentence is confidently confidential.",
        ("hello " * m) + ("world " * n)
    ]

    for i, t in enumerate(tests):
        with open(t[0], "w") as fh:
            fh.write(before[i])

    # Make test calls.
    for path, keywords, expected in tests:
        try:
            hits = get_hits(path, keywords)
        except Exception as e:
            print("- Failed", flush=True)
            print("\nYour function threw the following error,", flush=True)
            print(str(type(e)).split("'")[1], ":", e, flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}\nKeywords: {keywords}", flush=True)
            return 1

        if type(hits) in (list, tuple):
            if list(hits) != expected:
                print("- Failed.", flush=True)
                print(f"\nYour function returned the wrong value. {hits} instead of {expected}.", flush=True)
                print("This happened with test data:", flush=True)
                print(f"Path: {path}\nKeywords: {keywords}", flush=True)
                return 1
        else:
            print("- Failed.", flush=True)
            print(f"\nYour function returned a value of the wrong type. "
                  f"'{type(hits)}' instead of 'list' or 'tuple'.", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}\nKeywords: {keywords}", flush=True)
            return 1
    print("- Passed", flush=True)

    # Check the contents after calls.
    after = []
    for t in tests:
        with open(t[0], "r") as fh:
            after.append(fh.read())

    print("Checking that test files have not been modified... ", end="", flush=True)
    sleep(1)
    for i, (a, b) in enumerate(zip(before, after)):
        if a != b:
            print("- Failed", flush=True)
            print(f"\nYour function modified the contents of {os.path.abspath(tests[i][0])}.", flush=True)
            print(f"The contents of the file was {len(before[i])} characters long before and {len(after[i])} after.", flush=True)
            return 1
    print("- Passed", flush=True)

    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
