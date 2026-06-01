import matplotlib.pyplot as plt
import numpy as np
import time

# 冒泡排序可视化
def bubble_sort_visualize(arr):
    arr = arr.copy()
    n = len(arr)
    plt.ion()
    fig, ax = plt.subplots()
    bars = ax.bar(range(n), arr, color='blue')
    ax.set_title("Bubble Sort Visualization")

    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                for bar, height in zip(bars, arr):
                    bar.set_height(height)
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(0.1)
    plt.ioff()
    plt.show()
    return arr

# 二分查找
def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left+right)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid+1
        else:
            right = mid-1
    return -1

# 主程序
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    sorted_data = bubble_sort_visualize(data)
    print("Sorted:", sorted_data)

    target = 25
    idx = binary_search(sorted_data, target)
    print(f"Found {target} at index {idx}")