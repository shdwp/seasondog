from seasondog.config import MOVIE_EXTENSIONS, SUB_EXTENSIONS
from seasondog import config

import time
import os
import re


def leading_zero(episode, count):
    return ''.join(['0' for i in range(count - len(str(episode)))]) + str(episode)


def re_matcher(pattern):
    return lambda x, n: re.match(pattern, x, re.I)


def simple_matcher(episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}.*({})$".format(leading_zero(episode, zero),
                                             "|".join(extensions)))


def prefix_matcher(prefix, episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}{}.*({})$".format(prefix,
                                               leading_zero(episode, zero),
                                               "|".join(extensions)))


def prefix_suffix_matcher(prefix, suffix, episode, extensions=[], zero=2):
    return re_matcher(r"^.*{}{}{}.*({})$".format(prefix,
                                                 leading_zero(episode, zero),
                                                 suffix,
                                                 "|".join(extensions)))


def nth_matcher(episode):
    return lambda x, n: n == episode


def match(directory, matchers, limit=1):
    if config.MATCHER_DEBUG:
        start_time = time.time()

    for path, dirs, files in os.walk(directory):
        files.sort()

        for matcher in matchers:
            result = []
            i = 0
            for x in files:
                i += 1
                if matcher(x, i):
                    result.append(os.path.join(path, x))

            if config.MATCHER_DEBUG:
                if len(result) != 0:
                    print("Matcher {}, matched {}".format(matcher, result))
                    print("    ", "ok" if len(result) == 1 else "fail: multiple results")

            if result and (limit == -1 or len(result) == limit):
                if config.MATCHER_DEBUG:
                    print("Matched in: {}".format(time.time() - start_time))
                return result

    if config.MATCHER_DEBUG:
        print("Matched in: {}".format(time.time() - start_time))
        print("None matched!")


def match_episode(directory, episode, limit=1):
    matchers = []
    for p in config.PREFIXES:
        for s1 in config.SURROUNDINGS:
            for s2 in config.SURROUNDINGS:
                for i in range(1, 3):
                    matchers.append(prefix_suffix_matcher(
                        p+s1,
                        s2, episode,
                        MOVIE_EXTENSIONS,
                        i))

    for i in range(1, 3):
        matchers.append(simple_matcher(episode, MOVIE_EXTENSIONS, i))
    matchers.append(nth_matcher(episode))

    return match(directory, matchers, limit)


def match_subs(directory, episode, limit=1):
    matchers = []
    for p in config.PREFIXES:
        for s1 in config.SURROUNDINGS:
            for s2 in config.SURROUNDINGS:
                for i in range(1, 3):
                    matchers.append(prefix_suffix_matcher(
                        p+s1,
                        s2,
                        episode,
                        SUB_EXTENSIONS,
                        i))

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
