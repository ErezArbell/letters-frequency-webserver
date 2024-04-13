#!/usr/bin/env python3
import requests
from tabulate import tabulate

class PageTooBig(Exception):
    pass

def get_text(url):
    r = requests.get(url, stream=True)
    if int(r.headers['content-length']) > 300*1024:
        raise PageTooBig
    return r.content.decode()

hebrew_letters = u"אבגדהוזחטיכלמנסעפצקרשת"
final_letters = {
    u'ך': u'כ',
    u'ם': u'מ',
    u'ן': u'נ',
    u'ף': u'פ',
    u'ץ': u'צ'
}
letters = { letter: 0 for letter in hebrew_letters }

def count_letters(url, tablefmt='html'):
    try:
        text = get_text(url)
    except PageTooBig:
        return "Error: page is too big"

    for letter in text:
        if letter in final_letters.keys():
            letter = final_letters[letter]
        if letter in hebrew_letters:
            letters[letter] += 1

    sum = 0
    for letter in letters:
        sum += letters[letter]

    letters_tupple = [(letter, letters[letter]) for letter in letters]

    table = [['Letter', 'Count', 'Percentage']]
    for letter, count in sorted(letters_tupple, key=lambda a: a[1], reverse=True):
        percentage = 0 if sum == 0 else 100.0 * count / sum
        percentage = "%.1f%%" % percentage
        table.append([letter, count, percentage])

    return tabulate(table, tablefmt=tablefmt, headers='firstrow')

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(count_letters(url, tablefmt='github'))
