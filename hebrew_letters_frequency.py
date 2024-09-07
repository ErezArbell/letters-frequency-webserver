#!/usr/bin/env python3
import requests
from tabulate import tabulate

class PageTooBig(Exception):
    pass

class HebrewLetterCounter:
    def __init__(self):
        self.hebrew_letters = u"אבגדהוזחטיכלמנסעפצקרשת"
        self.final_letters = {
            u'ך': u'כ',
            u'ם': u'מ',
            u'ן': u'נ',
            u'ף': u'פ',
            u'ץ': u'צ'
        }

    def get_text(self, url):
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        if int(r.headers['content-length']) > 300*1024:
            raise PageTooBig
        return r.content.decode()

    def count_letters(self, url, tablefmt='html'):
        try:
            text = self.get_text(url)
            if text.startswith("Error:"):
                return text
        except PageTooBig:
            return "Error: page is too big"

        letters = { letter: 0 for letter in self.hebrew_letters }

        for letter in text:
            if letter in self.final_letters.keys():
                letter = self.final_letters[letter]
            if letter in self.hebrew_letters:
                letters[letter] += 1

        total = sum(letters.values())

        letters_tupple = [(letter, letters[letter]) for letter in letters]

        table = [['Letter', 'Count', 'Percentage']]
        for letter, count in sorted(letters_tupple, key=lambda a: a[1], reverse=True):
            percentage = 0 if total == 0 else 100.0 * count / total
            percentage = "%.1f%%" % percentage
            table.append([letter, count, percentage])

        return tabulate(table, tablefmt=tablefmt, headers='firstrow')

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    counter = HebrewLetterCounter()
    print(counter.count_letters(url, tablefmt='github'))
