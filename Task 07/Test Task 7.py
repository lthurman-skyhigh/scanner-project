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
from time import sleep


def load_functions(verbose=True):
    if verbose:
        print("Finding method format_results()... ", end="", flush=True)
        sleep(1)
    try:
        from task_7_work import format_results
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find format_results(), stopping test.", flush=True)
        try:
            import task_7_work
            if verbose:
                print("The file task_7_work.py was found but was missing the function format_results",
                      flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_7_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    if verbose:
        print("Finding method save_results()... ", end="", flush=True)
        sleep(1)
    try:
        from task_7_work import save_results
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find save_results(), stopping test.", flush=True)
        try:
            import task_7_work
            if verbose:
                print("The file task_7_work.py was found but was missing the function save_results", flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_7_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    return format_results, save_results


def test_task() -> int:
    format_results, save_results = load_functions(True)
    if 1 in (format_results, save_results):
        return 1

    test_cases = [
        # Case 1
        {
            "hits": {
                os.path.join("test_data", "Structure 1", "File 1.txt"): [1, 0, 0],
                os.path.join("test_data", "Structure 1", "Folder 2", "File 1.txt"): [0, 1, 0],
                os.path.join("test_data", "Structure 1", "Folder 2", "File 2.txt"): [0, 0, 1],
                os.path.join("test_data", "Structure 1", "Folder 3", "File 2.txt"): [0, 0, 1]
            },
            "keywords": [
                "confidential",
                "private",
                "secret"
            ],
            "output_path": os.path.join("test_data", "test_output_1.csv"),
            "expected": 'File Path,Keyword,Hits' + '\n' +
                        '"' + os.path.join('test_data', 'Structure 1', 'File 1.txt') + '","confidential",1\n' +
                        '"' + os.path.join('test_data', 'Structure 1', 'Folder 2', 'File 1.txt') + '","private",1\n' +
                        '"' + os.path.join('test_data', 'Structure 1', 'Folder 2', 'File 2.txt') + '","secret",1\n' +
                        '"' + os.path.join('test_data', 'Structure 1', 'Folder 3', 'File 2.txt') + '","secret",1\n'
        },
        # Case 2
        {
            "hits": {
                'path 1': [1, 4],
                'path 2': [2, 1],
            },
            "keywords": [
                "keyword 1",
                "keyword 2"
            ],
            "output_path": os.path.join("test_data", "test_output_2.csv"),
            "expected": 'File Path,Keyword,Hits\n' +
                        '"path 1","keyword 2",4\n' +
                        '"path 1","keyword 1",1\n' +
                        '"path 2","keyword 1",2\n' +
                        '"path 2","keyword 2",1\n'
        },
    ]

    print("\nTesting your function... ", end="", flush=True)

    sleep(2)

    for test_case in test_cases:
        # Clear the test_output.
        if os.path.exists(test_case["output_path"]):
            os.remove(test_case["output_path"])

        # Call function format_results.
        try:
            formatted = format_results(test_case["hits"], test_case["keywords"])
        except Exception as e:
            print("Error.\nYour format_results function threw the following error:")
            print(str(type(e)).split("'")[1] + ": " + str(e))
            return 1
        # Call function save_results.
        try:
            save_results(test_case["output_path"], formatted)
        except Exception as e:
            print("Error.\nYour save_results function threw the following error:")
            print(str(type(e)).split("'")[1] + ": " + str(e))
            return 1

        if os.path.exists(test_case["output_path"]):
            # If the function created a correctly named output file.
            with open(test_case["output_path"], "r") as fh:
                written = fh.read()

            if written != test_case["expected"]:
                print("- Failed")
                print("\nYour function did not handle the following case correctly:")
                print("Hits:")
                for h in test_case["hits"]:
                    print("-", h, ":", test_case["hits"][h])
                print("\nExpected:\n", test_case["expected"])
                print("Returned:\n", written)
                return 1
        else:
            # If the function did NOT create a correctly named output file.
            print("- Failed")
            print("\nYour function did not create the required output file:", test_case["output_path"])
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
