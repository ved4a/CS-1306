#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 100

void map_message_to_key(char *key, char *message);
void swap(char *a, char *b);
void sort_string(char str[]);
void print_sorted_key_arrays(char *key, char key_arrays[][MAX], int *array_sizes, int key_len);
void to_uppercase(char str[]);
void sort_key_with_indices(char *key, KeyCharIndex sorted_key[], int key_len);

// Define a structure to store both key character and its original index
typedef struct {
    char ch;
    int index;
} KeyCharIndex;

int main(void){
     char key[MAX], message[MAX];

     // Input the key and message
    printf("Enter the key (e.g., HACK): ");
    scanf("%s", key);

    printf("Enter the message (e.g., HELLOWORLD): ");
    scanf("%s", message);

    // Convert to uppercase for consistency
    to_uppercase(key);
    to_uppercase(message);


    // Map the message to the key arrays
    map_message_to_key(key, message);

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

    print_sorted_key_arrays(key, key_arrays, array_sizes, key_len);
}

void swap(char *a, char *b)
{
    char temp = *a;
    *a = *b;
    *b = temp;
}

void sort_string(char str[])
{
    int n = strlen(str);

    // Implementing bubble sort
    for (int i = 0; i < n -1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (str[j] > str[j + 1])
            {
                swap(&str[j], &str[j + 1]);
            }
        }
    }
}

void to_uppercase(char str[])
{
    int len = strlen(str);
    for (int i = 0; i < len; i++)
    {
        str[i] = toupper(str[i]);
    }
}

void print_sorted_key_arrays(char *key, char key_arrays[][MAX], int *array_sizes, int key_len) {
    // Array to hold the sorted key along with their original indices
    KeyCharIndex sorted_key[key_len];

    // Populate the array with the characters from the key and their original indices
    for (int i = 0; i < key_len; i++) {
        sorted_key[i].ch = key[i];
        sorted_key[i].index = i;
    }

    // Sort the array based on the characters, but keep their original indices
    sort_key_with_indices(key, sorted_key, key_len);

    // Print the arrays according to the sorted key and their original indices
    for (int i = 0; i < key_len; i++) {
        int original_index = sorted_key[i].index;
        printf("%c : ", sorted_key[i].ch);
        for (int j = 0; j < array_sizes[original_index]; j++) {
            printf("%c", key_arrays[original_index][j]);
        }
        printf("\n");
    }
}
