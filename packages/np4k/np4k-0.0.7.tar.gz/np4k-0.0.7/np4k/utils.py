# -*- coding: utf-8 -*-
"""
Holds misc. utility methods which prove to be
useful throughout this library.
"""
__title__ = 'np4k'
__author__ = 'Airvue'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023, Airvue'

import codecs
import hashlib
import logging
import os
import pickle
import random
import re
import string
import sys
from pathlib import Path
import threading
import time
from typing import Optional, List, Callable, Any, Generator, Dict

from hashlib import sha1

from bs4 import BeautifulSoup

from . import settings

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FileHelper:
    """
    Provides methods for working with files.
    """
    @staticmethod
    def loadResourceFile(filename: str) -> str:
        """
        Loads the contents of a resource file.

        :param filename: The name or path of the resource file.
        :return: The contents of the file as a string.
        :raises IOError: If the file cannot be opened or read.
        """
        if not os.path.isabs(filename):
            dirpath = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dirpath, 'resources', filename)
        else:
            path = filename
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                content = f.read()
            return content
        except IOError:
            raise IOError(f"Couldn't open file {path}")


class ParsingCandidate:

    def __init__(self, url: str, link_hash: str):
        """
        Initializes a ParsingCandidate object.

        :param url: The URL of the candidate.
        :param link_hash: The MD5 hash of the URL.
        """
        self.url = url
        self.link_hash = link_hash


class RawHelper:
    """
    Provides methods for working with raw HTML data.
    """
    @staticmethod
    def get_parsing_candidate(url: str, raw_html: str) -> Optional[ParsingCandidate]:
        """
        Gets a parsing candidate object from a URL and raw HTML data.

        :param url: The URL of the web page.
        :param raw_html: The raw HTML data.
        :return: A ParsingCandidate object.
        """
        if isinstance(raw_html, str):
            raw_html = raw_html.encode('utf-8', 'replace')
        link_hash = f"{hashlib.md5(raw_html).hexdigest()}.{time.time()}"
        return ParsingCandidate(url=url, link_hash=link_hash)


class URLHelper:
    @staticmethod
    def get_parsing_candidate(url_to_crawl: str) -> ParsingCandidate:
        """Returns a ParsingCandidate object for the given URL to crawl.

        :param url_to_crawl: The URL to crawl.
        :return: A ParsingCandidate object.
        """
        # Replace shebang in urls
        final_url = url_to_crawl.replace('#!', '?_escaped_fragment_=') \
            if '#!' in url_to_crawl else url_to_crawl
        link_hash = f"{hashlib.md5(final_url.encode()).hexdigest()}.{time.time()}"
        return ParsingCandidate(url=final_url, link_hash=link_hash)


class StringSplitter:
    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern)

    def split(self, string: str) -> list[str]:
        if not string:
            return []
        return self.pattern.split(string)


class StringReplacement:
    def __init__(self, pattern: str, replace_with: str) -> None:
        self.pattern = pattern
        self.replaceWith = replace_with

    def replaceAll(self, string: str) -> str:
        """
        Replaces all occurrences of `pattern` in `string` with `replace_with`.

        :param string: The string to perform replacements on.
        :return: The modified string with all replacements made.
        """
        if not string:
            return ''
        return string.replace(self.pattern, self.replaceWith)


class ReplaceSequence:
    def __init__(self):
        self.replacements: List[StringReplacement] = []

    def create(self, firstPattern: str, replaceWith: Optional[str] = None) -> StringReplacement:
        result = StringReplacement(firstPattern, replaceWith or '')
        self.replacements.append(result)
        return self

    def append(self, pattern: str, replaceWith: Optional[str] = None) -> StringReplacement:
        return self.create(pattern, replaceWith)

    def replaceAll(self, string: str) -> str:
        if not string:
            return ''

        mutatedString = string
        for rp in self.replacements:
            mutatedString = rp.replaceAll(mutatedString)
        return mutatedString


class TimeoutError(Exception):
    pass


