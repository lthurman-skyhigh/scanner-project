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
import subprocess
from time import sleep


def load_function(verbose=True):
    if verbose:
        print("Finding method scan()... ", end="", flush=True)
        sleep(1)
    try:
        from task_4_work import scan
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find scan(), stopping test.", flush=True)
        try:
            import task_4_work
            if verbose:
                print("The file task_4_work.py was found but was missing the function scan", flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_4_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1
    return scan


def test_task():
    scan = load_function(True)
    if scan == 1:
        return 1

    tests = [
        [
            # Case
            os.path.join("test_data", "Structure 1"),
            # Expected
            "".join([p + "\n" for p in [
                os.path.join("test_data", "Structure 1", "File 1.txt"),
                os.path.join("test_data", "Structure 1", "File 2.txt"),
                os.path.join("test_data", "Structure 1", "Folder 1", "File 1.txt"),
                os.path.join("test_data", "Structure 1", "Folder 1", "File 2.txt"),
                os.path.join("test_data", "Structure 1", "Folder 2", "File 1.txt"),
                os.path.join("test_data", "Structure 1", "Folder 2", "File 2.txt"),
                os.path.join("test_data", "Structure 1", "Folder 3", "File 1.txt"),
                os.path.join("test_data", "Structure 1", "Folder 3", "File 2.txt"),
            ]
                     ]
                    )
        ],
    ]

    for path, expected in tests:
        print(f"Testing on {path}...")
        sleep(1)

        interpreter = ["py", "-3"] if os.name == "nt" else ["python3"]
        args = interpreter + ["__harness.py", path]

        try:
            print()
            output = subprocess.check_output(args).decode()
        except subprocess.CalledProcessError:
            print("\nYour function raised the above exception.")
            return 1

        output_correct = True
        output_lines = [line.strip() for line in output.split("\n")]
        expected_lines = [line.strip() for line in expected.split("\n")]
        if len(output_lines) == len(expected_lines):
            for output_line, expected_line in zip(output_lines, expected_lines):
                if output_line.strip() != expected_line.strip():
                    break
        else:
            output_correct = False

        if not output_correct:
            print("Failed\n")
            print("Your function did not print the files correctly.")
            print("\nExpected:")
            print(expected)
            print("\nGot:")
            print(output)
            return 1

        print("Passed")

    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
