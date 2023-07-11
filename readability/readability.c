#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    int sentences, words, letters;
    float grade;

    // index = 0.0588 * L - 0.296 * S - 15.8
    // where L is the average number of letters per 100 words in the text,
    // and S is the average number of sentences per 100 words in the text.

    string text = get_string("Text: ");
    letters = count_letters(text);
    words = count_words(text);
    sentences = count_sentences(text);
    grade = (0.0588 * (100 * (float) letters / words)) - (0.296 * (100 * (float) sentences / words)) - 15.8;
    grade = round(grade);
    if (grade < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    if (grade >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    printf("Grade %.0f\n", grade);
    return 0;
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char letter = tolower(text[i]);
        if (islower(letter))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            if (text[i - 1] != 32 && text[i + 1] != 0)
            {
                words++;
            }
        }
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            if (text[i - 1] != 33 && text[i - 1] != 46 && text[i - 1] != 63)
            {
                sentences++;
            }
        }
    }
    return sentences;
}