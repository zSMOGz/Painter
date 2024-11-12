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
                     simpledialog,
                     ttk)
from PIL import Image, ImageDraw, ImageFont, ImageTk


def rgb_to_hex(r: int,
               g: int,
               b: int):
    """"
    Преобразование цвета RGB в HEX
    """
    hex_value = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return hex_value


class DrawingApp:
    __brush_sizes = ["1", "2", "5", "10", "20", "50", "100", "200",
                     "500", "1000"]
    __canvas_color = "white"
    __previous_pen_color = "black"
    __max_canvas_size_width = 900
    __max_canvas_size_height = 900
    __text_size = 20
    __font = ImageFont.truetype("arial.ttf", size=__text_size)
    __last_place_text = ""

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        self.canvas_size_width = 600
        self.canvas_size_height = 600
        self.image = Image.new("RGB",
                               (self.canvas_size_width,
                                self.canvas_size_height),
                               self.__canvas_color)
        self.photo = ImageTk.PhotoImage(self.image)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = Canvas(root,
                             width=self.canvas_size_width,
                             height=self.canvas_size_height,
                             bg=self.__canvas_color)
        self.canvas.pack()

        self.canvas_current_color = Canvas(root,
                                           width=20,
                                           height=20,
                                           bg=self.__previous_pen_color)

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
                       self.save_image_event)
        self.root.bind('<Control-c>',
                       self.choose_color_event)

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

        self.canvas_current_color.pack(side=LEFT)
        size_button = Button(control_frame,
                             text="Размер изображния",
                             command=self.update_size)
        size_button.pack(side=LEFT)

        text_button = Button(control_frame,
                             text="Текст",
                             command=self.create_text)
        text_button.pack(side=LEFT)

        cc_canvas = self.change_canvas_color
        change_canvas_color_button = Button(control_frame,
                                            text="Цвет фона",
                                            command=cc_canvas)
        change_canvas_color_button.pack(side=LEFT)

    def update_size(self):
        """
        Обновление размера изображения.
        """
        max_size = self.__max_canvas_size_width
        size = simpledialog.askinteger("Размер изображения",
                                       "Новый размер картинки:",
                                       minvalue=100,
                                       maxvalue=900,
                                       initialvalue=max_size,
                                       parent=self.root)
        self.canvas_size_width = size
        self.canvas_size_height = size
        self.image = Image.new("RGB",
                               (self.canvas_size_width,
                                self.canvas_size_height),
                               self.__canvas_color)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.canvas_size_width,
                           height=self.canvas_size_height)
        self.canvas.pack()

    def create_text(self):
        """
        Получение текста из диалога.
        """
        self.__last_place_text = simpledialog.askstring("Текст",
                                                        "Введите текст:",
                                                        parent=self.root)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.bind('<Button-1>',
                         self.place_text)

    def place_text(self,
                   event):
        """
        Расположение текста на изображении.
        """
        self.draw.text((event.x, event.y),
                       text=self.__last_place_text,
                       fill=self.pen_color,
                       font=self.__font,
                       background=self.__canvas_color)

        self.photo = ImageTk.PhotoImage(self.image)
        image_id = self.canvas.create_image(0,
                                            0,
                                            anchor="nw",
                                            image=self.photo)

        self.canvas.itemconfig(image_id,
                               image=self.photo)
        self.canvas.update()

        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<B1-Motion>',
                         self.paint)
        self.canvas.bind('<ButtonRelease-1>',
                         self.reset)

    def change_canvas_color(self):
        """
        Изменение цвета фона.
        """
        self.__canvas_color = colorchooser.askcolor(
            color=self.__canvas_color)[1]
        self.set_current_canvas_color()

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
        self.set_current_color()

    def clear_canvas(self):
        """
        Очистка холста.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB",
                               (600, 400),
                               self.__canvas_color)
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Выбор цвета.
        """
        self.pen_color = self.__previous_pen_color
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.set_current_color()

    def choose_color_event(self,
                           event):
        """
        Выбор цвета.
        """
        self.choose_color()

    def set_current_color(self):
        """
        Установка текущего цвета.
        """
        if (self.pen_color is not None
                and self.pen_color != self.__canvas_color):
            self.canvas_current_color.configure(bg=self.pen_color)

    def set_current_canvas_color(self):
        """
        Установка текущего цвета фона.
        """
        if self.__canvas_color is not None:
            self.canvas.config(bg=self.__canvas_color)
            self.canvas.update()

    def eraser(self):
        """
        Ластик.
        """
        self.__previous_pen_color = self.pen_color
        self.pen_color = self.__canvas_color

    def save_image(self):
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

    def save_image_event(self,
                         event):
        """
        Сохранение изображения.
        """
        self.save_image()


def main():
    root = Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
