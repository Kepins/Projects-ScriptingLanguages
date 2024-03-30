import random
import string


if __name__ == '__main__':
    MAX_LEN_STRING = 40

    n = int(input())

    pairs = set()
    lines = []

    generated = 0
    while generated < n:
        k = random.randint(1, MAX_LEN_STRING)
        str1 = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
        if generated % 3 == 0:
            str2 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, MAX_LEN_STRING)))
        else:
            partition_start = random.randint(0, k-1) if k > 1 else 0
            partition_end = random.randint(partition_start+1, k) if k > 1 else 1
            str2 = str1[partition_start:partition_end]
        if (str1, str2) not in pairs:
            pairs.add((str1, str2))
            lines.extend((str1, str2))
            generated += 1

    with open("data.in", "w") as file:
        file.write("\n".join(lines))
        file.write("\n")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
