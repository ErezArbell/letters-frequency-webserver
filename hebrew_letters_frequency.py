#!/usr/bin/env python3
import requests

def get_text(url):
    response = requests.get(url)
    return response.text

hebrew_letters = u"אבגדהוזחטיכלמנסעפצקרשת"
final_letters = {
    u'ך': u'כ',
    u'ם': u'מ',
    u'ן': u'נ',
    u'ף': u'פ',
    u'ץ': u'צ'
}
letters = { letter: 0 for letter in hebrew_letters }

def count_letters(url):
    text = get_text(url)
    for letter in text:
        if letter in final_letters.keys():
            letter = final_letters[letter]
        if letter in hebrew_letters:
            letters[letter] += 1

    sum = 0
    for letter in letters:
        sum += letters[letter]

    letters_tupple = [(letter, letters[letter]) for letter in letters]
    output = ""
    for letter, count in sorted(letters_tupple, key=lambda a: a[1], reverse=True):
        output += "%3s%8d%8.1f%%\n" % (letter, count, 0 if sum == 0 else 100.0 * count / sum)

    return output
