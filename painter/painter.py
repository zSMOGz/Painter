from tkinter import (LEFT,
                     ROUND,
                     TRUE,
                     Tk,
                     Canvas,
                     Frame,
                     Button,
                     Label,
                     X,
                     colorchooser,
                     filedialog,
                     messagebox,
                     ttk)
from PIL import Image, ImageDraw


def rgb_to_hex(r: int,
               g: int,
               b: int):
    """"
    Преобразование цвета RGB в HEX
    """
    hex_value = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return hex_value


class DrawingApp:
    __brush_sizes = ["1", "2", "5", "10"]
    __canvas_color = "white"
    __previous_pen_color = "black"

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB",
                               (600, 400),
                               self.__canvas_color)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = Canvas(root,
                             width=600,
                             height=400,
                             bg=self.__canvas_color)
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = (None,
                                    None)
        self.pen_color = 'black'
        self.__previous_pen_color = self.pen_color

        self.canvas.bind('<B1-Motion>',
                         self.paint)
        self.canvas.bind('<ButtonRelease-1>',
                         self.reset)
        self.canvas.bind('<Button-3>',
                         self.pick_color)

        self.root.bind('<Control-s>',
                       self.save_image)
        self.root.bind('<Control-c>',
                       self.choose_color)

    def setup_ui(self):
        """
        Создание интерфейса.
        """
        control_frame = Frame(self.root)
        control_frame.pack(fill=X)

        clear_button = Button(control_frame,
                              text="Очистить",
                              command=self.clear_canvas)
        clear_button.pack(side=LEFT)

        color_button = Button(control_frame,
                              text="Выбрать цвет",
                              command=self.choose_color)
        color_button.pack(side=LEFT)

        eraser_button = Button(control_frame,
                               text="Ластик",
                               command=self.eraser)
        eraser_button.pack(side=LEFT)

        label_brush_size = Label(text="Размер кисти")
        label_brush_size.pack(side=LEFT)
        brush_size_combobox = ttk.Combobox(values=self.__brush_sizes,
                                           state="readonly")
        brush_size_combobox.set(self.__brush_sizes[0])
        brush_size_combobox.pack(side=LEFT)
        self.brush_size_scale = brush_size_combobox
        self.brush_size_scale.pack(side=LEFT)

        save_button = Button(control_frame,
                             text="Сохранить",
                             command=self.save_image)
        save_button.pack(side=LEFT)

    def paint(self,
              event):
        """
        Рисование.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x,
                                    self.last_y,
                                    event.x,
                                    event.y,
                                    width=self.brush_size_scale.get(),
                                    fill=self.pen_color,
                                    capstyle=ROUND,
                                    smooth=TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                           fill=self.pen_color,
                           width=int(self.brush_size_scale.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self,
              event):
        """
        Сброс координат.
        """
        self.last_x, self.last_y = None, None

    def pick_color(self,
                   event):
        """
        Выбор цвета текущего пикселя.
        """
        r, g, b = self.image.getpixel((event.x,
                                       event.y))
        self.pen_color = rgb_to_hex(r, g, b)

    def clear_canvas(self):
        """
        Очистка холста.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB",
                               (600, 400),
                               self.__canvas_color)
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self,
                     event):
        """
        Выбор цвета.
        """
        self.pen_color = self.__previous_pen_color
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def eraser(self):
        """
        Ластик.
        """
        self.__previous_pen_color = self.pen_color
        self.pen_color = self.__canvas_color

    def save_image(self,
                   event):
        """
        Сохранение изображения.
        """
        file_path = filedialog.asksaveasfilename(
            filetypes=[('PNG files',
                        '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация",
                                "Изображение успешно сохранено!")


def main():
    root = Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
