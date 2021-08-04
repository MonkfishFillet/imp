import re
import random

def rolls_from_args(args: str):
    args_match = lambda arg_pattern: _RollUtil._args_match_regex(arg_pattern, args)

    if args_match(_DNDRoll.ARG_PATTERN):
        ret = _DNDRoll(args)
    elif args_match(_RangeRoll.ARG_PATTERN):
        ret = _RangeRoll(args)
    elif args_match(_ListRoll.ARG_PATTERN):
        ret = _ListRoll(args)
    elif args == '':
        ret = _RangeRoll('1-100')
    else:
        ret = None
    
    return str(ret) if ret else None


class _RollUtil():
    @classmethod
    def _args_match_regex(cls, pattern: str, args: str):
        match = re.search(pattern, args)
        return True if match else False
    
    @classmethod
    def _findall_matches_in_args(cls, pattern: str, args: str):
        matches = re.findall(pattern, args)
        return matches

    # this is kinda tightly coupled, but considering it's an optional helper function following a common
    #  interface for the Roll classes, I think the reduction in duplicate code is worth it
    @classmethod
    def parse_args_and_roll(cls, arg_pattern: str, parse_arg_matches: callable, roll: callable, args: str):
        matches = cls._findall_matches_in_args(arg_pattern, args)
        parse_arg_matches(matches)
        roll()


class _DNDRoll():  # Names TBD
    ARG_PATTERN = r'([0-9]*d[0-9]+)(\+[0-9]+)*'

    def __init__(self, args: str):
        self.rolls = []
        _RollUtil.parse_args_and_roll(self.ARG_PATTERN, self._parse_matches, self.roll, args)

    def _parse_matches(self, matches):
        def parse_num_rolls(roll_match):
            roll_parts = roll_match.split('d')
            num_rolls = roll_parts[0]
            if not num_rolls:
                num_rolls = 1
            return int(num_rolls)

        def parse_max_roll(roll_match):
            roll_parts = roll_match.split('d')
            max_roll = roll_parts[-1]
            return int(max_roll)

        def parse_offset(offset_match):
            offset_parts = offset_match.split('+')
            offset = offset_parts[-1]
            if not offset:
                offset = 0
            return int(offset)

        for match in matches:
            roll_match, offset_match = match

            num_rolls = parse_num_rolls(roll_match)
            max_roll = parse_max_roll(roll_match)
            offset = parse_offset(offset_match)

            roll = {'num': num_rolls, 'max': max_roll, 'offset': offset}
            self.rolls.append(roll)

    def roll(self):
        for roll in self.rolls:
            num_rolls = roll['num']
            max_roll = roll['max']
            offset = roll['offset']

            sub_rolls = [random.randint(1, max_roll) for _ in range(num_rolls)]
            result = sum(sub_rolls) + offset

            roll['sub_rolls'] = sub_rolls
            roll['result'] = result

    def __str__(self):
        rolls = []
        for roll in self.rolls:
            num_rolls = str(roll['num'])
            max_roll = str(roll['max'])
            offset = str(roll['offset'])
            result = str(roll['result'])
            sub_rolls = [str(sub_roll) for sub_roll in roll['sub_rolls']]

            sub_rolls = ' + '.join(sub_rolls)
            rolls.append(f"{num_rolls}d{max_roll}: {sub_rolls} + {offset} = {result}")
        return '\n'.join(rolls)

    
class _RangeRoll():  # Names TBD
    ARG_PATTERN = r'[0-9]+-[0-9]+'

    def __init__(self, args: str):
        self.rolls = []
        _RollUtil.parse_args_and_roll(self.ARG_PATTERN, self._parse_matches, self.roll, args)
        
    def _parse_matches(self, matches):
        for match in matches:
            bounds = match.split('-')
            bounds = [int(bound) for bound in bounds]
            low = min(bounds)
            high = max(bounds)
            
            self.rolls.append({'min': low, 'max': high})

    def roll(self):
        for roll in self.rolls:
            result = random.randint(roll['min'], roll['max'])
            roll['result'] = result

    def __str__(self):
        rolls = [f"{roll['min']}-{roll['max']}: {roll['result']}" for roll in self.rolls]
        return '\n'.join(rolls)


class _ListRoll():  # Names TBD
    ARG_PATTERN = r'\w+'

    def __init__(self, args: str):
        self.choices = []
        self.result = None
        _RollUtil.parse_args_and_roll(self.ARG_PATTERN, self._parse_matches, self.roll, args)

    def _parse_matches(self, matches):
        self.choices = matches

    def roll(self):
        self.result = random.choice(self.choices)

    def __str__(self):
        choices_str = "Choices: " + ", ".join(self.choices)
        result_str = f"Result: {self.result}"
        return f"{choices_str}\n{result_str}"