#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

#include "partition.hpp"


int main(int argc, char* argv[]){
    std::ifstream file_in("data.in");
    std::ofstream file_out("data.out");
    std::string line;
    std::vector<std::string> in_strings;
    std::vector<std::string> partition_strings;
    
    if (!file_out.is_open() or !file_in.is_open()){
        exit(1);
    }
    int lineNumber = 0;
    while (std::getline(file_in, line)) {
        if (lineNumber % 2 == 0) {
            in_strings.push_back(line);
        } else {
            partition_strings.push_back(line);
        }
        lineNumber++;
    }
    file_in.close();

    // Get the results
    size_t minSize = std::min(in_strings.size(), partition_strings.size());
    std::string str1, str2, str3;
    for (size_t i = 0; i < minSize; ++i) {
        
        std::tie(str1, str2, str3) = partition(in_strings[i], partition_strings[i]);
        file_out << str1 << "\n" << str2 << "\n" << str3 << "\n";
    }
    file_out.close();
    

    // Time function calls
    auto start = std::chrono::high_resolution_clock::now();
    for (int i=0; i< 3750;i++){
        for (size_t i = 0; i < minSize; ++i) {
            partition(in_strings[i], partition_strings[i]);
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed_loop_with_calls = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    
    // Time loop
    start = std::chrono::high_resolution_clock::now();
    for (int i=0; i< 3750;i++){
        for (size_t i = 0; i < minSize; ++i) {
        }
    }
    end = std::chrono::high_resolution_clock::now();
    auto elapsed_loop = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << elapsed_loop_with_calls.count() - elapsed_loop.count() << '\n';
    return 0;
}