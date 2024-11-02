#include "aes.hpp"
#include "exception.hpp"
#include <pybind11/pybind11.h>

// Encrypts using AES-128/CBC/NoPadding.
void AES_128::encrypt(const ByteArray& plaintext, ByteArray& ciphertext) {
    ByteArray padded(plaintext);
    zeroPad(padded);

    // Convert key and iv to byte arrays
    const byte* keyBytes = key.data();
    const byte* ivBytes = iv.data();

    // Setup PyCryptodome AES cipher for encryption
    pybind11::module_ pyCrypto = pybind11::module_::import("Crypto.Cipher.AES");
    auto cipher = pyCrypto.attr("new")(pybind11::bytes((char*)keyBytes, key.size()),
                                        pyCrypto.attr("MODE_CBC"),
                                        pybind11::bytes((char*)ivBytes, iv.size()));

    // Encrypt
    auto encrypted_data = cipher.attr("encrypt")(pybind11::bytes((char*)padded.data(), padded.size()));
    ciphertext = ByteArray(reinterpret_cast<const byte*>(encrypted_data.cast<std::string>().data()), encrypted_data.size());
}

// Decrypts using AES-128/CBC/NoPadding.
void AES_128::decrypt(const ByteArray& ciphertext, ByteArray& plaintext) {
    // Convert key and iv to byte arrays
    const byte* keyBytes = key.data();
    const byte* ivBytes = iv.data();

    // Setup PyCryptodome AES cipher for decryption
    pybind11::module_ pyCrypto = pybind11::module_::import("Crypto.Cipher.AES");
    auto cipher = pyCrypto.attr("new")(pybind11::bytes((char*)keyBytes, key.size()),
                                        pyCrypto.attr("MODE_CBC"),
                                        pybind11::bytes((char*)ivBytes, iv.size()));

    // Decrypt
    auto decrypted_data = cipher.attr("decrypt")(pybind11::bytes((char*)ciphertext.data(), ciphertext.size()));
    plaintext = ByteArray(reinterpret_cast<const byte*>(decrypted_data.cast<std::string>().data()), decrypted_data.size());

    zeroUnPad(plaintext);
}

// Padding to the next 16-byte block
void AES_128::zeroPad(ByteArray& plaintext) {
    while (plaintext.size() % blockSize != 0) {
        plaintext.push_back(0);
    }
}

// Remove padding
void AES_128::zeroUnPad(ByteArray& plaintext) {
    while (plaintext.size() > 0 && plaintext.back() == 0) {
        plaintext.pop_back();
    }
}
