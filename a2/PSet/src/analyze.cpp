#include <iostream>
#include <cfloat>
#include <cmath>
#include "aes.hpp"
#include "analyze.hpp"
#include "exception.hpp"

using namespace std;

Analyze::Analyze() : key(AES_128::keyLength), iv(AES_128::blockSize) {
    cipher = AES_128();  // Initialize AES cipher object
    for (unsigned k = 0; k < NUM_KEY_SHARES; k++) {
        keyShare[k].resize(AES_128::keyLength);
    }
}

void Analyze::run(int argc, char* argv[]) {
    if (argc != 5) {
        cout << "usage: " << argv[0] << " freq key in out" << endl;
        return;
    }
    char* freqFile = argv[1];
    char* keyFile = argv[2];
    char* inFile = argv[3];
    char* outFile = argv[4];

    dist.readFreq(freqFile);           // Read distribution
    readKeySharesFile(keyFile);        // Read key shares
    readIVCiphertext(inFile);          // Read IV and ciphertext

    cout << "IV:\n";
    iv.writeHex(cout) << endl;

    // Guess the key
    guessKey();

    // Set guessed key and IV in cipher
    cipher.setKey(key);
    cipher.setIV(iv);

    // Decrypt ciphertext with guessed key
    cipher.decrypt(ciphertext, plaintext);

    cout << "Guessed key:\n";
    cout << "Indices " << keyIndex1 << " and " << keyIndex2 << endl;
    key.writeHex(cout) << endl;

    // Write decrypted plaintext to output file
    ofstream out(outFile);
    if (!out) {
        throw CryptoException("bruteforce: can't open plaintext file for writing");
    }
    out << plaintext;
    out.close();
}

void Analyze::guessKey() {
    double minDivergence = DBL_MAX;
    unsigned bestIdx1 = 0, bestIdx2 = 1;

    for (unsigned idx1 = 0; idx1 < NUM_KEY_SHARES; ++idx1) {
        for (unsigned idx2 = idx1 + 1; idx2 < NUM_KEY_SHARES; ++idx2) {
            key = keyShare[idx1] ^ keyShare[idx2];

            cipher.setKey(key);
            ByteArray decrypted;
            cipher.decrypt(ciphertext, decrypted);

            double currentDivergence = divergence(decrypted);

            if (currentDivergence < minDivergence) {
                minDivergence = currentDivergence;
                bestIdx1 = idx1;
                bestIdx2 = idx2;
            }
        }
    }

    keyIndex1 = bestIdx1;
    keyIndex2 = bestIdx2;
}

double Analyze::divergence(const ByteArray& s) const {
    double q[ALPHABETSIZE] = {0};
    double totalBytes = s.size();

    for (unsigned char byte : s) {
        if (byte < ALPHABETSIZE) {
            q[byte]++;
        }
    }

    for (int i = 0; i < ALPHABETSIZE; ++i) {
        q[i] /= totalBytes;
    }

    // Access prob via the getter method
    const double* prob = dist.getProb();
    double totalDivergence = 0.0;
    for (int b = 0; b < ALPHABETSIZE; ++b) {
        totalDivergence += (prob[b] - q[b]) * (prob[b] - q[b]);
    }

    return totalDivergence;
}


void Analyze::readKeySharesFile(const char* keyFile) {
    ifstream in(keyFile);
    if (!in) {
        throw CryptoException("analyze: can't open key file");
    }
    for (unsigned k = 0; k < NUM_KEY_SHARES; k++) {
        keyShare[k].readHex(in);
    }
    in.close();
}

void Analyze::readIVCiphertext(const char* inFile) {
    ifstream in(inFile);
    if (!in) {
        throw CryptoException("analyze: can't open ciphertext file for reading");
    }
    iv.readBytes(in);
    ciphertext.readAllBytes(in);
    in.close();
}
