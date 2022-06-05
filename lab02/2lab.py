import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import matplotlib.pyplot as plt
import sympy as sym
import numpy as np
from math import *

def is_num(s):
    s = str(s)
    try:
        if s.isdigit():
            return True
    except:
        pass
    else:
        d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-', 'e']
        cond = True
        for i in s:
            if i not in d:
                cond = False
        if s.count(".") > 1 or s.count("-") > 2:
            cond = False
        if s == '':
            cond = False
        return cond


def clear_table(tree):
    for item in tree.get_children():
        tree.delete(item)


def create_table(tree, elem_seg, roots, f_roots, iters, errors):
    table = [(i + 1,
              f"[{(str(elem_seg[i][0]))}; {str(elem_seg[i][1])}]",
              f"{roots[i]:.3f}" if is_num(roots[i]) else str(roots[i]),
              f"{f_roots[i]:.4g}" if is_num(f_roots[i]) else str(f_roots[i]),
              str(iters[i]),
              errors[i]) for i in range(len(roots))]
    for index, val in enumerate(table):
        tree.insert(parent='', index='end', iid=index, values=val)


def check_value(name, val):
    if name == 'float':
        try:
            return float(val)
        except BaseException:
            return None
    elif name == 'int':
        try:
            return int(val)
        except BaseException:
            return None
    else:
        return val


def calc_button(tree, action, func, a, b, h, EPS, Nmax):
    if not all(map(lambda x: len(x), [func, a, b, h, EPS, Nmax])):
        mbox.showerror(title='Ошибка ввода', message='Есть пустая строка')
        return
    try:
        a, b, h, EPS, Nmax = float(a), float(
            b), float(h), float(EPS), int(Nmax)
        elem_seg, roots, f_roots, iters, errors = simple_iterations(
            func, a, b, h, EPS, Nmax)
        if action == 'table':
            clear_table(tree)
            create_table(tree, elem_seg, roots, f_roots, iters, errors)
        elif action == 'graph':
            out_window_matplotlib(func, a, b)
    except Exception as ex:
        mbox.showerror(title='Ошибка ввода', message=f'Некорректный ввод, {ex}')
        return


# подставить вместо x значение val
def calc_func(func, val):
    try:
        x = val
        return eval(func)
    except ZeroDivisionError:
        return inf


# значение в производной ф-ции
def deriv_func(func, n):
    x = sym.Symbol('x')
    return sym.diff(func, x, n)


def check_errors(a, b, f, deriv_f):
    if not deriv_f(b):
        return 'Производная равна 0'
    if f(a) * f(b) > 0:
        return 'Одинаковые знаки f(x)'
    return '-'


def simple_iterations(func, a, b, h, EPS, Nmax):
    x = sym.Symbol('x')
    func, a, b, EPS, Nmax, h = func, float(
        a), float(b), float(EPS), int(Nmax), float(h)
    roots = []
    f_roots = []
    seg = [a, b]
    elem_seg = []
    iters = []
    errors = []

    a = seg[0]
    b = seg[0] + h
    f = sym.lambdify(x, func)
    g = sym.lambdify(x, func + " + x")
    deriv_f = sym.lambdify(x, deriv_func(func, 1))
    deriv_g = sym.lambdify(x, deriv_func(func + " + x", 1))
    while a < seg[1]:
        a = round(a, 5)
        b = round(b, 5)
        elem_seg.append([a, b])
        iteration = 0

        errors.append(check_errors(a, b, f, deriv_f))
        if errors[-1] == '-' and (abs(deriv_g(a)) < 1 or abs(deriv_g(b)) < 1):
            root_cur_g = g(a) if abs(
                deriv_g(a)) < abs(deriv_g(b)) else g(b)
            root_cur = a if abs(
                deriv_g(a)) < abs(deriv_g(b)) else b
            root_prev = 0
            while abs(root_cur - root_prev) >= EPS and iteration <= Nmax:
                iteration += 1
                root_prev = root_cur
                g = sym.lambdify(x, func + " + x")
                deriv_g = sym.lambdify(x, deriv_func(func + " + x", 1))
                root_cur = root_cur_g
                root_cur_g = g(root_cur_g)
            roots.append(root_cur)
            f_roots.append(calc_func(func, root_cur))
        else:
            t = ""
            if deriv_g(a) > 1 and deriv_g(b) > 1 and (f(a) * f(b)) < 0:
                t = "Метод простых итераций расходится"
            roots.append(t if t else 'f(x) != 0')
            f_roots.append(t if t else 'f(x) != 0')
        iters.append(iteration)
        a += h
        b += h
        if b > seg[1]:
            b = seg[1]

    return elem_seg, roots, f_roots, iters, errors


