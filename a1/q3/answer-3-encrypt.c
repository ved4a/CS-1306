#include <stdio.h>
#include <string.h>

#define MAX 100

int main(void){

    return 0;
}

void map_message_to_key(char *key, char *message)
{
    int key_len = strlen(key);
    int msg_len = strlen(message);

    // Create an array of arrays
    // One array for each letter in the key
    char key_arrays[key_len][MAX];
    int array_sizes[key_len];

    // Initialize arrays + size of arrays
    for (int i = 0; i < key_len; i++)
    {
        array_sizes[i] = 0;
    }

    // Map message letters into key arrays
    for (int i = 0; i < msg_len; i++)
    {
        int array_index = i % key_len;
        key_arrays[array_index][array_sizes[array_index]] = message[i];
        array_sizes[array_index]++;
    }

    // Print
    for (int i = 0; i < key_len; i++)
    {
        printf("%c = [", key[i]);
        for (int j = 0; j < array_sizes[i]; j++)
        {
            printf("%c", key_arrays[i][j]);
            if (j < array_sizes[i] - 1)
            {
                printf(", ");
            }
        }
        printf("]\n");
    }
}