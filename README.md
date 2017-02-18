# Generate a phrase

Forked from [Pass-phrase](https://github.com/aaronbassett/Pass-phrase)
by [Aaron Bassett](https://about.me/aaronbassett) which was inspired by
the 'Password Strength' comic by [xkcd](http://xkcd.com/936/).

# What it does

Phrases are 3 words; adjective, adjective, noun. I find this pattern
produces suitable phrases.

## Usage

**From the command line**

    $ ./show_title.py -C
    Cool Skillful Title

**In your own scripts**

There is no easy way to use it in your own scripts at the moment. But
if you really must use it _right this second_ in your own scripts then
you can do:

    >>> from show_title import generate_wordlist, passphrase
    >>> adjectives = generate_wordlist("adjectives.txt")
    >>> nouns = generate_wordlist("nouns.txt")
    >>> phrase(adjectives, adjectives, nouns, " ")
    'rare mere reward'

## Word files

The script expects 2 different word files, I've included examples of
these in the repo:

+ adjectives.txt
+ nouns.txt

It will check for the existence of these files in the current directory
or in `~/.show-title/`

If you want to use other files, or relocate them, use the command line
options.

    $ ./show_tile.py --adjectives="/usr/share/dict/adjectives" --nouns="/usr/share/dict/nouns" --verbs="/usr/share/dict/verbs"

## Command line options

    Options:
      -h, --help            show this help message and exit
      --adjectives=ADJECTIVES
                            List of valid adjectives for passphrase
      --nouns=NOUNS         List of valid nouns for passphrase
      -s SEPARATOR, --separator=SEPARATOR
                            Separator to add between words
      -n NUM, --num=NUM     Number of passphrases to generate
      --min=MIN_LENGTH      Minimum length of a valid word to use in passphrase
      --max=MAX_LENGTH      Maximum length of a valid word to use in passphrase
      --valid_chars=VALID_CHARS
                            Valid chars, using regexp style (e.g. '[a-z]')
      -U, --uppercase       Force passphrase into uppercase
      -L, --lowercase       Force passphrase into lowercase
      -C, --capitalise, --capitalize
                            Force passphrase to capitalise each word
      -V, --verbose         Report various metrics for given options


## Thanks

Thanks to Steven Tobin and his version of the
[XKCD-password-generator](https://github.com/redacted/XKCD-password-generator),
it inspired me to add some additional features to my own version. I've
also used bits & pieces of the code from XKCD-password-generator here.

## License

MIT: http://aaron.mit-license.org