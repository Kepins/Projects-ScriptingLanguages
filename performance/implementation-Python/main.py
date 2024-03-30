import time

from partition import partition


if __name__ == "__main__":
    with open("data.in", "r") as file:
        file_content = file.read().splitlines()
        cases = list(zip(file_content[::2], file_content[1::2]))

    # Get the results and append to list
    results = []
    for case in cases:
        results.append(partition(*case))

    with open("data.out", "w") as file:
        # Each item of a tuple is in newline
        file.write("\n".join([string for result in results for string in result]))

    N = 3800

    # Time function calls
    start = time.perf_counter_ns()
    for i in range(N):
        for case in cases:
            partition(*case)
    end = time.perf_counter_ns()
    time_loop_with_calls = end - start

    # Time loop
    start = time.perf_counter_ns()
    for i in range(N):
        for case in cases:
            pass
    end = time.perf_counter_ns()
    time_loop = end - start

    print((time_loop_with_calls - time_loop)/10**9)
