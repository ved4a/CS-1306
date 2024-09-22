#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 100

typedef struct {
    char ch;
    int index;
} KeyCharIndex;

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