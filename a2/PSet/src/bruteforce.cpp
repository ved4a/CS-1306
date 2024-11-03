#include "analyze.hpp"
#include "aes.hpp"  // Include the new AES header

int main(int argc, char* argv[]) {
    try {
        Analyze anal;
        anal.run(argc, argv);
    }
    catch (exception& e) {
        cerr << "exception caught\n" << e.what() << endl;
    }
    return 0;
}
