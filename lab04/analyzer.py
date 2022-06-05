# Дано множество точек на плоскости. Найти треугольник, для которого разность площадей треугольников,
# образованных делением одной из биссектрис, будет минимальна.

from itertools import combinations

def get_triangles(dot_list: list[tuple]):
    return combinations(dot_list, 3);

eps = 0.000001

dots = [(1, 1), (2, 2), (1, -1), (-4, 2)]

# def is_on_line(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]):
#     x = y = 0.0
#     if not (abs(b[0] - a[0]) < eps):
#         x = ((c[0] - a[0]) / (b[0] - a[0]))
#     if not (abs(b[1] - a[1]) < eps):
#         y = ((c[1] - a[1]) / (b[1] - a[1]))
#
#     res = False
#     if abs(x - y) < eps:
#         res = True
#
#     return res

# def find_triangles(dots: list):
#     pass
