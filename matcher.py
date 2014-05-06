import os
import re

def leading_zero(episode, count):
    return ''.join(['0' for i in range(count - len(str(episode)))]) + str(episode)

def match_episodes_from(directory, matcher):
    for path, dirs, files in os.walk(directory):
        files.sort()
        i = 0
        for x in files:
            i += 1
            if matcher(x, i):
                yield x

def re_matcher(pattern):
    return lambda x, n: re.match(pattern, x, re.I)

def simple_matcher(episode):
    return re_matcher(r"^.*{}.*$".format(leading_zero(episode, 2)))

def prefix_matcher(prefix, episode):
    return re_matcher(r"^.*{}{}.*$".format(prefix, leading_zero(episode, 2)))

def nth_matcher(episode):
    return lambda x, n: n == episode

def match(directory, episode):
    matchers = [
            prefix_matcher("episode", episode),
            prefix_matcher("ep", episode),
            prefix_matcher("e", episode),
            prefix_matcher("x", episode),
            simple_matcher(episode),
            nth_matcher(episode),
            ]

    for matcher in matchers:
        result = list(match_episodes_from(directory, matcher))
        if len(result) == 1:
            return result[0]