def out_window_matplotlib(func, a, b):
    x = sym.Symbol('x')
    f = sym.lambdify(x, func)
    deriv_f = sym.lambdify(x, deriv_func(func, 1))
    deriv_f2 = sym.lambdify(x, deriv_func(func, 2))
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(func)
    SIZE_X = 1000
    x_graph = np.linspace(a, b, SIZE_X)
    y_graph = np.array(list(map(lambda x: calc_func(func, x), x_graph)))
    last_point = None

    for point in x_graph:
        if last_point is None:
            last_point = point
        else:
            if f(last_point) * f(point) < 0:
                plt.plot(point, f(point), 'gx', ms=7, mew=3)
            if deriv_f(last_point) * deriv_f(point) <= 0:
                plt.plot(point, f(point), 'r*', ms=5, mew=3)
            if deriv_f2(last_point) * deriv_f2(point) < 0:
                plt.plot(point, f(point), 'b*', ms=5, mew=3)
            last_point = point

    plt.plot(inf, inf, 'gx', ms=7, mew=3, label='Корень')
    plt.plot(inf, inf, 'r*', ms=5, mew=3, label='Точка экстремума')
    plt.plot(inf, inf, 'b*', ms=5, mew=3, label='Точка перегиба')
    plt.legend(fontsize=10,
               ncol=1,  # количество столбцов
               facecolor='oldlace',  # цвет области
               edgecolor='r',  # цвет крайней линии
               title='Обозначения:',  # заголовок
               title_fontsize='5',  # размер шрифта заголовка
               numpoints=1,
               )
    plt.plot(x_graph, y_graph)
    plt.show()


# tkinter -----------
needed_data = ['Функция:', 'a:', 'b:', 'h:', 'eps:', 'Nmax:']
root = tk.Tk()
root.title('Метод простых итераций;')
InputFrame = tk.Frame(root)
TableFrame = tk.Frame(root, bg='blue')

for index, word in enumerate(needed_data):
    tk.Label(
        master=InputFrame,
        text=word,
        font="Arial 30",
        justify=tk.LEFT).grid(
        row=index,
        sticky=tk.E)

func = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=func,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=0,
    column=1)
a = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=a,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=1,
    column=1)
b = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=b,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=2,
    column=1)
h = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=h,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=3,
    column=1)
eps = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=eps,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=4,
    column=1)
Nmax = tk.StringVar()
tk.Entry(
    master=InputFrame,
    textvariable=Nmax,
    width=10,
    font=(
        "default",
        30),
    relief=tk.GROOVE,
    borderwidth=3).grid(
    row=5,
    column=1)

tree = ttk.Treeview(
    show='headings',
    columns=(
        '#1',
        '#2',
        '#3',
        '#4',
        '#5',
         '#6'))
tree.heading('#1', text='№ корня')
tree.heading('#2', text='[Xi:Xi+1]')
tree.heading('#3', text='x\'')
tree.heading('#4', text='f(x\')')
tree.heading('#5', text='Количество итераций')
tree.heading('#6', text='Код ошибки')

button_for_calc = tk.Button(
    master=InputFrame,
    width=22,
    text='Посчитать',
    command=lambda: calc_button(
        tree,
        'table',
        func.get(),
        a.get(),
        b.get(),
        h.get(),
        eps.get(),
        Nmax.get())).grid(
            row=6,
            column=1,
            columnspan=2,
            ipady=7,
            ipadx=5,
    pady=3)
button_for_graph = tk.Button(
    master=InputFrame,
    width=22,
    text='График',
    command=lambda: calc_button(
        tree,
        'graph',
        func.get(),
        a.get(),
        b.get(),
        h.get(),
        eps.get(),
        Nmax.get())).grid(
            row=7,
            column=1,
            columnspan=2,
            ipady=7,
            ipadx=5,
    pady=3)

InputFrame.pack()

scrollbar = ttk.Scrollbar(
    master=TableFrame,
    orient=tk.VERTICAL,
    command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT)
tree.pack(side=tk.LEFT)

TableFrame.pack()


root.minsize(355, 350)
root.mainloop()
