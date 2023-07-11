#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover infile\n");
        return 1;
    }

    char *infile = argv[1];

    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }

    typedef uint8_t BYTE;

    const int BLOCK_SIZE = 512;

    BYTE *buffer = malloc(BLOCK_SIZE);

    char output[8];

    int jpeg_num = -1;

    FILE *img = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, inptr) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(jpeg_num >= 0)
            {
                fclose(img);
            }
            jpeg_num++;
            sprintf(output, "%03i.jpg", jpeg_num);
            img = fopen(output, "w");
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
        else
        {
            if (jpeg_num >= 0)
            {
                fwrite(buffer, 1, BLOCK_SIZE, img);
            }
        }
    }

    free(buffer);
    fclose(inptr);
    fclose(img);
    return 0;
}