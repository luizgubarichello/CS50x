from cs50 import get_string

# index = 0.0588 * L - 0.296 * S - 15.8
# where L is the average number of letters per 100 words in the text,
# and S is the average number of sentences per 100 words in the text.

text = get_string("Text: ")

letters = sentences = 0
words = 1

for i, char in enumerate(text):
    end = ["?", "!", "."]
    if char.isalpha():
        letters+=1
    if text[i] == " ":
        if text[i-1] != " " and text[i+1] != " ":
            words+=1
    if text[i] in end:
        if text[i-1] not in end:
            sentences+=1

grade = (0.0588 * (100 * letters / words)) - (0.296 * (100 * sentences / words)) - 15.8
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade:.0f}")