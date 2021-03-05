from tkinter import *
from PIL import ImageTk, Image, ImageEnhance
# import matplotlib.pyplot as plt
import numpy
import cv2
import os


class Coloring:
    def __init__(self, path):
        self.root = Tk()
        self.root.title('Раскраска')

        menubar = Menu(self.root)

        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label="Save", command=self.save)

        settings_menu = Menu(menubar, tearoff=False)
        settings_menu.add_command(label="Settings", command=self.open_settings)

        # self.thresholding = StringVar(value='threshold')

        gallery_menu = Menu(menubar, tearoff=False)
        gallery_menu.add_command(label="Gallery", command=self.open_gallery)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="Gallery", menu=gallery_menu)
        self.root.config(menu=menubar)

        self.path_to_save = StringVar(value='images/')

        self.image_path = path
        self.np_array_image = self.prepare_image(cv2.imread(self.image_path))
        self.image = self.cv2pil_imgs(self.np_array_image)

        self.imageNp = self.np_array_image.copy()
        self.imageTk = self.cv2pil_imgs(self.imageNp)

        # self.changes = [(self.imageTk, self.imageNp)]
        self.changes = []
        self.image_frame = Frame(self.root, height=self.imageTk.height(), width=self.imageTk.width())
        self.image_frame.grid(row=1, column=1)

        self.root.rowconfigure((0,2), weight=1, uniform='fred')
        self.root.columnconfigure((0,2), weight=1, uniform='fred')

        self.gallery_frame = None
        self.gallery_path = StringVar(value='images/')

        self.image_canvas = Canvas(self.image_frame, height=self.imageTk.height(), width=self.imageTk.width())
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.imageTk)
        self.image_canvas.pack()

        self.colors = {
            'brown': (150, 75, 0),
            'red': (255, 0, 0),
            'orange': (255, 128, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'light_blue': (0, 128, 255),
            'blue': (0, 0, 255),
            'violet': (128, 0, 255),
            'white': (255, 255, 255),
            'black': (1, 1, 1),
            'custom0': (255, 255, 255),
            'custom1': (255, 255, 255),
            'custom2': (255, 255, 255),
            'custom3': (255, 255, 255),
            'custom4': (255, 255, 255),
            'custom5': (255, 255, 255)
        }


        self.color = (255, 255, 255)
        self.root.bind('<Button-1>', self.fragment_coloring)

        self.brown_btn = self.circle(self.colors['brown'])
        self.red_btn = self.circle(self.colors['red'])
        self.yellow_btn = self.circle(self.colors['yellow'])
        self.orange_btn = self.circle(self.colors['orange'])
        self.green_btn = self.circle(self.colors['green'])
        self.blue_btn = self.circle(self.colors['blue'])
        self.light_blue_btn = self.circle(self.colors['light_blue'])
        self.violet_btn = self.circle(self.colors['violet'])
        self.white_btn = self.circle(self.colors['white'])
        self.black_btn = self.circle(self.colors['black'])
        self.custom_btn0 = self.circle_for_custom_btn(self.colors['custom0'])
        self.custom_btn1 = self.circle_for_custom_btn(self.colors['custom1'])
        self.custom_btn2 = self.circle_for_custom_btn(self.colors['custom2'])
        self.custom_btn3 = self.circle_for_custom_btn(self.colors['custom3'])
        self.custom_btn4 = self.circle_for_custom_btn(self.colors['custom4'])

        self.right_frame = Frame(self.root)
        self.right_frame.grid(row=1, column=2)

        self.colors_frame = Frame(self.right_frame)
        self.colors_frame.pack()

        self.default_colors = Frame(self.colors_frame)
        self.default_colors.pack(side='right')

        self.brown = Button(self.default_colors ,image=self.brown_btn, command=lambda: self.change_color('brown')).pack()
        self.red = Button(self.default_colors ,image=self.red_btn, command=lambda: self.change_color('red')).pack()
        self.orange = Button(self.default_colors, image=self.orange_btn, command=lambda: self.change_color('orange')).pack()
        self.yellow = Button(self.default_colors, image=self.yellow_btn, command=lambda: self.change_color('yellow')).pack()
        self.green = Button(self.default_colors, image=self.green_btn, command=lambda: self.change_color('green')).pack()
        self.light_blue = Button(self.default_colors, image=self.light_blue_btn, command=lambda: self.change_color('light_blue')).pack()
        self.blue = Button(self.default_colors, image=self.blue_btn, command=lambda: self.change_color('blue')).pack()
        self.violet = Button(self.default_colors, image=self.violet_btn, command=lambda: self.change_color('violet')).pack()

        self.custom_colors = Frame(self.colors_frame)
        self.custom_colors.pack(side='right')

        self.custom0 = Button(self.custom_colors, image=self.custom_btn0, command=lambda: self.change_color('custom0'))
        self.custom0.bind('<Double-Button-1>', lambda event, arg=0: self.change_cst_clr(event, arg))
        self.custom0.pack()

        self.custom1 = Button(self.custom_colors, image=self.custom_btn1, command=lambda: self.change_color('custom1'))
        self.custom1.bind('<Double-Button-1>', lambda event, arg=1: self.change_cst_clr(event, arg))
        self.custom1.pack()

        self.custom2 = Button(self.custom_colors, image=self.custom_btn2, command=lambda: self.change_color('custom2'))
        self.custom2.bind('<Double-Button-1>', lambda event, arg=2: self.change_cst_clr(event, arg))
        self.custom2.pack()

        self.custom3 = Button(self.custom_colors, image=self.custom_btn3, command=lambda: self.change_color('custom3'))
        self.custom3.bind('<Double-Button-1>', lambda event, arg=3: self.change_cst_clr(event, arg))
        self.custom3.pack()

        self.custom4 = Button(self.custom_colors, image=self.custom_btn4, command=lambda: self.change_color('custom4'))
        self.custom4.bind('<Double-Button-1>', lambda event, arg=4: self.change_cst_clr(event, arg))
        self.custom4.pack()

        self.custom5 = Button(self.custom_colors, image=self.custom_btn4, command=lambda: self.change_color('custom5'))
        self.custom5.bind('<Double-Button-1>', lambda event, arg=5: self.change_cst_clr(event, arg))
        self.custom5.pack()

        self.white = Button(self.custom_colors, image=self.white_btn, command=lambda: self.change_color('white')).pack()
        self.black = Button(self.custom_colors, image=self.black_btn, command=lambda: self.change_color('black')).pack()

        self.reset_undo = Frame(self.right_frame)
        self.reset_undo.pack(pady=40)

        self.reset_btn = Button(self.reset_undo, text='Reset', height=1, width=8, command=self.reset)
        self.undo_btn = Button(self.reset_undo, text='Undo', height=2, width=8, command=self.undo)
        self.reset_btn.pack()
        self.undo_btn.pack()
        self.selected_color_image = self.circle(self.color)

        self.explanation = Label(self.reset_undo, text='Selected color:')
        self.explanation.pack(pady=5)

        self.selected_color = Label(self.reset_undo, image=self.selected_color_image, relief=RAISED)
        self.selected_color.pack()
        self.save_path = '.'

        self.cstm_clr = ImageTk.PhotoImage(Image.open('cstm_clr.png'))
        self.cstm_clr_np = cv2.imread('cstm_clr.png')

        self.clrng_zoom_frame = Frame(self.root)
        self.clrng_zoom_frame.grid(row=2, column=1)
        self.buttons_frame = Frame(self.clrng_zoom_frame)
        self.buttons_frame.pack()
        self.coloring_btn_img = self.cv2pil_imgs(self.proportional_resize(cv2.imread('coloring_button1.jpg'), 60))
        self.coloring_btn = Button(self.buttons_frame, image=self.coloring_btn_img, command=self.enable_coloring, width=60, height=60)
        self.coloring_btn['state'] = 'disable'
        self.coloring_btn.pack(side='left')
        self.zoom_btn_img = self.cv2pil_imgs(self.proportional_resize(cv2.imread('zoom_button.jpg'), 52))
        self.zoom_btn = Button(self.buttons_frame, image=self.zoom_btn_img, command=self.enable_zooming, width=60, height=60)
        self.zoom_btn.pack(side='left')

        self.zoom_slider_frame = Frame(self.clrng_zoom_frame)
        self.zoom_slider_frame.pack(side='left')

        self.scale = IntVar(value=200)

        self.coloring = True
        self.zoomed = False

    def reset(self):
        if self.zoomed:
            self.enable_zooming()
            self.return_size()
            self.enable_coloring()

        self.imageNp = self.np_array_image.copy()
        self.imageTk = self.cv2pil_imgs(self.imageNp)
        self.change_img(self.imageTk)

    def undo(self):
        self.imageNp = self.np_array_image.copy()
        if self.changes:
            self.changes.pop(-1)

        if self.changes:
            for change in self.changes:
                if list(self.imageNp[change[0][1]][change[0][0]]) != [0, 0, 0]:
                    cv2.floodFill(self.imageNp, None, change[0], change[1])

        if self.zoomed:
            self.configure_zoomed_image()
        else:
            self.imageTk = self.cv2pil_imgs(self.imageNp)
            self.change_img(self.imageTk)


    def proportional_resize(self, imageNp, new_height):
        height, width, _ = imageNp.shape

        new_width = (width * new_height) / height
        imageNp = cv2.resize(imageNp, (int(new_width), new_height))

        return imageNp

    def enable_coloring(self):
        self.coloring_btn['state'] = 'disable'
        self.zoom_btn['state'] = 'active'
        self.right_frame.grid(row=1, column=2)

        self.root.bind('<Button-1>', self.fragment_coloring)
        self.image_canvas.unbind('<Double-Button-1>')

        self.zoom_slider.pack_forget()
        self.coloring = True
        self.buttons_frame.pack()
        self.zoom_slider_frame.pack_forget()

    def enable_zooming(self):
        self.zoom_btn['state'] = 'disable'
        self.coloring_btn['state'] = 'active'
        self.right_frame.grid_forget()
        self.root.unbind('<Button-1>')

        self.zoom_slider = Scale(self.zoom_slider_frame, from_=100, to=500, orient=HORIZONTAL, command=self.change_scale, length=200, variable=self.scale, resolution=10)
        self.zoom_slider.pack()

        if self.zoomed:
            self.image_canvas.bind('<Double-Button-1>', self.return_size)
        else:
            self.image_canvas.bind('<Double-Button-1>', self.zoom)

        self.coloring = False
        self.buttons_frame.pack(side='left')
        self.zoom_slider_frame.pack(side='left', padx=15)


    def change_scale(self, event):
        self.return_size()
        self.zoom()

    def make_zoomed_image(self, imageNp, scale):
        height, width, _ = imageNp.shape
        zoomed_image = cv2.resize(imageNp, (int(width * scale), int(height * scale)))

        return zoomed_image

    def configure_zoomed_image(self):
        self.zoomed_imageNp = self.make_zoomed_image(self.imageNp, self.scale.get() / 100)
        self.zoomed_imageTk = self.cv2pil_imgs(self.zoomed_imageNp)
        self.image_canvas.itemconfigure(self.image_canvas.find_all()[-1], image=self.zoomed_imageTk)

    def zoom(self, event=None):
        if not self.coloring:
            scale = self.scale.get() / 100
            self.zoomed_imageNp = self.make_zoomed_image(self.imageNp, scale)
            self.zoomed_imageTk = self.cv2pil_imgs(self.zoomed_imageNp)

            self.image_canvas.create_image(0, 0, anchor='nw', image=self.zoomed_imageTk)

            self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
            self.image_canvas.bind("<ButtonPress-1>", self.scroll_start)
            self.image_canvas.bind("<B1-Motion>", self.scroll_move)

            self.image_canvas.bind('<Double-Button-1>', self.return_size)

            self.zoomed = True

    def scroll_start(self, event):
        if not self.coloring:
            self.image_canvas.scan_mark(event.x, event.y)
            self.movingimage = self.image_canvas.find_closest(event.x, event.y, halo=5)

    def scroll_move(self, event):
        if not self.coloring:
            self.image_canvas.scan_dragto(event.x, event.y, gain=1)

    def return_size(self, event=None):
        if not self.coloring:
            zoomed_image = self.image_canvas.find_all()[-1]
            if zoomed_image != 1:
                self.image_canvas.destroy()

                self.imageTk = self.cv2pil_imgs(self.imageNp)
                self.image_canvas = Canvas(self.image_frame, height=self.imageTk.height(), width=self.imageTk.width())
                self.image_canvas.create_image(0, 0, anchor='nw', image=self.imageTk)
                self.image_canvas.pack()

                self.image_canvas.bind('<Double-Button-1>', self.zoom)
                self.zoomed = False

    def fragment_coloring(self, event):
        if '.!frame.!canvas' in str(event.widget) and list(self.imageNp[event.y][event.x]) != [0, 0, 0]:
            canvas = event.widget
            x = int(canvas.canvasx(event.x))
            y = int(canvas.canvasy(event.y))

            is_black_on_origin = False
            if self.zoomed:
                scale = self.scale.get() / 100
                x = int(canvas.canvasx(event.x) / scale)
                y = int(canvas.canvasy(event.y) / scale)
                if list(self.imageNp[y][x]) == [0, 0, 0]:
                    is_black_on_origin = True

            if not is_black_on_origin:
                cv2.floodFill(self.imageNp, None, (x, y), self.color)

            self.imageTk = self.cv2pil_imgs(self.imageNp)

            if self.zoomed:
                self.configure_zoomed_image()
            else:
                self.change_img(self.imageTk)

            self.changes.append(((x,y), self.color))

    def open_settings(self):
        try:
            self.settings.destroy()
        except AttributeError:
            pass

        self.settings = Toplevel(self.root)
        self.settings.resizable(width=0, height=0)

        # thresholding_explanation = Label(self.settings, text='Thresholding:')
        # thresholding_explanation.pack(anchor='w')
        # threshold_check_box = Checkbutton(self.settings, text='Thresholding' , variable=self.thresholding, onvalue='threshold', offvalue='False')
        # adaptiveThreshold_check_box = Checkbutton(self.settings, text='Adaptive thresholding' , variable=self.thresholding, onvalue='adaptiveThreshold', offvalue='False')
        # thresholdOtsu_check_box = Checkbutton(self.settings, text='Otsu thresholding' , variable=self.thresholding, onvalue='thresholdOtsu', offvalue='False')
        # threshold_check_box.pack(anchor='w', padx=10)
        # adaptiveThreshold_check_box.pack(anchor='w', padx=10)
        # thresholdOtsu_check_box.pack(anchor='w', padx=10)

        path_explanation = Label(self.settings, text='Path to save:')
        path_explanation.pack(anchor='w')
        path_entry = Entry(self.settings, textvariable=self.path_to_save)
        # path_entry.insert(END, self.path_to_save)
        path_entry.pack(anchor='w', padx=10)

        gallery_path_explanation = Label(self.settings, text='Gallery path:')
        gallery_path_explanation.pack(anchor='w')
        self.gallery_path_entry = Entry(self.settings, textvariable=self.gallery_path)
        # self.gallery_path_entry.insert(END, self.gallery_path)
        self.gallery_path_entry.pack(anchor='w', padx=10)

        settings_ok_btn = Button(self.settings, text='OK', command=self.settings_destroy)
        settings_ok_btn.pack(pady=10)

    def validate_entry(self):
        if os.path.exists(self.path_to_save.get()) == True and os.path.exists(self.gallery_path.get()) == True:
            return True
        else:
            self.path_to_save.set('images/')
            self.gallery_path.set('images/')
            return False

    def settings_destroy(self):
        if self.validate_entry():
            self.settings.destroy()

    def save(self):
        image_name = 'image'
        image_extension = '.png'
        idx = 0

        while True:
            if os.path.exists(self.path_to_save.get() + image_name + image_extension):
                image_name = 'image' + str(idx)
            else:
                break

            idx += 1

        cv2.imwrite(self.path_to_save.get() + image_name + image_extension, self.imageNp)


    def change_cst_clr(self, *args):
        try:
            self.chooser_frame.destroy()
        except AttributeError:
            pass

        self.chooser_frame = Frame(self.root)
        self.chooser_frame.grid(row=1, column=0)
        self.palette = Canvas(self.chooser_frame, width=253, height=253)

        self.palette.create_image(128,3, anchor='n', image=self.cstm_clr)
        self.palette.pack(padx=15)

        self.slider_explanation = Label(self.chooser_frame, text='Color saturation:')
        self.slider_explanation.pack()

        self.enchance_var = IntVar(value=1.0)
        self.enchance_slider = Scale(self.chooser_frame, from_=0.1, to=1.0, orient=HORIZONTAL, command=lambda event, arg=args[1]: self.change_enchance(event, arg),
                                     resolution=0.0001, variable=self.enchance_var, length=200)
        self.enchance_slider.pack()

        ok = Button(self.chooser_frame, text='OK', command=self.chooser_frame.destroy).pack(pady=10)
        self.palette.create_oval(5, 3, 251, 251, outline='black', width=4)
        self.shape_id = self.palette.create_oval(81, 81, 71, 71, fill='green', outline='white')

        self.palette.bind("<B1-Motion>", lambda event, arg=args[1]: self.cursor_move(event, arg))


    def change_enchance(self,event, idx):
        img = numpy.array([[[self.colors['custom' + str(idx)][0], self.colors['custom' + str(idx)][1], self.colors['custom' + str(idx)][2]]]])
        img = img.astype(numpy.uint8)
        img = Image.fromarray(img)
        converter = ImageEnhance.Color(img)
        img2 = converter.enhance(self.enchance_slider.get())
        img2 = numpy.array(img2)

        color = (int(img2[0][0][0]),int(img2[0][0][1]),int(img2[0][0][2]))

        setattr(self, 'custom_btn' + str(idx), self.circle_for_custom_btn(color))
        getattr(self, 'custom' + str(idx)).config(image=getattr(self, 'custom_btn' + str(idx)))
        self.color = color

        self.selected_color_image = self.circle(color)
        self.selected_color.configure(image=self.selected_color_image)
        self.selected_color.image = self.selected_color_image

    def cursor_move(self, event, idx):
        color = tuple(
            [
                int(self.cstm_clr_np[event.y][event.x][2]),
                int(self.cstm_clr_np[event.y][event.x][1]),
                int(self.cstm_clr_np[event.y][event.x][0])
            ]
        )

        if color == (0, 0, 0):
            self.colors['custom' + str(idx)] = (1, 1, 1)
        else:
            self.colors['custom' + str(idx)] = color

        setattr(self, 'custom_btn' + str(idx), self.circle_for_custom_btn(self.colors['custom'+str(idx)]))
        getattr(self, 'custom'+str(idx)).config(image=getattr(self, 'custom_btn'+str(idx)))
        self.color = self.colors['custom' + str(idx)]

        self.palette.coords(self.shape_id, event.x - 5, event.y - 5, event.x + 5, event.y + 5)

        self.selected_color_image = self.circle(self.color)
        self.selected_color.configure(image=self.selected_color_image)
        self.selected_color.image = self.selected_color_image

    def circle(self, color):
        btn = cv2.imread('btn.jpg')
        h, w, c = btn.shape
        btn = cv2.resize(btn, (1000,1000))
        btn = cv2.circle(btn, (500,500), 450, color, -1)
        btn = cv2.resize(btn, (60,61))
        btn = Image.fromarray(btn)
        btn = ImageTk.PhotoImage(master=self.root, image=btn)
        return btn

    def circle_for_custom_btn(self, color):
        btn = cv2.imread('ctm_btn.jpg')
        btn = cv2.resize(btn, (1000,1000))
        btn = cv2.circle(btn, (700,300), 300, color, -1)
        btn = cv2.resize(btn, (60,61))

        btn = Image.fromarray(btn)
        btn = ImageTk.PhotoImage(master=self.root, image=btn)

        return btn

    def change_color(self, color):
        self.color = self.colors[color]

        self.selected_color_image = self.circle(self.color)
        self.selected_color.configure(image=self.selected_color_image)
        self.selected_color.image = self.selected_color_image

    def prepare_image(self, image=None):
        if image is None:
            image = self.imageNp

        try:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        except cv2.error:
            pass

        _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        mask = (image == [0., 0., 0.]).all(axis=2)

        image[mask] = [0, 0, 0]

        self.imageNp = image

        return image

    def cv2pil_imgs(self, nparray):
        img = Image.fromarray(nparray)
        image = ImageTk.PhotoImage(image=img)
        return image

    def change_img(self, image):
        self.image_canvas.itemconfigure(self.image_canvas.find_all()[-1], image=image)

    def run(self):
        self.root.mainloop()

    def open_gallery(self, event=None):
        if self.zoomed:
            self.enable_zooming()
            self.return_size()
            self.enable_coloring()

        if not self.gallery_frame:
            self.clrng_zoom_frame.grid_forget()

            self.gallery_frame = Frame(self.root)
            self.internal_frame = Frame(self.gallery_frame)
            self.gallery_canvas = Canvas(self.internal_frame, width=310, height=700)
            self.scrollbar = Scrollbar(self.internal_frame, orient=VERTICAL, command=self.gallery_canvas.yview)

            self.images_frame = Frame(self.gallery_canvas)
            self.images_frame.bind(
                "<Configure>",
                lambda e: self.gallery_canvas.configure(
                    scrollregion=self.gallery_canvas.bbox("all")
                )
            )
            self.gallery_canvas.create_window((0, 0), window=self.images_frame, anchor="nw")
            self.gallery_canvas.configure(yscrollcommand=self.scrollbar.set)

            self.gallery_frame.grid(row=1, column=0, sticky='nw', padx=50)
            self.internal_frame.pack()
            self.gallery_canvas.pack(side='left')
            self.scrollbar.pack(fill=Y, side='left')

            self.images = self.collect_images()
            self.arrange_images()

            self.rectangle = None
            self.previous_selection = None

            self.right_frame.grid_forget()

            self.root.unbind('<Button-1>')

            self.image_backup = self.imageNp.copy()

    def image_selection(self, event):
        try:
            canvas_idx = int(str(event.widget).split('.')[-1].replace('!canvas', '')) - 1
        except ValueError as e:
            canvas_idx = 0

        if self.previous_selection is None:
            self.previous_selection = canvas_idx
            self.rectangle = getattr(self, 'canvas' + str(canvas_idx)).create_rectangle(2, 2, 100, 100, outline='black')
        else:
            getattr(self, 'canvas' + str(self.previous_selection)).delete(self.rectangle)
            self.rectangle = getattr(self, 'canvas' + str(canvas_idx)).create_rectangle(2, 2, 100, 100, outline='black')
            self.previous_selection = canvas_idx

        self.selected_filename = self.images[canvas_idx]
        self.selected_image = ImageTk.PhotoImage(Image.open(self.gallery_path.get() + self.selected_filename))
        self.selected_image_path = self.gallery_path.get() + self.selected_filename
        self.change_root_image(self.selected_image)

    def collect_images(self):
        files = os.listdir(self.gallery_path.get())

        self.collected_images = []
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                self.collected_images.append(file)

        return self.collected_images

    def cv2pil_imgs_gallery(self, nparray):
        nparray = cv2.resize(nparray, (100,100))

        img = Image.fromarray(nparray)
        image = ImageTk.PhotoImage(image=img)
        return image

    def arrange_images(self):

        column = 0
        row = 0
        for idx, image_name in enumerate(self.images):
            setattr(self, 'glry_image' + str(idx), self.cv2pil_imgs_gallery(cv2.imread(self.gallery_path.get() + image_name)))
            image = getattr(self, 'glry_image' + str(idx))

            setattr(self, 'canvas' + str(idx), Canvas(self.images_frame, width=100, height=100))
            getattr(self, 'canvas' + str(idx)).create_image(50,50, image=image)
            getattr(self, 'canvas' + str(idx)).grid(column=column, row=row)
            getattr(self, 'canvas' + str(idx)).bind('<Button-1>', self.image_selection)

            if len(self.images[idx]) > 18:
                name = self.images[idx][:11]
                extension = '.' + self.images[idx].split('.')[-1]
                label_text = f'{name}... {extension}'
            else:
                label_text = self.images[idx]

            setattr(self, 'filename' + str(idx), Label(self.images_frame, text=label_text))
            getattr(self, 'filename' + str(idx)).grid(column=column, row=row+1)

            if column != 2:
                column += 1
            else:
                row += 2
                column = 0
        self.btns_frame = Frame(self.gallery_frame)

        # if self.imageTk.height() == 800:
        #     self.btns_frame.grid(column=0, row=2, sticky='nw', padx=153)
        # else:
        #     self.btns_frame.grid(column=0, row=2, sticky='nw', padx=153, pady=40)
        self.btns_frame.pack(anchor='w', padx=103, pady=30)

        self.accept_btn = Button(self.btns_frame, text='Accept', command=self.accept)
        self.accept_btn.pack(side='left',padx=3)

        self.cancel_btn = Button(self.btns_frame, text='Cancel', command=self.cancel)
        self.cancel_btn.pack(side='left')

    def accept(self):
        if self.collected_images == []:
            self.cancel()
            return None

        self.gallery_frame.destroy()
        self.image_path = self.selected_image_path
        self.np_array_image = self.prepare_image(cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE))
        self.image = self.cv2pil_imgs(self.np_array_image)

        self.imageNp = self.np_array_image.copy()
        self.imageTk = self.cv2pil_imgs(self.imageNp)


        if self.imageTk.height() > 800:
            self.np_array_image = self.proportional_resize(self.np_array_image, 800)
            self.image = self.cv2pil_imgs(self.np_array_image)

            self.imageNp = self.np_array_image.copy()
            self.imageTk = self.cv2pil_imgs(self.imageNp)

        self.image_canvas.configure(height=self.imageTk.height(), width=self.imageTk.width())
        self.changes = []

        self.change_root_image(self.imageTk)

        self.right_frame.grid(row=1, column=2)

        self.root.bind('<Button-1>', self.fragment_coloring)

        self.gallery_frame = None
        self.btns_frame.destroy()
        self.clrng_zoom_frame.grid(row=2, column=1)
        self.image_backup = None

    def cancel(self):
        self.rectangle = None
        self.previous_selection = None
        self.imageNp = self.image_backup
        self.imageTk = self.cv2pil_imgs(self.imageNp)
        self.change_root_image(self.imageTk)
        self.image_backup = None
        self.selected_image_path = None
        self.gallery_frame.destroy()
        self.right_frame.grid(row=1, column=2)
        self.gallery_frame = None

        self.root.bind('<Button-1>', self.fragment_coloring)

        self.btns_frame.destroy()
        self.clrng_zoom_frame.grid(row=2, column=1)



    def change_root_image(self, image, preparing=None):
        height = image.height()

        if preparing:
            image = self.prepare_image(image)

        if height > 800:
            self.imageee = self.cv2pil_imgs(self.proportional_resize(self.imageNp, 800))
            self.image_canvas.itemconfigure((1,), image=self.imageee)
            self.image_canvas.configure(height=self.imageee.height(), width=self.imageee.width())
            # self.btns_frame.grid_forget()
            # self.btns_frame.grid(column=0, row=2, sticky='nw', padx=153)
        else:
            self.image_canvas.itemconfigure((1,), image=image)
            self.image_canvas.configure(height=image.height(), width=image.width())
            # self.btns_frame.grid_forget()
            # self.btns_frame.grid(column=0, row=2, sticky='nw', padx=153, pady=40)

        self.image_frame.grid_forget()
        self.right_frame.grid_forget()
        self.image_frame.grid(row=1, column=1)

coloring = Coloring("images/17.jpg")
coloring.run()
