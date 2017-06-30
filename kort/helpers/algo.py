"""
base_list contains a list of letters which will be used in shortened urls
- vowels have been removed to avoid lookalike words and confusing
- same for 0 and O, 1 and l

How to generate a new random base_list:

>>> import random
>>> s = "23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
>>> base_list = list(''.join(random.sample(s,len(s))))
"""

base_list = list("KMG8HtSXFfJCBQ6dqDvmPxYZ4sbTWph5wLcV3gj972ynzRkrN")
base = len(base_list)


def encode(num: int):
    result = []
    if num == 0:
        result.append(base_list[0])

    while num > 0:
        result.append(base_list[num % base])
        num //= base

    return "".join(reversed(result))


def decode(code: str):
    num = 0
    code_list = list(code)
    for index, code in enumerate(reversed(code_list)):
        num += base_list.index(code) * base ** index
    return num


def untokenize_url(token: str):
    """Retrieve url from a kort token

    Decode token to retrieve id
    Retrieve url associated to id from database
    """
    try:
        entry_id = decode(token)
    except ValueError:
        # in case token is wrongly formatted
        return

    from kort.models import Links
    link = Links.by_id(entry_id)
    if not link:
        return
    return link.url
