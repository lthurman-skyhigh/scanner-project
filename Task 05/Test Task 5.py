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


def load_function(verbose=True):
    if verbose:
        print("Finding method scan()... ", end="", flush=True)
        sleep(1)
    try:
        from task_5_work import scan
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find scan(), stopping test.", flush=True)
        try:
            import task_5_work
            if verbose:
                print("The file task_5_work.py was found but was missing the function scan", flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_5_work.py", flush=True)
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

    test_path = os.path.join("test_data", "Structure 1")
    test_keywords = [
        "confidential",
        "private",
        "secret",
        "Confidential",
        "Private",
        "Secret",
        "CONFIDENTIAL",
        "PRIVATE",
        "SECRET"
    ]
    expected_results = {
        os.path.join("test_data", "Structure 1", "File 1.txt"): [1, 0, 0, 0, 0, 0, 0, 0, 0],
        os.path.join("test_data", "Structure 1", "Folder 2", "File 1.txt"): [0, 1, 0, 0, 0, 0, 0, 0, 0],
        os.path.join("test_data", "Structure 1", "Folder 2", "File 2.txt"): [0, 0, 1, 0, 0, 0, 0, 0, 0],
        os.path.join("test_data", "Structure 1", "Folder 3", "File 2.txt"): [0, 0, 1, 0, 0, 0, 0, 0, 0]
    }

    print("\nTesting your function...")
    print("path:", test_path)
    print("keywords:")
    for k in test_keywords:
        print("-", k)

    sleep(3)

    try:
        results: dict = scan(test_path, test_keywords)
    except Exception as e:
        print("- Failed", flush=True)
        print("\nYour function threw the following error:", flush=True)
        print(str(type(e)).split("'")[1], ":", e, flush=True)
        return 1

    # Check that the function returns the correct type.
    if not isinstance(results, dict):
        print("Your function did not return a valid dictionary.")
        return 1

    found = []
    for ek in expected_results:
        if ek in results.keys():
            found.append(ek)
            hits = list(results[ek])
            if hits != expected_results[ek]:
                # Found but wrong hits.
                print("\nFailed.")
                if sum(hits) > sum(expected_results[ek]):
                    # Matched too many things.
                    print("Your function matched too many things in file:")
                else:
                    # Missed some matches.
                    print("Your function missed matches in file:")
                print(ek)
                return 1
        else:
            # Not found.
            print(f"\nFailed.\nYour function did not catch the file:\n{ek}")
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
