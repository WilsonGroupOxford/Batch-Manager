from typing import Callable


def valid_int(string: str, lower: float | int = float("-inf"), upper: float | int = float("inf"),
              confirm_num: int = None) -> str:
    while True:
        while True:
            try:
                ans = int(input(string))
                break
            except ValueError:
                print("That is not a valid answer")
        if ans < lower or ans > upper:
            print("That is not a valid answer")
        elif ans == confirm_num:
            if confirm():
                break
        else:
            break
    return ans


def micro_valid_int(string: str, lower: float | int = float("-inf"), upper: float | int = float("inf")) -> bool:
    try:
        int(string)
    except ValueError:
        return False
    if int(string) < lower or int(string) > upper:
        return False
    return True


def valid_str(prompt: str, length_range: list = None, char_types: list = None, exit_string: str = None) -> str | bool:
    valid = 0
    while valid == 0:
        valid = 1
        if exit_string is not None:
            prompt += f"({exit_string} to exit)\n"
        string = input(prompt)
        if string == exit_string:
            return False
        if length_range is not None:
            if len(string) < length_range[0] or len(string) > length_range[1]:
                print(f"Input must be between {length_range[0]} and {length_range[1]} characters long")
                valid = 0
        if char_types is not None:
            if char_types == "ASCII":
                char_types = [chr(i) for i in range(32, 127)]
            for char in string:
                if char not in char_types:
                    print(f"Input must not contain {char}")
                    valid = 0
                    break
    return string


def valid_triple(prompt: str, trip_type: str, valid_func: Callable,
                 lower: float | int = float("-inf"), upper: float | int = float("inf"),
                 delim: str = ",", exit_string: str = "e") -> tuple:
    nums = input(prompt)
    if nums == exit_string:
        return False, "exit"
    nums = nums.split(delim)
    if len(nums) != 3:
        print("You must enter only 3 numbers")
        return False, None
    print(valid_func)
    for i, num in enumerate(nums):
        try:
            nums[i] = valid_func(num)
        except ValueError:
            print("You did not enter either integers or floats")
            return False, None
    if nums[0] > nums[1]:
        print("First number must be less than second number")
        return False, None
    if (nums[0] or nums[1]) < lower or (nums[0] or nums[1]) > upper:
        print("Numbers out of bounds")
        return False, None
    if trip_type == "ses" and nums[-1] > nums[1] - nums[0]:
        print("Step size cannot be larger than range")
        return False, None
    if trip_type == "sen":
        try:
            nums[2] = int(nums[2])
        except ValueError:
            print("Number of steps must be an integer")
            return False, None
        if nums[2] < 2 or nums[2] > 999999:
            print("Number of steps must be 1 < n < 999999")
            return False, None
        if valid_func == int and nums[2] > nums[1] - nums[0] + 1:
            print("Number of steps cannot exceed the range for integers")
            return False, None
    return True, nums


def valid_csv(prompt: str, csv_type: str, lower: float | int = float("-inf"), upper: float | int = float("inf"),
              valid_func: Callable = None, allowed_strings: list | tuple = None, delim: str = ",", exit_string: str = "e"):
    string = input(f"{prompt}\n('{exit_string}' to exit)\n")
    if string == exit_string:
        return False, "exit"
    csv = string.split(delim)
    if len(csv) < 2:
        print("You must enter at least 2 items")
        return False, None
    if csv_type == "nums":
        for i, string in enumerate(csv):
            try:
                csv[i] == valid_func(string)
            except ValueError:
                print("You must enter either integers or floats")
                return False, None
            if csv[i] < lower or csv[i] > upper:
                print(f"Number '{csv[i]}' out of bounds")
                return False, None
    if allowed_strings:
        for string in csv:
            if string not in allowed_strings:
                print(f"Disallowed string '{string}' entered")
                return False, None
    return True, csv


def confirm(prompt: str = "Are you sure?[y,n]", answers: tuple = ("y", "n")) -> bool:
    while True:
        conf = input(prompt).lower()
        if conf == answers[0]:
            return True
        elif conf == answers[1]:
            return False
        print("That is not a valid answer")
