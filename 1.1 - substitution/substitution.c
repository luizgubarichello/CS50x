#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    int keylen = strlen(key);

    if (keylen != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < keylen; i++)
    {
        key[i] = tolower(key[i]);
        if (!isalpha(key[i]))
        {
            printf("Key must have only letters.\n");
            return 1;
        }
        if (strchr(key, key[i]) != strrchr(key, key[i]))
        {
            printf("Key can't have duplicated letters.\n");
            return 1;
        }
    }

    string text = get_string("plaintext:  ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (islower(text[i]))
        {
            text[i] = tolower(key[text[i] - 97]);
        }
        else if (isupper(text[i]))
        {
            text[i] = toupper(key[text[i] - 65]);
        }
    }

    printf("ciphertext: %s\n", text);
    return 0;
}