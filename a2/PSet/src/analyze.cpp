/*
 * analyze.cpp
 *
 *  Created on: Jan 23, 2010
 *      Author: mike
 */

#include <iostream>
#include <cfloat>
#include <cmath>
using namespace std;
#include "aes.hpp"
#include "analyze.hpp"
#include "exception.hpp"

using namespace std;

//-------------------------------------------------------------------
Analyze::Analyze() :
    key(AES_128::keyLength), iv(AES_128::blockSize) {
    for (unsigned k = 0; k < NUM_KEY_SHARES; k++)
        keyShare[k].resize(AES_128::keyLength);
}

//-------------------------------------------------------------------
void Analyze::run(int argc, char* argv[]) {
    if (argc != 5) {
        cout << "usage: " << argv[0] << " freq key in out" << endl;
        return;
    }
    char* freqFile = argv[1];
    char* keyFile = argv[2];
    char* inFile = argv[3];
    char* outFile = argv[4];

    // Get the distribution
    dist.readFreq(freqFile);

    // Get the key shares
    readKeySharesFile(keyFile);

    // Get the iv and ciphertext
    readIVCiphertext(inFile);

    cout << "IV:\n";
    iv.writeHex(cout) << endl;

    // Guess the key
    guessKey();

    // Check that the key works
    cipher.setKey(key);
    cipher.decrypt(ciphertext, plaintext);

    // Print results
    cout << "Guessed key:\n";
    cout << "Indices " << keyIndex1 << " and " << keyIndex2 << endl;
    key.writeHex(cout) << endl;

    // Write the plaintext to the output file
    ofstream out(outFile);
    if (!out)
        throw CryptoException(
                "bruteforce: can't open plaintext file for writing");
    out << plaintext;
    out.close();
}
//-------------------------------------------------------------------
void Analyze::guessKey() {
    double minDivergence = DBL_MAX;  // Start with the maximum possible value
    unsigned bestIdx1 = 0, bestIdx2 = 1; // Initialize best indices

    // Iterate over all pairs of key indices (idx1, idx2)
    for (unsigned idx1 = 0; idx1 < NUM_KEY_SHARES; ++idx1) {
        for (unsigned idx2 = idx1 + 1; idx2 < NUM_KEY_SHARES; ++idx2) {
            // Compute the master key by XORing the two key shares
            key = keyShare[idx1] ^ keyShare[idx2];

            // Decrypt the ciphertext using the master key
            cipher.setKey(key);
            ByteArray decrypted;
            cipher.decrypt(ciphertext, decrypted);

            // Calculate the divergence
            double currentDivergence = divergence(decrypted);
            
            // Check if this divergence is the smallest we have found
            if (currentDivergence < minDivergence) {
                minDivergence = currentDivergence;
                bestIdx1 = idx1;
                bestIdx2 = idx2;
            }
        }
    }

    // Store the best key indices found
    keyIndex1 = bestIdx1;
    keyIndex2 = bestIdx2;
}

//-------------------------------------------------------------------
double Analyze::divergence(const ByteArray& s) const {
    double q[ALPHABETSIZE] = {0}; // Frequency distribution of the decrypted message
    double totalBytes = s.size();

    // Calculate frequencies for the decrypted message
    for (unsigned char byte : s) {
        if (byte < ALPHABETSIZE) {
            q[byte]++;
        }
    }

    // Normalize the frequency distribution for the decrypted message
    for (int i = 0; i < ALPHABETSIZE; ++i) {
        q[i] /= totalBytes;
    }

    // Calculate the divergence between the reference distribution and the decrypted message
    double totalDivergence = 0.0;
    for (int b = 0; b < ALPHABETSIZE; ++b) {
        totalDivergence += (dist.prob[b] - q[b]) * (dist.prob[b] - q[b]);
    }

    return totalDivergence; // Return the calculated divergence
}


//-------------------------------------------------------------------
// Read key from file
void Analyze::readKeySharesFile(const char* keyFile) {
    ifstream in(keyFile);
    if (!in)
        throw CryptoException("analyze: can't open key file");
    for (unsigned k = 0; k < NUM_KEY_SHARES; k++)
        keyShare[k].readHex(in);
    in.close();
}

//-------------------------------------------------------------------
// Read IV and ciphertext from file
void Analyze::readIVCiphertext(const char* inFile) {
    ifstream in(inFile);
    if (!in)
        throw CryptoException(
                "analyze: can't open ciphertext file for reading");
    iv.readBytes(in);
    ciphertext.readAllBytes(in);
    in.close();
}
