import random
import time
from tkinter import *


class SortingVisualizer:
    def __init__(self, arr, speed):
        self.arr = arr
        self.n = len(arr)
        self.window = Tk()
        self.window.title("PopUpSort")
        self.window.geometry("600x450")
        self.window.resizable(False, False)  # disables resizing in both directions

        self.canvas = Canvas(self.window, width=600, height=400)
        self.canvas.pack()

        self.time_label = Label(self.window, text="Elapsed Time: 0.000s", fg="black", font=("Helvetica", 16))
        self.time_label.pack(side=BOTTOM)

        if self.n == 0:
            raise ValueError("Cannot visualize an empty array")

        self.draw_array(self.arr)
        self.speed = speed

        self.start_time = time.time()
        self.timer_stopped = False
        self.update_timer()

    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time

        if self.timer_stopped:
            self.time_label.config(fg='green2')
            return
        else:
            self.time_label.config(text="Elapsed Time: {:.3f}s".format(self.elapsed_time))
            self.window.after(10, self.update_timer)

    def draw_array(self, arr):
        self.canvas.delete("all")
        canvas_height = 350
        canvas_width = 600
        x_width = canvas_width / (self.n + 1)
        offset = (canvas_width - (self.n * x_width)) / 2  # calculate the starting point for the first rectangle
        spacing = 0
        normalized_arr = [i / max(self.arr) for i in self.arr]

        for i, height in enumerate(normalized_arr):
            x0 = i * x_width + offset + spacing
            y0 = canvas_height - height * 300
            x1 = (i + 1) * x_width + offset
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.canvas.create_text(x0 + 2, y0, anchor=SW, text=str(self.arr[i]))

        self.window.update()

    def bubble_sort(self):
        for i in range(self.n):
            for j in range(0, self.n - i - 1):
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                    self.draw_array(self.arr)
                    time.sleep(self.speed)
        self.completed()

    def insertion_sort(self):
        for i in range(1, self.n):
            key = self.arr[i]
            j = i - 1
            while j >= 0 and self.arr[j] > key:
                self.arr[j + 1] = self.arr[j]
                j -= 1
            self.arr[j + 1] = key
            self.draw_array(self.arr)
            time.sleep(self.speed)
        self.completed()

    def selection_sort(self):
        for i in range(self.n):
            min_idx = i
            for j in range(i + 1, self.n):
                if self.arr[j] < self.arr[min_idx]:
                    min_idx = j
            self.arr[i], self.arr[min_idx] = self.arr[min_idx], self.arr[i]
            self.draw_array(self.arr)
            time.sleep(self.speed)
        self.completed()

    def completed(self):
        self.timer_stopped = True
        self.canvas.delete("all")
        canvas_height = 350
        canvas_width = 600
        x_width = canvas_width / (self.n + 1)
        offset = (canvas_width - (self.n * x_width)) / 2  # calculate the starting point for the first rectangle
        spacing = 0
        normalized_arr = [i / max(self.arr) for i in self.arr]

        for i, height in enumerate(normalized_arr):
            x0 = i * x_width + offset + spacing
            y0 = canvas_height - height * 300
            x1 = (i + 1) * x_width + offset
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="green2")
            self.canvas.create_text(x0 + 2, y0, anchor=SW, text=str(self.arr[i]))

        self.window.update()
        self.window.mainloop()


def sort(arr, algorithm, speed):
    if algorithm.lower() == 'bubble sort' or algorithm.lower() == 'b':
        sv = SortingVisualizer(arr, speed)
        sv.bubble_sort()
    elif algorithm.lower() == 'selection sort' or algorithm.lower() == 's':
        sv = SortingVisualizer(arr, speed)
        sv.selection_sort()
    elif algorithm.lower() == 'insertion sort' or algorithm.lower() == 'i':
        sv = SortingVisualizer(arr, speed)
        sv.insertion_sort()


def sort_rand(size, min, max, algorithm, speed):
    arr = []
    for i in range(size):
        arr.append(random.randint(min, max))
    if algorithm.lower() == 'bubble sort' or algorithm.lower() == 'b':
        sv = SortingVisualizer(arr, speed)
        sv.bubble_sort()
    elif algorithm.lower() == 'selection sort' or algorithm.lower() == 's':
        sv = SortingVisualizer(arr, speed)
        sv.selection_sort()
    elif algorithm.lower() == 'insertion sort' or algorithm.lower() == 'i':
        sv = SortingVisualizer(arr, speed)
        sv.insertion_sort()
