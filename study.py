#! /Users/nguyen/anaconda3/bin/python

from string import punctuation
import sys
from collections import Counter
import json
from re import sub
from random import choice, choices, randint

def word_counts(string_input):
    """ Returns word count for a string
    """
    # initialize dictionary
    dict_of_words = {}

    all_words = string_input.split()
    all_words = [word.lower() for word in all_words]
    dict_of_words.update(Counter(all_words))
    return dict_of_words

def study(filename):
    """ Create flash cards from the markdown cells of a jupyter notebook
    """
    # open the file
    with open(filename) as f:
        data = json.load(f)
    f.close()

    # extract the text from the markdown cells
    all_source_cells = []
    for cell in data["cells"]:
        if cell["cell_type"] == "markdown":
            all_source_cells.append(cell["source"])

    # get general word count
    gen_word_count = {}
    for cell in all_source_cells:
        for line in cell:
            line = line.lower().strip(punctuation)
            line = sub('[`,.\(\)]', '', line)
            gen_word_count.update(word_counts(line))

    # Make a list of keywords
    keywords = []
    for cell in all_source_cells:
        for line in cell:
            for word in line.split():
                if '*' in word:
                    clean_word = word.replace('*', '').replace('\n', '')
                    if len(clean_word) > 3:
                        keywords.append(clean_word)
    # add repeated words to keywords list
    for k, v in gen_word_count.items():
        if v > 1 and len(k) > 4:
            keywords.append(k)
    # Make the flash cards
    flash_cards = {}
    for cell in all_source_cells:
        for line in cell:
            for word in keywords:
                line = line.replace('*', '').replace('\n', '')
                words_list = line.split()
                if word in words_list:
                    words_list = ['_____' if x == word else x for x in words_list]
                    question = " ".join(words_list)
                    flash_cards.update({question: word})

    return flash_cards, keywords

if __name__ == '__main__':
    flash_cards, keywords = study(sys.argv[1])

    i = len(flash_cards)
    score = ""

    print("{} question(s) were created".format(i))
    while i > 0:
        question = choice(list(flash_cards.keys()))
        print(question)
        correct_answer = flash_cards.pop(question)
        multi_choices = choices(list(flash_cards.values()), k=5)
        multi_choices.append(correct_answer)
        print(sorted(multi_choices))
        answer = input("Type in your answer: ")
        print("Correct answer: " + correct_answer + '\n')
        i -= 1
        if answer == correct_answer:
            score += '+'
        else:
            score += '-'
        print("Score: " + score + '\n' + "Type ^C to quit." + '\n')
