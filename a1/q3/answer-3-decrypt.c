#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 100

typedef struct {
    char ch;
    int index;
} KeyCharIndex;

void decrypt_message(char *key, char *ciphertext);
void to_uppercase(char str[]);

int main(void)
{
    char key[MAX], ciphertext[MAX];

    // Input the key and ciphertext
    printf("Enter the key (e.g., HACK): ");
    fgets(key, MAX, stdin);
    key[strcspn(key, "\n")] = '\0';

    printf("Enter the ciphertext: ");
    fgets(ciphertext, MAX, stdin);
    ciphertext[strcspn(ciphertext, "\n")] = '\0';

    return 0;
}

void decrypt_message(char *key, char *ciphertext)
{
    int key_len = strlen(key);
    int cipher_len = strlen(ciphertext);

    // Array to store the sorted key with original indices
    KeyCharIndex sorted_key[key_len];

    // Populate the sorted_key array with key characters and their original indices
    for (int i = 0; i < key_len; i++) {
        sorted_key[i].ch = key[i];
        sorted_key[i].index = i;
    }

    // Sort the key while keeping track of the original indices
    sort_key_with_indices(key, sorted_key, key_len);

    // Calculate the number of full columns and how many characters in the last incomplete column
    int full_col_size = cipher_len / key_len;
    int extra_chars = cipher_len % key_len;

    // Create an array of arrays to store the transposed columns
    char transposed[key_len][MAX];
    int array_sizes[key_len];

    // Fill transposed arrays based on the sorted key
    int current_char = 0;
    for (int i = 0; i < key_len; i++) {
        int original_index = sorted_key[i].index;

        // Determine how many characters this column will have
        int col_size = full_col_size + (original_index < extra_chars ? 1 : 0);

        // Fill the column with characters from the ciphertext
        for (int j = 0; j < col_size; j++) {
            transposed[original_index][j] = ciphertext[current_char++];
        }

        array_sizes[original_index] = col_size;
    }

    // Reconstruct the original message by reading row-wise from the columns
    printf("Decrypted message: ");
    for (int row = 0; row < full_col_size + 1; row++) {
        for (int col = 0; col < key_len; col++) {
            if (row < array_sizes[col]) {
                printf("%c", transposed[col][row]);
            }
        }
    }
    printf("\n");
}

void to_uppercase(char str[])
{
    int len = strlen(str);
    for (int i = 0; i < len; i++)
    {
        str[i] = toupper(str[i]);
    }
}