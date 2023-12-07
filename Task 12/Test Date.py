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

import random
import datetime
from time import sleep


def load_function(verbose=True):
    if verbose:
        print("Finding method validate_date()... ", end="", flush=True)
        sleep(1)
    try:
        from task_12_work import validate_date
        if verbose:
            print("- Passed", flush=True)
    except ImportError:
        if verbose:
            print("- Failed. Could not find validate_date(), stopping test.", flush=True)
        try:
            import task_12_work
            if verbose:
                print("The file task_12_work.py was found but was missing the function validate_date.",
                      flush=True)
        except ImportError:
            if verbose:
                print("Could not find the file task_12_work.py", flush=True)
        return 1
    except SyntaxError as e:
        print("- Failed\nAn error was found in the code to test:")
        print("-", e)
        return 1

    return validate_date


def gen_date():
    date = datetime.datetime.fromordinal(random.randint(657072, 803533))
    return str(date.day).zfill(2) + "/" + str(date.month).zfill(2) + "/" + str(date.year)


def gen_not_date():
    day = random.randint(31, 99)
    if day == 31:
        day = 0
    day = str(day).zfill(2)

    month = random.randint(12, 99)
    if month == 12:
        month = 0
    month = str(month).zfill(2)

    year = str(random.randint(0, 9999)).zfill(4)

    return "/".join([day, month, year])


def test_task():
    validate_date = load_function(True)
    if 1 == validate_date:
        return 1

    messages = [
        "\nTesting edge cases... ",
        "\nTesting your function against 100 random dates... ",
        "\nTesting your function against 100 random invalid dates... "
    ]

    manual_tests = [
        {"params": ["01/01/1970"], "result": True},
        {"params": ["28/02/2004"], "result": True},
        {"params": ["29/02/2004"], "result": True},
        {"params": ["29/02/1900"], "result": False},
        {"params": ["29/02/2000"], "result": True},
        {"params": ["31/01/1970"], "result": True},
        {"params": ["31/02/1970"], "result": False},
        {"params": ["31/03/1970"], "result": True},
        {"params": ["31/04/1970"], "result": False},
        {"params": ["31/05/1970"], "result": True},
        {"params": ["31/06/1970"], "result": False},
        {"params": ["31/07/1970"], "result": True},
        {"params": ["31/08/1970"], "result": True},
        {"params": ["31/09/1970"], "result": False},
        {"params": ["31/10/1970"], "result": True},
        {"params": ["31/11/1970"], "result": False},
        {"params": ["31/12/1970"], "result": True},
    ]

    case_sets = [
        manual_tests,
        [{"params": [gen_date()], "result": True} for i in range(100)],
        [{"params": [gen_not_date()], "result": False} for i in range(100)]
    ]

    for msg, test_cases in zip(messages, case_sets):
        print(msg, end="", flush=True)
        sleep(2)

        for test_case in test_cases:
            try:
                result = validate_date(*test_case["params"])
            except Exception as e:
                print("Error.\nYour validation function threw the following error:")
                print(str(type(e)).split("'")[1] + ": " + str(e))
                return 1

            if result != test_case["result"]:
                print("- Failed")
                print("\nYour function did not handle the following case correctly:")
                print(*test_case["params"])
                print("Expected:", test_case["result"])
                print("Got:", result)
                return 1

        print("- Passed.")
    return 0


if __name__ == '__main__':
    res = test_task()
    if res == 0:
        print("\nYour function passed all tests for this task!", flush=True)
    else:
        print("\nYour function did not pass all tests for this task.", flush=True)
    input("Press <ENTER> to continue. . .")
