import math

arr = [3, 6, 1, 9, 50, 30, 9, 52]
arr1 = [1, 3, 6, 9, 9, 30, 50, 52]

def sort_up(data):
    # flag = True
    for i in range(0, len(data)):
        # flag = False
        for j in range(0, len(arr) - 1 - i):
            # if (len(arr) - 1 - i) - j == 1:
            #     break
            if data[j] > data[j+1]:
                temp = data[j]
                data[j] = data[j+1]
                data[j+1] = temp
                # flag = True
    print(data)



def find_half(data, value):
    low = 0
    high = len(data) - 1

    while low <= high:
        mid = math.floor((low + high) / 2)
        if value == data[mid]:
            return mid
        elif value < data[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return -1


if __name__ == '__main__':
    sort_up(arr)
    print(find_half(arr1, 30))

