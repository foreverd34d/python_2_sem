from tkinter import Tk, Canvas, Event
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    is_active: bool
    is_main: bool


class App:

    def __init__(self, width: int, height: int, title: str, points_size: int,
                 delay: float):
        self.__width = width
        self.__height = height
        self.__points_size = points_size
        self.__delay = delay

        self.__points_list = []
        self.__points_objects_list = []
        self.__triangle_objects_list = []
        self.__triangle_min_diff = None

        self.__root = Tk()
        self.__root.title(title)
        self.__root.resizable(False, False)
        self.run_status = True

        self.__canvas = None
        self.__setup_canvas()

        self.__bind_list = {}
        self.__setup_binds()

        self.__tip_obj = self.__place_tip()
        self.__set_diff_to_zero()

    @staticmethod
    def __fail_safe(func):

        def wrapper(self, *args, **kwargs):
            if self.run_status:
                return func(self, *args, **kwargs)
            exit(0)

        return wrapper

    def __setup_canvas(self):
        self.__canvas = Canvas(self.__root,
                               width=self.__width,
                               height=self.__height)
        self.__canvas.pack()

    def __setup_binds(self):
        self.__bind_list["<Escape>"] = ("root",
                                        self.__root.bind(
                                            "<Escape>", self.__remove_tip))
        self.__bind_list["<Button-1>"] = ("canvas",
                                          self.__canvas.bind(
                                              "<Button-1>",
                                              self.__place_point))
        self.__bind_list["<Button-3>"] = ("canvas",
                                          self.__canvas.bind(
                                              "<Button-3>",
                                              self.__remove_point))
        self.__bind_list["<Return>"] = ("root",
                                        self.__root.bind(
                                            "<Return>",
                                            self.__do_calculations))
        self.__bind_list["<BackSpace>"] = ("root",
                                           self.__root.bind(
                                               "<BackSpace>",
                                               self.__remove_all_points))

        self.__root.protocol("WM_DELETE_WINDOW", self.__object_destruction)

    @__fail_safe
    def __disable_binds(self):
        for bind_key in self.__bind_list.keys():
            if self.__bind_list[bind_key][0] == "root":
                self.__root.unbind(bind_key, self.__bind_list[bind_key][1])
            if self.__bind_list[bind_key][0] == "canvas":
                self.__canvas.unbind(bind_key, self.__bind_list[bind_key][1])

    def __place_tip(self):
        return self.__canvas.create_text(self.__width / 8,
                                         self.__height / 16,
                                         text="'Left-click' to add point\n"
                                         "'Right-click' to remove point\n"
                                         "'BackSpace' to remove all points\n"
                                         "Press 'Esc' to close this tip\n"
                                         "Press 'Enter' to start calculations")

    @__fail_safe
    def __remove_tip(self, event=None):
        self.__canvas.delete(self.__tip_obj)
        self.__tip_obj = None

    @__fail_safe
    def __place_point(self, event: Event):
        point_obj = self.__canvas.create_oval(event.x,
                                              event.y,
                                              event.x,
                                              event.y,
                                              width=self.__points_size,
                                              outline="#0d1117")
        self.__points_list.append(
            Point(event.x, event.y, is_active=False, is_main=False))
        self.__points_objects_list.append(point_obj)
        print(f'Added <{event.x},{event.y}>')

        self.__canvas.update()

    @__fail_safe
    def __find_point_near(self, x, y):
        for point in self.__points_list:
            if ((point.x - self.__points_size / 2) <= x <= (point.x + self.__points_size / 2)) and \
                    ((point.y - self.__points_size / 2) <= y <= (point.y + self.__points_size / 2)):
                return self.__points_list.index(point)
        print(f"Can't find point near <{x},{y}>")

    @__fail_safe
    def __remove_point(self, event: Event):
        index = self.__find_point_near(event.x, event.y)
        if index is None:
            return

        self.__canvas.delete(self.__points_objects_list[index])
        print(
            f'Removed <{self.__points_list[index].x},{self.__points_list[index].y}> by click to <{event.x},{event.y}>'
        )

        self.__points_objects_list.pop(index)
        self.__points_list.pop(index)

        self.__canvas.update()

    @__fail_safe
    def __remove_all_points(self, event=None):
        for i in range(len(self.__points_objects_list)):
            self.__canvas.delete(self.__points_objects_list[i])

        self.__points_objects_list.clear()
        self.__points_list.clear()

    @__fail_safe
    def __make_point_normal(self, index):
        self.__canvas.itemconfig(self.__points_objects_list[index],
                                 outline="#0d1117")
        self.__points_list[index].is_active = False
        self.__points_list[index].is_main = False

        self.__canvas.update()

    @__fail_safe
    def __make_point_active(self, index):
        if self.__points_list[index].is_main:
            return
        self.__canvas.itemconfig(self.__points_objects_list[index],
                                 outline="#36AE7C")
        self.__points_list[index].is_active = True

        self.__canvas.update()

    @__fail_safe
    def __make_point_main(self, index):
        if not self.__points_list[index].is_active:
            print(
                f"Can't make point <{self.__points_list[index].x},{self.__points_list[index].y}> "
                f"main, it's not active!")
            return

        self.__canvas.itemconfig(self.__points_objects_list[index],
                                 outline="#EB5353")
        self.__points_list[index].is_main = True

        self.__canvas.update()

    @__fail_safe
    def __draw_triangle(self, a: Point, b: Point, c: Point, is_result=False):
        if not is_result and (not a.is_active or not b.is_active
                              or not c.is_active) and (not a.is_main
                                                       and not b.is_main
                                                       and not c.is_main):
            return

        color = "#2A2550" if not is_result else "#251D3A"

        self.__triangle_objects_list.clear()
        self.__triangle_objects_list.append(
            self.__canvas.create_line(a.x,
                                      a.y,
                                      b.x,
                                      b.y,
                                      fill=color,
                                      width=self.__points_size / 3))
        self.__triangle_objects_list.append(
            self.__canvas.create_line(c.x,
                                      c.y,
                                      b.x,
                                      b.y,
                                      fill=color,
                                      width=self.__points_size / 3))
        self.__triangle_objects_list.append(
            self.__canvas.create_line(a.x,
                                      a.y,
                                      c.x,
                                      c.y,
                                      fill=color,
                                      width=self.__points_size / 3))

        self.__canvas.update()

    @__fail_safe
    def __remove_triangle(self):
        for obj in self.__triangle_objects_list:
            self.__canvas.delete(obj)
        self.__triangle_objects_list.clear()

    @__fail_safe
    def __set_diff_to_zero(self):
        self.__triangle_min_diff = (self.__width * self.__height, 0,
                                    (Point(0, 0, False,
                                           False), Point(0, 0, False, False),
                                     Point(0, 0, False, False)))

    @__fail_safe
    def __calculate_area_diff(self, a: Point, b: Point, c: Point):
        area = 0.5 * abs((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y))
        len_ab = ((b.x - a.x)**2 + (b.y - a.y)**2)**0.5
        len_ac = ((c.x - a.x)**2 + (c.y - a.y)**2)**0.5

        res = abs((len_ab - len_ac) * area / (len_ab + len_ac))

        return res if res > 0 else self.__width * self.__height

    @__fail_safe
    def __set_area_min_diff(self, diff, index, a: Point, b: Point, c: Point):
        if diff < self.__triangle_min_diff[0]:
            self.__triangle_min_diff = (diff, index, (a, b, c))

    @__fail_safe
    def __do_calculations(self, event=None):
        if len(self.__points_list) < 3:
            print("Can't calculate, less than 3 points available!")
            return

        self.__disable_binds()
        self.__remove_triangle()

        for first in range(len(self.__points_list)):
            a = self.__points_list[first]
            self.__make_point_active(first)
            self.__make_point_main(first)

            for second in range(len(self.__points_list)):
                if second == first:
                    continue
                b = self.__points_list[second]

                self.__make_point_active(
                    self.__find_point_near(self.__points_list[second].x,
                                           self.__points_list[second].y))

                for third in range(len(self.__points_list)):
                    if third == second or third == first:
                        continue

                    c = self.__points_list[third]

                    self.__make_point_active(
                        self.__find_point_near(self.__points_list[third].x,
                                               self.__points_list[third].y))

                    # self.__draw_triangle(a, b, c)

                    self.__set_area_min_diff(
                        self.__calculate_area_diff(a, b, c), first, a, b, c)
                    # time.sleep(self.__delay)
                    self.__remove_triangle()

                    self.__make_point_normal(
                        self.__find_point_near(self.__points_list[third].x,
                                               self.__points_list[third].y))

                self.__make_point_normal(second)

            self.__make_point_normal(first)

        a, b, c = self.__triangle_min_diff[2]
        index = self.__triangle_min_diff[1]
        print(f'\nFound minimum: {self.__triangle_min_diff[0]} px^2\n'
              f'In triangle [{a.x},{a.y}]-[{b.x},{b.y}]-[{c.x},{c.y}]\n'
              f'With bisector from point <{a.x},{a.y}>')
        self.__draw_triangle(a, b, c, is_result=True)
        self.__make_point_active(index)
        self.__make_point_main(index)
        self.__set_diff_to_zero()

        self.__canvas.after(10000, self.__remove_triangle)
        self.__canvas.after(10000, self.__make_point_normal, index)

        self.__setup_binds()

    def __object_destruction(self):
        self.run_status = False
        self.__root.after(10, self.__root.destroy)

    def run(self):
        self.__root.mainloop()


if __name__ == '__main__':
    app = App(800, 800, "Triangle solver?", 16, 0.075)
    app.run()
