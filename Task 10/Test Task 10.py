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

import subprocess
import os
from time import sleep


def test_task():
    test_cases = [
        # Case 1
        {
            "test_input": (os.path.join("test_data", "Structure 1") + "\n" +
                           os.path.join("test_data", "test_config.txt") + "\n" +
                           os.path.join("test_data", "test_output.csv") + "\n" +
                           "\n"),
            "expected_output": "Enter directory to search: Enter keywords file path: Enter output file path: Scan complete! Press <ENTER> to close...",
            "expected_results": [
                'File Path,Keyword,Hits',
                r'"test_data\Structure 1\File 1.txt","confidential",1',
                r'"test_data\Structure 1\File 2.txt","[ab][cd][ef]",1',
                r'"test_data\Structure 1\Folder 1\File 3.txt","[ab][cd][ef]",1',
                r'"test_data\Structure 1\Folder 2\File 1.txt","private",1',
                r'"test_data\Structure 1\Folder 2\File 2.txt","secret",1',
                r'"test_data\Structure 1\Folder 3\File 2.txt","secret",1',
            ]
        }
    ]

    print("Testing your program:")
    sleep(1)
    for i, case in enumerate(test_cases):

        args = ["py", "-3"] if os.name == "nt" else ["python3"]
        args.append("task_10_work.py")

        output_file = case["test_input"].strip().split("\n")[-1]
        if os.path.exists(output_file):
            os.remove(output_file)

        print(f"Checking prompts for case {i + 1}... ", end="", flush=True)

        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, err = proc.communicate(input=case["test_input"].encode())

        sleep(1)

        if err != b"":
            print("- Failed")
            print("\nYour program raised the following exception:")
            print(err.decode())
            return 1
        elif output.decode() != case["expected_output"]:
            print("- Failed")
            print("\nYour program did not give the expected output.")
            print("Expected:")
            print(case["expected_output"])
            print("\nGot:")
            print(output.decode())
            return 1
        else:
            print("- Passed")

        sleep(1)
        print(f"Checking results from your program for case {i + 1}... ", end="", flush=True)
        sleep(1)
        output_file = case["test_input"].strip().split("\n")[-1]
        if os.path.exists(output_file):
            with open(output_file, "r") as fh:
                written = fh.read()
        else:
            print("- Failed")
            print("Your program did not create the correct output.")
            print(f"Missing output file {output_file}")
            return 1

        results_valid = True
        result_lines = [line.strip() for line in written.split("\n")]

        for written_line, expected_line in zip(result_lines, case["expected_results"]):
            if written_line != expected_line:
                results_valid = False
                break

        if not results_valid:
            print("- Failed")
            print("Your program did not create the correct output.")
            print("Expected:")
            print(*case["expected_results"], sep="\n")
            print("Got:")
            print(written)
            return 1
        print("- Passed")

    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
