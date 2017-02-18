#!/usr/bin/env python
# encoding: utf-8

import random
import optparse
import sys
import re
import os
import math
import datetime
import string

__LICENSE__ = """
The MIT License (MIT)

Copyright (c) 2012 Aaron Bassett, http://aaronbassett.com
Copyright (c) 2017 Martin Wimpress, http://flexion.org

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# random.SystemRandom() should be cryptographically secure
try:
    rng = random.SystemRandom
except AttributeError:
    sys.stderr.write("WARNING: System does not support cryptographically "
                     "secure random number generator or you are using Python "
                     "version < 2.4.\n"
                     "Continuing with less-secure generator.\n")
    rng = random.Random


# Python 3 compatibility
if sys.version[0] == "3":
    raw_input = input


def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """
    
    if options.num <= 0:
        sys.stderr.write("Little point running the script if you "
                         "don't generate even a single passphrase.\n")
        sys.exit(1)

    if options.max_length < options.min_length:
        sys.stderr.write("The maximum length of a word can not be "
                         "lesser then minimum length.\n"
                         "Check the specified settings.\n")
        sys.exit(1)

    if len(args) >= 1:
        parser.error("Too many arguments.")

    for word_type in ["adjectives", "nouns"]:
        wordfile = getattr(options, word_type, None)
        if wordfile is not None:
            if not os.path.exists(os.path.abspath(wordfile)):
                sys.stderr.write("Could not open the specified {0} word file.\n".format(word_type))
                sys.exit(1)
        else:
            common_word_file_locations = ["{0}.txt", "~/.phrase/{0}.txt"]

            for loc in common_word_file_locations:
                wordfile = loc.format(word_type)
                if os.path.exists(wordfile):
                    setattr(options, word_type, wordfile)
                    break

        if getattr(options, word_type, None) is None:
            sys.stderr.write("Could not find {0} word file, or word file does not exist.\n".format(word_type))
            sys.exit(1)


def generate_wordlist(wordfile=None,
                      min_length=0,
                      max_length=20,
                      valid_chars='.'):
    """
    Generate a word list from either a kwarg wordfile, or a system default
    valid_chars is a regular expression match condition (default - all chars)
    """

    words = []

    regexp = re.compile("^%s{%i,%i}$" % (valid_chars, min_length, max_length))

    # At this point wordfile is set
    wordfile = os.path.expanduser(wordfile)  # just to be sure
    wlf = open(wordfile)

    for line in wlf:
        thisword = line.strip()
        if regexp.match(thisword) is not None:
            words.append(thisword)

    wlf.close()
    
    if len(words) < 1:
        sys.stderr.write("Could not get enough words!\n")
        sys.stderr.write("This could be a result of either {0} being too small,\n".format(wordfile))
        sys.stderr.write("or your settings too strict.\n")
        sys.exit(1)

    return words
    

def verbose_reports(**kwargs):
    """
    Report entropy metrics based on word list size"
    """
    
    options = kwargs.pop("options")
    f = {}

    for word_type in ["adjectives", "nouns"]:
        print("The supplied {word_type} list is located at {loc}.".format(
            word_type=word_type,
            loc=os.path.abspath(getattr(options, word_type))
        ))
        
        words = kwargs[word_type]
        f[word_type] = {}
        f[word_type]["length"] = len(words)
        f[word_type]["bits"] = math.log(f[word_type]["length"], 2)

        if (int(f[word_type]["bits"]) == f[word_type]["bits"]):
            print("Your %s word list contains %i words, or 2^%i words."
                  % (word_type, f[word_type]["length"], f[word_type]["bits"]))
        else:
            print("Your %s word list contains %i words, or 2^%0.2f words."
                  % (word_type, f[word_type]["length"], f[word_type]["bits"]))    


def generate_phrase(adjectives, nouns, separator):
    return "{0}{s}{1}{s}{2}{s}".format(
        rng().choice(adjectives),
        rng().choice(adjectives),
        rng().choice(nouns),
        s=separator
    )    


def phrase(adjectives, nouns, separator, num=1,
               uppercase=False, lowercase=False, capitalise=False):
    """
    Returns a random phrase made up of
    adjective adjective noun
    """
    
    phrases = []

    for i in range(0, num):
        phrase = generate_phrase(adjectives, nouns, separator)
        if capitalise:
            phrase = string.capwords(phrase)
        phrases.append(phrase)

    all_phrases = "\n".join(phrases)
    
    if uppercase:
        all_phrases = all_phrases.upper()
    elif lowercase:
        all_phrases = all_phrases.lower()
        
    return all_phrases


if __name__ == "__main__":

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    
    parser.add_option("--adjectives", dest="adjectives",
                      default=None,
                      help="List of valid adjectives for phrase")
                      
    parser.add_option("--nouns", dest="nouns",
                      default=None,
                      help="List of valid nouns for phrase")
    
    parser.add_option("-s", "--separator", dest="separator",
                      default=' ',
                      help="Separator to add between words")
                      
    parser.add_option("-n", "--num", dest="num",
                      default=1, type="int",
                      help="Number of phrases to generate")
                      
    parser.add_option("--min", dest="min_length",
                      default=0, type="int",
                      help="Minimum length of a valid word to use in phrase")
                      
    parser.add_option("--max", dest="max_length",
                      default=20, type="int",
                      help="Maximum length of a valid word to use in phrase")
                      
    parser.add_option("--valid_chars", dest="valid_chars",
                      default='.',
                      help="Valid chars, using regexp style (e.g. '[a-z]')")
    
    parser.add_option("-U", "--uppercase", dest="uppercase",
                      default=False, action="store_true",
                      help="Force phrase into uppercase")
    
    parser.add_option("-L", "--lowercase", dest="lowercase",
                      default=False, action="store_true",
                      help="Force passphrase into lowercase")
    
    parser.add_option("-C", "--capitalise", "--capitalize", dest="capitalise",
                      default=False, action="store_true",
                      help="Force passphrase to capitalise each word")

    parser.add_option("-V", "--verbose", dest="verbose",
                      default=False, action="store_true",
                      help="Report various metrics for given options")
    
    (options, args) = parser.parse_args()
    validate_options(options, args)
    
    # Generate word lists
    adjectives = generate_wordlist(wordfile=options.adjectives,
                              min_length=options.min_length,
                              max_length=options.max_length,
                              valid_chars=options.valid_chars)
    
    nouns = generate_wordlist(wordfile=options.nouns,
                              min_length=options.min_length,
                              max_length=options.max_length,
                              valid_chars=options.valid_chars)
    
    if options.verbose:
        verbose_reports(adjectives=adjectives,
                        nouns=nouns,
                        options=options)
    
    print(phrase(
            adjectives,
            nouns,
            options.separator,
            num=int(options.num),
            uppercase=options.uppercase,
            lowercase=options.lowercase,
            capitalise=options.capitalise
        )
    )