def timelimit(timeout):
    """Borrowed from web.py, rip Aaron Swartz"""
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            class Dispatch(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None

                    self.setDaemon(True)
                    self.start()

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()
            c = Dispatch()
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError("Function %s timed out after %s seconds" % (function.__name__, timeout))
            if c.error:
                raise c.error[0](c.error[1])
            return c.result
        return wrapped
    return wrapper


def domain_to_filename(domain: str) -> str:
    """All '/' are turned into '-', no trailing. schema's
    are gone, only the raw domain + ".txt" remains
    """
    filename = domain.replace('/', '-')
    if filename.endswith('-'):
        filename = filename[:-1]
    filename = f"{filename}.txt"
    return filename


def filename_to_domain(filename: str) -> str:
    """
    [:-4] for the .txt at end
    The filename should have the format "example.com.txt".
    :param filename: The filename to convert.
    :return: The domain name.
    """
    return filename.replace('-', '/')[:-4]


def is_ascii(word: str) -> bool:
    """Returns True if a word is only ASCII characters"""
    return all(ord(c) < 128 for c in word)


def extract_meta_refresh(html: str) -> Optional[str]:
    """ Parses html for a tag like:
    <meta http-equiv="refresh" content="0;URL='http://sfbay.craigslist.org/eby/cto/5617800926.html'" />
    Example can be found at: https://www.google.com/url?rct=j&sa=t&url=http://sfbay.craigslist.org/eby/cto/
    5617800926.html&ct=ga&cd=CAAYATIaYTc4ZTgzYjAwOTAwY2M4Yjpjb206ZW46VVM&usg=AFQjCNF7zAl6JPuEsV4PbEzBomJTUpX4Lg
    """
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if element:
        try:
            wait_part, url_part = element['content'].split(";")
        except ValueError:
            # In case there are not enough values to unpack
            # for instance: <meta http-equiv="refresh" content="600" />
            return None
        else:
            # Get rid of any " or ' inside the element
            # for instance:
            # <meta http-equiv="refresh" content="0;URL='http://sfbay.craigslist.org/eby/cto/5617800926.html'" />
            if url_part.lower().startswith("url="):
                return url_part[4:].replace('"', '').replace("'", '')
    return None


def to_valid_filename(s: str) -> str:
    """
    Converts an arbitrary string (in our case a domain name) into a valid file name for caching.

    :param s: The string to convert.
    :return: The converted string.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in s if c in valid_chars)


def cache_disk(seconds: int = 86400 * 5, cache_folder: str = "/tmp") -> Callable:
    """
    Decorator for caching function results to disk for a specified number of seconds.

    :param seconds: The number of seconds to cache the result for. Defaults to 5 days.
    :param cache_folder: The path to the cache folder. Defaults to "/tmp".
    :return: A decorator function that caches the results of a function to disk.
    """
    def do_cache(function: Callable) -> Callable:
        def inner_function(*args, **kwargs):
            """
            Calculates a cache key based on the decorated function signature.

            The domain of the inputs (args[1]) is used to hash the cache key.

            :param args: The positional arguments passed to the function.
            :param kwargs: The keyword arguments passed to the function.
            :return: The cached result or the result of the decorated function.
            """
            key = sha1((str(args[1]) + str(kwargs)).encode('utf-8')).hexdigest()
            filepath = Path(cache_folder) / key

            # Verify that the cached object exists and is less than X seconds old.
            if filepath.exists():
                modified = filepath.stat().st_mtime
                age_seconds = time.time() - modified
                if age_seconds < seconds:
                    with open(filepath, "rb") as file:
                        return pickle.load(file)

            # call the decorated function...
            result = function(*args, **kwargs)
            # ... and save the cached object for next time
            with open(filepath, "wb") as file:
                pickle.dump(result, file)
            return result
        return inner_function
    return do_cache


def print_duration(method: Callable) -> Callable:
    """
    Decorator for printing out the runtime duration of a method in seconds.

    :param method: The method to time.
    :return: The timed method.
    """
    def timed(*args, **kw):
        start_time = time.perf_counter()
        result = method(*args, **kw)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"{method.__name__} took {duration:.2f} seconds")
        return result
    return timed


def chunks(l: List[Any], n: int) -> Generator[List[Any], None, None]:
    """
    Yield n successive chunks from l.

    :param l: The list to split into chunks.
    :param n: The number of chunks to yield.
    :return: A generator that yields the successive chunks of the input list.
    """
    newn = int(len(l) / n)
    for i in range(0, n - 1):
        yield l[i * newn:i * newn + newn]
    yield l[n * newn - newn:]


def purge(fn, pattern):
    """Delete files in a dir matching pattern
    """
    for f in os.listdir(fn):
        if re.search(pattern, f):
            os.remove(os.path.join(fn, f))


def clear_memo_cache(source):
    """Clears the memoization cache for this specific news domain
    """
    d_pth = os.path.join(settings.MEMO_DIR, domain_to_filename(source.domain))
    if os.path.exists(d_pth):
        os.remove(d_pth)
    else:
        print('memo file for', source.domain, 'has already been deleted!')


def memoize_articles(source, articles):
    """When we parse the <a> links in an <html> page, on the 2nd run
    and later, check the <a> links of previous runs. If they match,
    it means the link must not be an article, because article urls
    change as time passes. This method also uniquifies articles.
    """
    source_domain = source.domain
    config = source.config

    if len(articles) == 0:
        return []

    memo = {}
    cur_articles = {article.url: article for article in articles}
    d_pth = os.path.join(settings.MEMO_DIR, domain_to_filename(source_domain))

    if os.path.exists(d_pth):
        f = codecs.open(d_pth, 'r', 'utf8')
        urls = f.readlines()
        f.close()
        urls = [u.strip() for u in urls]

        memo = {url: True for url in urls}
        # prev_length = len(memo)
        for url, article in list(cur_articles.items()):
            if memo.get(url):
                del cur_articles[url]

        valid_urls = list(memo.keys()) + list(cur_articles.keys())

        memo_text = '\r\n'.join(
            [href.strip() for href in (valid_urls)])
    # Our first run with memoization, save every url as valid
    else:
        memo_text = '\r\n'.join(
            [href.strip() for href in list(cur_articles.keys())])

    # new_length = len(cur_articles)
    if len(memo) > config.MAX_FILE_MEMO:
        # We still keep current batch of articles though!
        log.critical('memo overflow, dumping')
        memo_text = ''

    # TODO if source: source.write_upload_times(prev_length, new_length)
    ff = codecs.open(d_pth, 'w', 'utf-8')
    ff.write(memo_text)
    ff.close()
    return list(cur_articles.values())


def get_useragent() -> str:
    """
    Returns the next user agent in a saved file, chosen randomly.

    :return: The selected user agent string.
    """
    with open(settings.USERAGENTS, 'r') as f:
        agents = f.readlines()
        selection = random.randint(0, len(agents) - 1)
        agent = agents[selection]
        return agent.strip()


def get_available_languages() -> List[str]:
    """
    Returns a list of available languages and their 2 character input codes.

    :return: A list of 2 character language codes.
    """
    stopword_files = os.listdir(os.path.join(settings.STOPWORDS_DIR))
    two_dig_codes = [f.split('-')[1].split('.')[0] for f in stopword_files]
    for d in two_dig_codes:
        assert len(d) == 2
    two_dig_codes.sort()
    return two_dig_codes


def print_available_languages() -> None:
    """
    Prints available languages with their full names
    """
    language_dict = {
        'ar': 'Arabic',
        'be': 'Belarusian',
        'bg': 'Bulgarian',
        'da': 'Danish',
        'de': 'German',
        'el': 'Greek',
        'en': 'English',
        'es': 'Spanish',
        'et': 'Estonian',
        'fa': 'Persian',
        'fi': 'Finnish',
        'fr': 'French',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'lt': 'Lithuanian',
        'mk': 'Macedonian',
        'nb': 'Norwegian (Bokmål)',
        'nl': 'Dutch',
        'no': 'Norwegian',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sl': 'Slovenian',
        'sr': 'Serbian',
        'sv': 'Swedish',
        'sw': 'Swahili',
        'th': 'Thai',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'vi': 'Vietnamese',
        'zh': 'Chinese',
    }

    codes = get_available_languages()
    print('\nYour available languages are:')
    print('\ninput code\t\tfull name')
    for code in codes:
        print(f'  {code}\t\t\t  {language_dict[code]}')
    print()


def extend_config(config: Any, config_items: Dict[str, Any]) -> Any:
    """
    Dynamically generates a new config object by extending an existing config object
    with the given key-value pairs.

    :param config: The existing config object to extend.
    :param config_items: The key-value pairs to add to the config object.
    :return: The new config object with the added key-value pairs.
    """
    for key, val in list(config_items.items()):
        if hasattr(config, key):
            setattr(config, key, val)

    return config
