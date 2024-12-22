# Task 0: Prepare showcase of synchronous filter function adaptation

def sync_filter(func, arr):
    result = []
    for item in arr:
        if func(item):
            result.append(item)
    return result


def is_upper(word):
    return type(word) is str and word.isupper()


def is_two_power(num):
    if type(num) is not int or num <= 0:
        return False
    return (num & (num - 1)) == 0


def is_even(num):
    return type(num) is int and num % 2 == 0


def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]
    print("Filtering uppercase strings from list1:")
    print(sync_filter(is_upper, list1))
    print("Filtering powers of two from list2:")
    print(sync_filter(is_two_power, list2))
    print("Filtering even numbers from list3:")
    print(sync_filter(is_even, list3))


if __name__ == "__main__":
    main()
