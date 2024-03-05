#include "partition.hpp"
#include <iostream>


std::tuple<std::string, std::string, std::string> partition(const std::string& inStr, const std::string partitionStr){
    const long max_idx_partition = inStr.length() - partitionStr.length();

    long i = 0;
    while(i <= max_idx_partition){
        const std::string substr = inStr.substr(i, partitionStr.length());
        if (substr == partitionStr){
            break;
        }
        ++i;
    }

    if (i <= max_idx_partition){
        return std::make_tuple(inStr.substr(0, i), partitionStr, inStr.substr(i + partitionStr.length()));
    }

    return std::make_tuple(inStr, "", "");
}