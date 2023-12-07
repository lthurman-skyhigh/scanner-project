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

from random import randint, choice, shuffle
from time import sleep
import os


def simple_tests(load_rules):
    # Generate test files.
    words = [
        "confidential",
        "protected",
        "private",
        "secret",
        "personal",
        "username",
        "password"
    ]
    shuffled = list(words)
    shuffle(shuffled)
    tests = [
        (os.path.abspath(os.path.join("test_data", "test_1.txt")), [choice(words)]),
        (os.path.abspath(os.path.join("test_data", "test_2.txt")), words),
        (os.path.abspath(os.path.join("test_data", "test_3.txt")), shuffled)
    ]

    before = []
    for path, expected in tests:
        with open(path, "w") as fh:
            fh.write("\n".join(expected))
            before.append("\n".join(expected))

    # Make test calls.
    for path, expected in tests:
        try:
            loaded = load_rules(path)
        except Exception as e:
            print("- Failed", flush=True)
            print("\nYour function raised the following error,", flush=True)
            print(str(type(e)).split("'")[1], ":", e, flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        if type(loaded) not in (tuple, list):
            # Case that the wrong type is returned.
            print("- Failed.", flush=True)
            print(f"\nYour function returned a value of the wrong type. "
                  f"'{type(loaded)}' instead of 'list'.", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        elif len(loaded) != len(expected):
            # Case that the wrong number of words was returned.
            print("- Failed.", flush=True)
            print(f"\nYour function returned the wrong number of keywords. "
                  f"{len(loaded)} instead of {len(expected)}.", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        elif min([loaded[i] == expected[i] for i in range(len(expected))]) is False:
            # Case that the loaded words are not the expected words.
            print("- Failed.", flush=True)
            print(f"\nYour function returned unexpected keyword(s).", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
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
            print(f"The contents of the file was {len(before[i])} characters long before and {len(after[i])} after.",
                  flush=True)
            return 1
    print("- Passed", flush=True)

    return 0


def complex_tests(load_rules):
    # Generate test files.
    words = [
        "confidential",
        "protected",
        "private",
        "secret",
        "personal",
        "username",
        "password"
    ]
    tests = [
        [os.path.abspath(os.path.join("test_data", "test_4.txt")), []],
        [os.path.abspath(os.path.join("test_data", "test_5.txt")), []],
        [os.path.abspath(os.path.join("test_data", "test_6.txt")), []]
    ]

    before = []
    for i in range(len(tests)):
        shuffle(words)
        text = ""
        for j in range(randint(3, 6)):
            w = words[j]
            text += (" " * randint(1, 3)) + ("\t" * randint(1, 3)) + w +\
                    (" " * randint(1, 3)) + ("\t" * randint(1, 3)) + ("\n" * randint(1, 3))
            tests[i][1].append(words[j])
        before.append(text)
        with open(tests[i][0], "w") as fh:
            fh.write(text)

    # Make test calls.
    for path, expected in tests:
        try:
            loaded = load_rules(path)
        except Exception as e:
            print("- Failed", flush=True)
            print("\nYour function raised the following error,", flush=True)
            print(str(type(e)).split("'")[1], ":", e, flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        if type(loaded) not in (tuple, list):
            # Case that the wrong type is returned.
            print("- Failed.", flush=True)
            print(f"\nYour function returned a value of the wrong type. "
                  f"'{type(loaded)}' instead of 'list'.", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        elif len(loaded) != len(expected):
            # Case that the wrong number of words was returned.
            print("- Failed.", flush=True)
            print(f"\nYour function returned the wrong number of keywords. "
                  f"{len(loaded)} instead of {len(expected)}.\n"
                  f"Did you make sure to ignore empty lines?", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

        elif min([loaded[i] == expected[i] for i in range(len(expected))]) is False:
            # Case that the loaded words are not the expected words.
            print("- Failed.", flush=True)
            print(f"\nYour function returned unexpected keyword(s).\n"
                  f"Did you remember to remove whitespace?", flush=True)
            print("This happened with test data:", flush=True)
            print(f"Path: {path}", flush=True)
            return 1

    print("- Passed", flush=True)

    # Check the contents after calls.
    print("Checking that test files have not been modified... ", end="", flush=True)
    sleep(1)

    after = []
    for t in tests:
        with open(t[0], "r") as fh:
            after.append(fh.read())

    for i, (a, b) in enumerate(zip(before, after)):
        if a != b:
            print("- Failed", flush=True)
            print(f"\nYour function modified the contents of {os.path.abspath(tests[i][0])}.", flush=True)
            print(f"The contents of the file was {len(before[i])} characters long before and {len(after[i])} after.",
                  flush=True)
            return 1
    print("- Passed", flush=True)

    return 0


def test_task() -> int:
    print("Finding method load_rules()... ", end="", flush=True)
    sleep(1)
    try:
        from task_2_work import load_rules
        print("- Passed", flush=True)
    except ImportError:
        print("- Failed. Could not find load_rules(), stopping test.", flush=True)
        try:
            import task_2_work
            print("The file task_2_work.py was found but was missing the function load_rules", flush=True)
        except ImportError:
            print("Could not find the file task_2_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    print("Running simple tests... ", end="", flush=True)
    sleep(1)

    result = simple_tests(load_rules)
    if result != 0:
        return result

    print("Running complex tests... ", end="", flush=True)
    sleep(1)

    result = complex_tests(load_rules)
    if result != 0:
        return result

    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
