import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import sys
import math


# Draw func
def draw_plot(a, b, step):
    fig = plt.figure()

    # X/Y Axis
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    x_arr, y_arr = [], []
    for i in range(round((b - a) / step)):
        x_arr.append(a + step * i)

    try:
        y_arr = [func_executable(x) for x in x_arr]
    except ZeroDivisionError:
        y_arr = [func_executable(x) if x != 0 else math.inf for x in x_arr]

    plt.plot(x_arr, y_arr)

    for root in roots:
        plt.plot(*root, marker="o", markersize=7, markerfacecolor="red")
        plt.text(root[0], 0.1 * (max(y_arr) - min(y_arr)) + root[1],
                 f"{root[0]},\n{root[1]}",
                 horizontalalignment='right' if root[0] < 0 else 'left',
                 verticalalignment='center')

    global_min = round(minimize_func(x_arr[0]), len(str(step)))
    func_global_min = round(func_executable(global_min), len(str(step)))
    plt.plot(global_min, func_global_min, marker="o", markersize=7, markerfacecolor="orange")
    plt.text(global_min, func_global_min,
             f'{global_min},\n{func_global_min}',
             horizontalalignment='right',
             verticalalignment='center')

    knee_points = find_knee_points(x_arr, y_arr)

    for point in knee_points:
        plt.plot(*point, marker="o", markersize=7, markerfacecolor="green")
        plt.text(point[0], 0.1 * (max(y_arr) - min(y_arr)) + point[1],
                 f"{point[0]},\n{point[1]}",
                 horizontalalignment='right' if point[0] < 0 else 'left',
                 verticalalignment='center')

    plt.show()


def minimize_func(left_border):
    return opt.minimize(func_executable, left_border).x[0]


def find_knee_points(x_arr, y_arr):
    knee_points = []
    knee_status = ''

    for i in range(1, len(y_arr)):
        y = y_arr[i]
        y_prev = y_arr[i - 1]

        if i == 1:
            if y > y_prev:
                knee_status = 'up'
            elif y < y_prev:
                knee_status = 'down'
            else:
                knee_status = 'lin'
        else:
            if knee_status != 'up' and y > y_prev:
                knee_status = 'up'
                knee_points.append((x_arr[i], y))
            elif knee_status != 'down' and y < y_prev:
                knee_status = 'down'
                knee_points.append((x_arr[i], y))
            elif knee_status != 'lin' and y == y_prev:
                knee_status = 'lin'
                knee_points.append((x_arr[i], y))
        if y_prev == math.inf:
            knee_points.pop()

    return knee_points


# Get func root by Brent method
def get_root(a, b, n_max, eps):
    error_code = 0
    root, data = 'None', {}
    iter_index = 0
    try:
        for iter_index in range(n_max):
            root, data = opt.brentq(func_executable, a, b, maxiter=n_max, xtol=eps, full_output=True)

            if data.converged:
                return data.root, iter_index, error_code
            else:
                error_code = 3
                return data.root, iter_index, error_code
    except RuntimeError as re:
        error_code = 1
        return root, n_max, error_code

    except ZeroDivisionError as ze:
        error_code = 3
        return 0, iter_index, error_code

    except ValueError:
        error_code = 4
        return root, iter_index, error_code


# Create function from equation
def func_executable(x):
    return eval(fr'{func}')


# Request data from user
def get_input():
    while True:
        try:
            global func
            func = input('Type function: ')
            a, b = tuple(map(float, input('Type left and right border of interval, separated by space: ').split()))
            step = float(input('Type step: '))
            n_max = int(input('Type iteration limit: '))
            eps = float(input('Type precision: '))
        except ValueError as ve:
            print(f'\n\tCan\'t convert string to float', file=sys.stderr)
            continue
        break

    return a, b, step, n_max, eps


# Print help message
def print_help():
    print('\nError codes:\n'
          '     0 - Root found in interval\n'
          '     1 - Iterations limit\n'
          '     2 - Zero Division\n'
          '     3 - F(a) and F(b) must have different signs\n'
          '\nTable format:\n'
          '| № | Interval [] | Root | F(Root) | Iterations | Error code |')


def main(is_test=False, test_id=0):
    if not is_test:
        a, b, step, n_max, eps = get_input()
    else:
        global func
        func = tests[test_id][0]
        a, b, step, n_max, eps = tests[test_id][1:]
        print(f">> {func}")

    print_help()

    index = 0
    steps_count = 0
    left = float(round(a, len(str(step))))
    right = float(round(a + step, len(str(step))))
    while True:

        steps_count += 1
        if a + step * steps_count > b + 0.1 * step:
            break
        data = get_root(left, right, n_max, eps)

        index += 1

        root, iterations, error_code = data
        if root != 'None':
            global roots
            func_value = round(func_executable(root), len(str(step))) if error_code != 3 else math.inf
            root = round(root, len(str(step)))
            roots.append((root, func_value))
        else:
            func_value = 'None'

        print(
            f'|{index:>3}|[{left:<5},{right:>5}]|{root:^6}|{func_value:^9}|{iterations:^12}|{error_code:^12}|')

        left = round(left + step, 6)
        right = round(right + step, 6)

    draw_plot(a, b, step)


if __name__ == '__main__':
    roots = []
    tests = {
        0: ["x**2 - 1",
            -3, 3, 0.75, 100, 0.01],
        1: ["x**2 - 1",
            -3, 3, 0.1, 100, 0.01],
        2: ["1/x -7 + x*x + 1/(x*x)",
            -6, 6, 0.1, 10000, 0.01],
        3: ["1/x -7 + x*x + 1/(x*x)",
            -6, 6, 0.2, 10000, 0.01],
        4: ["1/x -7 + x*x + 1/(x*x)",
            -6, 6, 1, 10000, 0.1],
    }
    main(is_test=True, test_id=1)
