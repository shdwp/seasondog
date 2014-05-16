import os
import re
from seasondog.config import MOVIE_EXTENSIONS, SUB_EXTENSIONS

def leading_zero(episode, count):
    return ''.join(['0' for i in range(count - len(str(episode)))]) + str(episode)

def re_matcher(pattern):
    return lambda x, n: re.match(pattern, x, re.I)

def simple_matcher(episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}.*({})$".format(leading_zero(episode, zero), "|".join(extensions)))

def prefix_matcher(prefix, episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}{}.*({})$".format(prefix, leading_zero(episode, zero), "|".join(extensions)))

def prefix_suffix_matcher(prefix, suffix, episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}{}{}.*({})$".format(prefix, leading_zero(episode, zero), suffix, "|".join(extensions)))

def nth_matcher(episode):
    return lambda x, n: n == episode

def match(directory, matchers, limit=1):
    for path, dirs, files in os.walk(directory):
        files.sort()

        for matcher in matchers:
            result = []
            i = 0
            for x in files:
                i += 1
                if matcher(x, i):
                    result.append(os.path.join(path, x))

            if result and (limit == -1 or len(result) == limit):
                return result

def match_episode(directory, episode, limit=1):
    prefixes = ["episode", "ep", "e", "x"]
    suffixes = [" ", ""]
    matchers = []
    for p in prefixes:
        for s in suffixes:
            for i in range(1, 3):
                matchers.append(prefix_suffix_matcher(p, s, episode, MOVIE_EXTENSIONS, i))

    matchers.append(simple_matcher(episode, MOVIE_EXTENSIONS))
    matchers.append(nth_matcher(episode))

    return match(directory, matchers, limit)

def match_subs(directory, episode, limit=1):
    prefixes = ["episode", "ep", "e", "x"]
    suffixes = [" ", ""]
    matchers = []
    for p in prefixes:
        for s in suffixes:
            for i in range(1, 3):
                matchers.append(prefix_suffix_matcher(p, s, episode, SUB_EXTENSIONS, i))

    matchers.append(simple_matcher(episode, SUB_EXTENSIONS))
    matchers.append(nth_matcher(episode))

    return match(directory, matchers, limit)

def match_file(directory, episode, limit=1):
    return match(
            directory, [
            simple_matcher(episode),
            nth_matcher(episode),
            ],
            limit)
