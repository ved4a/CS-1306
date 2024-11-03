#pragma once

#include <iostream>
using namespace std;

#define ALPHABETSIZE 256

class Distribution {
private:
    double prob[ALPHABETSIZE];
public:
    Distribution() {}
    void readFreq(const char* freqFile);
    const double operator[] (int k) const { return prob[k]; }
    const double* getProb() const { return prob; } // Add this line
    ostream& print(ostream& out) const;
};

inline ostream& operator<<(ostream& out, Distribution& dist) {
    return dist.print(out);
}
