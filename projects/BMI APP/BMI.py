import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        # Window setup
        super().__init__(fg_color = GREEN)
        self.title('')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        self.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
        self.columnconfigure(0 , weight = 1, uniform = 'a')
        
        # Data
        self.metric_bool = ctk.BooleanVar(value = True)
        self.height_int = ctk.IntVar(value = 170)
        self.weight_float = ctk.DoubleVar(value = 65.0)
        self.BMI_string = ctk.StringVar(value = '')
        self.update_bmi()

        # Tracing (trace_add lets you watch for changes in a tkinter variable (StringVar, IntVar, DoubleVar, BooleanVar).
        # Whenever the variable is read, written to, or deleted, it can call a callback function.
        self.height_int.trace_add('write', self.update_bmi)
        self.weight_float.trace_add('write', self.update_bmi)
        self.metric_bool.trace_add('write', self.change_units)

        # Widgets
        Result_Text(self, self.BMI_string)
        self.weight_input = Weight_Input(self, self.weight_float, self.metric_bool)
        self.height_input = Height_Input(self, self.height_int, self.metric_bool)
        Unit_Switch(self, self.metric_bool)

        self.mainloop()

    def change_units(self, * args): # *args is for the trace_add
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()

    def update_bmi(self, *args): # *args is for the trace_add
        height_meter = self.height_int.get() / 100.0
        weight_kilogram = self.weight_float.get()
        bmi_result = round(weight_kilogram / height_meter ** 2, 2)
        self.BMI_string.set(value=str(bmi_result))

    def change_title_bar_color(self):
        # Change colour of title bar, only works on windows
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35 # Attribute of colour of title bar
            COLOUR = TITLE_HEX_COLOUR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOUR), sizeof(c_int)))
        except:
            pass

class Result_Text(ctk.CTkLabel):
    def __init__(self, parent, bmi_result):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight = 'bold')
        super().__init__(master = parent, textvariable = bmi_result, font = font, text_color = WHITE)
        self.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew')

class Weight_Input(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master = parent, fg_color = WHITE)
        self.grid(column = 0, row = 2, sticky = 'nsew', padx = 10, pady = 10)
        self.weight_float = weight_float
        self.is_metric = metric_bool

        # Layout
        self.rowconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure(0, weight = 2, uniform = 'a')
        self.columnconfigure(1, weight = 1, uniform = 'a')
        self.columnconfigure(2, weight = 3, uniform = 'a')
        self.columnconfigure(3, weight = 1, uniform = 'a')
        self.columnconfigure(4, weight = 2, uniform = 'a')

        # Input Text
        self.output_string = ctk.StringVar()
        self.update_weight()

        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        self.label = ctk.CTkLabel(master = self, textvariable = self.output_string, text_color = BLACK, font = font)
        self.label.grid(row = 0, column = 2)

        # Input Buttons
        self.big_plus_button = ctk.CTkButton(master = self, command = lambda: self.update_weight(('plus', 'large')), text = '+', font = font, text_color = BLACK, fg_color = LIGHT_GREY, hover_color = GREY)
        self.big_plus_button.grid(row = 0, column = 4, sticky = 'ns', padx = 5, pady = 5)

        self.small_plus_button = ctk.CTkButton(master = self, command = lambda: self.update_weight(('plus', 'small')), text = '+', font = font, text_color = BLACK, fg_color = LIGHT_GREY, hover_color = GREY)
        self.small_plus_button.grid(row = 0, column = 3, sticky = 'ns', padx = 4, pady = 4)

        self.big_minus_button = ctk.CTkButton(master = self, command = lambda: self.update_weight(('minus', 'large')), text = '-', font = font, text_color = BLACK, fg_color = LIGHT_GREY, hover_color = GREY)
        self.big_minus_button.grid(row = 0, column = 0, sticky = 'ns', padx = 5, pady = 5)

        self.small_minus_button = ctk.CTkButton(master = self, command = lambda: self.update_weight(('minus', 'small')), text = '-', font = font, text_color = BLACK, fg_color = LIGHT_GREY, hover_color = GREY)
        self.small_minus_button.grid(row = 0, column = 1, sticky = 'ns', padx = 4, pady = 4)

    def update_weight(self, info = None):
        if info:
            if self.is_metric.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16

            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        if self.is_metric.get():
            self.output_string.set(f'{round(self.weight_float.get(), 1)} kg')
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f'{int(pounds)}lbs {int(ounces)}oz')
                                        
class Height_Input(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master = parent, fg_color = WHITE)
        self.grid(row = 3, column = 0, sticky = 'nsew', padx = 10, pady = 10)
        self.is_metric = metric_bool

        # Widgets
        self.slider = ctk.CTkSlider(self,
                                    command = self.update_text, # slider auto insets the "amount argument"
                                    button_color = GREEN,
                                    button_hover_color = GREY,
                                    progress_color = GREEN,
                                    fg_color = LIGHT_GREY,
                                    variable = height_int,
                                    from_ = 100,
                                    to = 250)
        self.slider.pack(side = 'left', fill = 'x', expand = True, padx = 10, pady = 10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        self.output_text = ctk.CTkLabel(master = self, textvariable = self.output_string, font = ctk.CTkFont(family = FONT, size = INPUT_FONT_SIZE), text_color = BLACK)
        self.output_text.pack(side = 'right', padx = 20, pady = 5)

    def update_text(self, amount):
        if self.is_metric.get():
            amount = f'{(amount / 100):.2f} m'
            self.output_string.set(value = amount)
        else:
            feet, inches = divmod(amount / 2.54, 12)   
            self.output_string.set(value = f'{int(feet)}\'{int(inches)}\"' )

class Unit_Switch(ctk.CTkLabel):
    def __init__(self, parent, is_metric):
        super().__init__(master = parent, fg_color=GREEN, text = 'metric',text_color = DARK_GREEN, font = ctk.CTkFont(family = FONT, size = SWITCH_FONT_SIZE, weight = 'bold'))
        self.place(relx = 0.98, rely = 0.01, anchor = 'ne')

        self.is_metric = is_metric
        self.bind('<Button>', self.change_units)
    
    def change_units(self, event):
        # change the metric bool True -> False
        self.is_metric.set(not self.is_metric.get())

        if self.is_metric.get():
            self.configure(text = 'metric')
        else:
            self.configure(text = 'imperial')

if __name__ == '__main__':
    App()