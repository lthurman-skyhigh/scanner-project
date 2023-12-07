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

import datetime
import os
import random
import re
import time


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("----------------------------------------")


def test(pattern, n=50, verbose=False):
    print("Checking regex is valid... ", end="", flush=True)
    time.sleep(1)
    try:
        rc = re.compile(pattern)
    except re.error:
        print("Failed")
        return 1
    print("Passed")

    print(f"Testing '{pattern}' against {n} random dates... ", end="", flush=True)
    time.sleep(1)

    for i in range(n):
        date = datetime.datetime.fromordinal(random.randint(657072, 803533))
        string_date = str(date.day).zfill(2) + "/" + str(date.month).zfill(2) + "/"
        if random.randint(0, 1):
            string_date += str(date.year)
        else:
            string_date += str(date.year)[2:]
        if verbose:
            print(f"\nChecking {string_date}... ", end="", flush=True)
        match = rc.search(string_date)
        if match is None:
            print("Failed")
            print(f"\nYour pattern failed to catch the date {string_date}.")
            return 1
        elif match.string[match.start(): match.end()] != string_date:
            print("Failed")
            print(f"\nYour pattern failed to catch the date {string_date} properly. "
                  f"Caught '{match.string[match.start(): match.end()]}'.")
            return 1
        elif verbose:
            print("Passed", end="", flush=True)
    print("- Passed")
    return 0


if __name__ == '__main__':
    while True:
        clear_screen()
        p = input("Enter a regex pattern to test: ")
        result = test(p, verbose=False)

        if result == 0:
            print("\nYour pattern passed all tests for this task!\n")
        else:
            print("\nYour pattern did not pass all tests for this task.\n")

        input("Press <ENTER> to try another pattern . . .")
