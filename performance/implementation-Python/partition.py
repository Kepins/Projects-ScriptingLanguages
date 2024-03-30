from typing import Tuple


def partition(in_str: str, partition_str: str) -> Tuple[str, str, str]:
    max_idx_partition = len(in_str) - len(partition_str)

    i = 0
    while i <= max_idx_partition:
        substr = in_str[i:i + len(partition_str)]
        if substr == partition_str:
            break
        i += 1

    if i <= max_idx_partition:
        return in_str[:i], partition_str, in_str[i + len(partition_str):]

    return in_str, "", ""
