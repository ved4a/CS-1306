#pragma once
#include "bytearray.hpp"
using namespace std;

class AES_128 {
public:
    static const unsigned int keyLength = 16;
    static const unsigned int blockSize = 16;
private:
    ByteArray key;  // Store the key directly
    ByteArray iv;   // Store the IV directly

public:
    AES_128() {}
    void encrypt(const ByteArray& plaintext, ByteArray& ciphertext);
    void decrypt(const ByteArray& ciphertext, ByteArray& plaintext);
    void zeroPad(ByteArray& plaintext);
    void zeroUnPad(ByteArray& plaintext);

    void setKey(const ByteArray& keyData) {
        if (keyData.size() != keyLength)
            throw CryptoException("Key must be 16 bytes for AES-128.");
        key = keyData;
    }
    void setIV(const ByteArray& ivData) {
        if (ivData.size() != blockSize)
            throw CryptoException("IV must be 16 bytes for AES-128 CBC.");
        iv = ivData;
    }
};
