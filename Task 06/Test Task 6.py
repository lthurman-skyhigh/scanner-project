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

from time import sleep
import copy


def load_function(verbose=True):
    if verbose:
        print("Finding method sort_2d_list()... ", end="", flush=True)
        sleep(1)
    try:
        from task_6_work import sort_2d_list
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find sort_2d_list(), stopping test.", flush=True)
        try:
            import task_6_work
            if verbose:
                print("The file task_6_work.py was found but was missing the function sort_2d_list", flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_6_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    return sort_2d_list


def test_task():
    sort_2d_list = load_function(True)
    if sort_2d_list == 1:
        return 1

    test_data = [
        [
            [
                [0, 7, 7], [0, 4, 7], [4, 5, 8], [7, 8, 0], [3, 0, 8],
                [6, 9, 2], [6, 5, 6], [5, 5, 5], [9, 5, 4], [7, 3, 3]
            ],
            0,
            False
        ],
        [
            [
                [7, 9, 7], [2, 5, 6], [8, 9, 5], [0, 2, 8], [6, 0, 4],
                [9, 3, 6], [6, 6, 3], [2, 9, 4], [1, 8, 9], [7, 9, 9]
            ],
            2,
            False
        ],
        [
            [
                [0, 1, 4], [8, 8, 1], [1, 0, 7], [4, 8, 9], [0, 0, 8],
                [0, 3, 1], [1, 3, 8], [0, 4, 1], [4, 4, 4], [6, 7, 7]
            ],
            1,
            True
        ],
        [
            [
                [8, 7, 5], [8, 8, 1], [8, 2, 5], [1, 7, 1], [5, 3, 5],
                [4, 9, 5], [9, 4, 2], [8, 7, 0], [8, 2, 8], [1, 7, 0]
            ],
            0,
            True
        ],
    ]
    expected_results = [
        [[0, 7, 7], [0, 4, 7], [3, 0, 8], [4, 5, 8], [5, 5, 5], [6, 9, 2], [6, 5, 6], [7, 8, 0], [7, 3, 3], [9, 5, 4]],
        [[6, 6, 3], [6, 0, 4], [2, 9, 4], [8, 9, 5], [2, 5, 6], [9, 3, 6], [7, 9, 7], [0, 2, 8], [1, 8, 9], [7, 9, 9]],
        [[8, 8, 1], [4, 8, 9], [6, 7, 7], [0, 4, 1], [4, 4, 4], [0, 3, 1], [1, 3, 8], [0, 1, 4], [1, 0, 7], [0, 0, 8]],
        [[9, 4, 2], [8, 7, 5], [8, 8, 1], [8, 2, 5], [8, 7, 0], [8, 2, 8], [5, 3, 5], [4, 9, 5], [1, 7, 1], [1, 7, 0]]
    ]

    print("\nTesting your function... ", end="", flush=True)

    sleep(2)

    for test, expected in zip(test_data, expected_results):
        failed = False
        data, ind, rev = test
        try:
            result = sort_2d_list(copy.deepcopy(data), ind, rev)
        except Exception as e:
            failed = True
            result = "Error.\nYour function threw the following error:\n"
            result += str(type(e)).split("'")[1] + ": " + str(e)

        if result != expected or failed:
            print("- Failed")
            print("\nYour function did not handle the following case correctly:")
            print("List:", test[0])
            print("Index:", test[1])
            print("Reverse:", test[2])
            print("\nExpected:", expected)
            print("Returned:", result)
            return 1

    print("Passed.")
    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
