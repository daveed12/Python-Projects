#David De La Cruz

import sys
import random
from itertools import permutations


def getwords(words, num, word):
    permutated_words = list(map("".join, permutations(word, num)))
    return list(set(permutated_words) & set(words))


def formatoutput(listwords,postpermutated):
    if listwords == postpermutated:
        return -1
    for words in listwords:
        count = 0
        letters = len(words[0])
        for word in words:
            if '-' in word:
                count = count + 1
        print(words)
        if len(words) == count:
            print("%d %d-letter words left" % (count, letters))
        else:
            print("%d %d-letter words left" % (len(words) - (len(words) - count), letters))


def checklist(listwords, guess):
    count = 0
    for words in listwords:
        for word in words:
            if word == guess:
                return count, words.index(word)
        count = count + 1
    return -1, -1


def main():
    postpermutated = []

    if len(sys.argv) > 1:
        random.seed(sys.argv[1])
    else:
        random.seed()

    file = open("words.txt", "r")
    text_string = file.read()
    words = [words for words in text_string.split()]

    length = input("Enter the range of word lengths (low,high)")
    low, high = [y for x in length.split(',') for y in x if y.isdigit()]
    low, high = int(low), int(high)
    word = random.choice(words)

    while True:
        if low <= len(word):
            if high >= len(word):
                break
        word = random.choice(words)

    tmp = list(word)
    random.shuffle(tmp)
    word = ''.join(tmp)

    for x in range(low, high+1):
        postpermutated.append(getwords(words, x, word))
    postpermutated = [sorted(x) for x in postpermutated]
    postpermutated = [x for x in postpermutated if x != []]

    blanks = [[len(y)*'-' for y in x]for x in postpermutated]

    while True:
        if formatoutput(blanks, postpermutated) == -1:
            print("Congrats you won!")
            break
        print(word + ":\n")
        guess = input("Enter a guess: ")
        if guess == 'q':
            break
        elif len(guess) < low or len(guess) > high:
            print("\n" + "The guess does not fit within the range of (%d,%d)" % (low, high) + "\n")
        else:
            outer, inner = checklist(postpermutated, guess)
            if inner != -1:
                blanks[outer][inner] = guess
                print("Correct!" + "\n")
            else:
                print("Incorrect!" + "\n")

    for words in postpermutated:
        print(str(len(words[0])) + ": " + str(words))


if __name__ == "__main__":
    main()
