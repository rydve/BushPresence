import subprocess
from pypresence import Presence
from pypresence.exceptions import PipeClosed
import pystray
from PIL import Image
import json
import os
from tkinter import Tk, Button, Frame, PhotoImage, font, Label, Toplevel, Scrollbar, Text, filedialog, END, Entry, messagebox, Canvas
import threading
import webbrowser
import ctypes
import requests
import validators

# global client_id_copy
# global connect_test

def check_for_update():
    response = requests.get('https://api.github.com/repos/rydve/BushPresence/releases/latest')
    latest_version = response.json()['tag_name']

    current_version = 'v.3.1'  # Замените на текущую версию вашей программы

    if latest_version != current_version:
        print("Update available")
        answer = messagebox.askokcancel("Обновление доступно", "Доступна новая версия программы. Хотите обновить?")
        if answer:
            webbrowser.open('https://disk.yandex.ru/d/fzpina2hULwA7A')


template_config = {
    "client_id": "",
    "details": "",
    "state": "",
    "large_image": "",
    "small_image": "",
    "buttons": [
        {
            "label": "",
            "url": ""
        },
        {
            "label": "",
            "url": ""
        }
    ]
}

global config

try:
    with open('configs/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except(FileNotFoundError, json.JSONDecodeError):
    with open('configs/config.json', 'w', encoding='utf-8') as f:
        json.dump(template_config, f, ensure_ascii=False, indent=4)
client_id = config['client_id']


global RPC
RPC = Presence(client_id)
try:
    RPC.connect()
    print("Успешное подключение")
    client_id_copy = client_id
    connect_test = 1

    params = {}
    valid_buttons = []

    for button in config['buttons']:
        label = button.get("label")
        url = button.get("url")

        if label and len(label) < 32 and url.startswith("http"):
            valid_buttons.append(button)

    if len(config['state']) > 2 and len(config['state']) <= 128:
        params['state'] = config['state']
    if len(config['details']) > 2 and len(config['details']) <= 128:
        params['details'] = config['details']
    if config['large_image'].strip():
        params['large_image'] = config['large_image']
    if config['small_image'].strip():
        params['small_image'] = config['small_image']
    if config['buttons']:
        params['buttons'] = valid_buttons

    RPC.update(**params)
    "Данные успешно загружены в активность"

except:
    client_id_copy = client_id
    connect_test = 0
    print("Не удалось подключиться")


def update_params():
    with open('configs/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)


    params = {}
    valid_buttons = []

    for button in config['buttons']:
        label = button.get("label")
        url = button.get("url")

        if label and len(label) < 32 and validators.url(url):
            valid_buttons.append(button)

    if len(config['state']) > 2:
        params['state'] = config['state']
    if len(config['details']) > 2:
        params['details'] = config['details']
    if config['large_image'].strip():
        params['large_image'] = config['large_image']
    if config['small_image'].strip():
        params['small_image'] = config['small_image']
    if config['buttons']:
        params['buttons'] = valid_buttons

    return params


def Refresh():
    updated_params = update_params()
    with open('configs/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    client_id = config['client_id']
    global client_id_copy
    global connect_test
    global RPC
    if client_id != client_id_copy or connect_test != 1:
        try:
            RPC_copy = Presence(client_id)
            RPC_copy.connect()
            client_id_copy = client_id
            connect_test += 1
            RPC_copy.update(**updated_params)
            print("Данные успешно обновлены")
        except:
            messagebox.showinfo("Ошибка подключения", "Ошибка подключения, проверьте корректно ли вы указали значение client_id")
            print("Ошибка подключения")
            print("Ошибка обновления данных, соединение потеряно")
    else:
        try:
            RPC.update(**updated_params)
            print("Данные успешно обновлены без переподключения")
        except PipeClosed:
            print("Соединение было закрыто, переподключаемся...")
            RPC = Presence(client_id)
            RPC.connect()
            RPC.update(**updated_params)
            print("Данные успешно обновлены после переподключения")

def open_discord():
    webbrowser.open('https://discord.gg/pGXSVaAWxs')

def on_enter(e):
    e.widget['background'] = 'DarkOliveGreen3'

def on_leave(e):
    e.widget['background'] = 'DarkOliveGreen1'

def create_button(frame, text, command, row, column):
    bold_font = font.Font(weight='bold', size=15, family='Courier')
    button = Button(frame, text=text, command=command, width=55, height=5, bg='DarkOliveGreen1', font=bold_font)
    button.grid(row=row, column=column)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def create_gui():
    global window
    window = Tk()
    window.title("BushPresence")

    window.iconbitmap('assets/icon.ico')

    window.resizable(False, False)

    global window_height
    global window_weight
    window_weight = 1000
    window_height = 800

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    global start_x, start_y
    start_x = int((screen_width / 2) - (window_weight / 2))
    start_y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_weight}x{window_height}+{start_x}+{start_y}")

    bg_image = PhotoImage(file="assets/background.png")

    bg_label = Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    canvas = Canvas(window, width=1000, height=800, highlightthickness=0)
    canvas.pack()

    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    title_text = "BushPresence"
    title_label = canvas.create_text(500, 70, text=title_text, font=font.Font(weight='bold', size=70, family="Courier New"), fill="DarkOliveGreen1")

    bold_font = font.Font(weight='bold', size=15, family='Courier')

    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    bold_font = font.Font(weight='bold', size=15, family='Courier')

    create_button(frame, "Config", lambda: menu_action(icon, 'Config'), 0, 0)
    create_button(frame, "README", lambda: menu_action(icon, 'README'), 1, 0)
    create_button(frame, "Refresh", lambda: menu_action(icon, 'Refresh'), 2, 0)
    create_button(frame, "Exit", lambda: menu_action(icon, 'Exit'), 3, 0)


    folder_path_button = Button(canvas, text="Program Folder", command=open_folder, font=bold_font,bg='DarkOliveGreen1')
    # folder_path_button.pack(side='left', anchor='s')
    folder_path_button_window = canvas.create_window(10, 790, anchor="sw", window=folder_path_button)
    folder_path_button.bind("<Enter>", on_enter)
    folder_path_button.bind("<Leave>", on_leave)

    discord_button = Button(canvas, text="Discord", command=open_discord, font=bold_font, bg='DarkOliveGreen1')
    # discord_button.pack(side='bottom', anchor='se')
    discord_button_window = canvas.create_window(990, 790, anchor="se", window=discord_button)
    discord_button.bind("<Enter>", on_enter)
    discord_button.bind("<Leave>", on_leave)


    window.protocol("WM_DELETE_WINDOW", window.withdraw)
    window.mainloop()

def open_readme():
    readme_window = Toplevel(window)
    readme_window.title("README")
    readme_window.iconbitmap('assets/icon.ico')
    readme_window.geometry(f"{window_weight}x{window_height}+{start_x}+{start_y}")

    scrollbar = Scrollbar(readme_window)
    scrollbar.pack(side='right', fill='y')

    text_widget = Text(readme_window, wrap='word', yscrollcommand=scrollbar.set, font=("Helvetica", 16))
    text_widget.pack(fill='both', expand=True)

    with open('other/README.txt', 'r',encoding='utf-8' ) as file:
        file_contents = file.read()

    text_widget.insert('1.0', file_contents)

    scrollbar.config(command=text_widget.yview)

    text_widget.config(state='disabled')

    text_widget.configure(bg="#2f3236", fg="white")



def open_config():
    def load_data():
        try:
            with open('configs/config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def reload_config_and_RPC():
        data = load_data()
        client_id_entry.delete(0, END)
        client_id_entry.insert(0, data.get("client_id", ""))

        details_entry.delete(0, END)
        details_entry.insert(0, data.get("details", ""))

        state_entry.delete(0, END)
        state_entry.insert(0, data.get("state", ""))

        large_image_entry.delete(0, END)
        large_image_entry.insert(0, data.get("large_image", ""))

        small_image_entry.delete(0, END)
        small_image_entry.insert(0, data.get("small_image", ""))

        button1_text_entry.delete(0, END)
        button1_text_entry.insert(0, data.get("buttons", [])[0].get("label", ""))

        button1_url_entry.delete(0, END)
        button1_url_entry.insert(0, data.get("buttons", [])[0].get("url", ""))

        button2_text_entry.delete(0, END)
        button2_text_entry.insert(0, data.get("buttons", [])[1].get("label", ""))

        button2_url_entry.delete(0, END)
        button2_url_entry.insert(0, data.get("buttons", [])[1].get("url", ""))

        Refresh()
        root.lift()



    def save_data():
        data = {
            "client_id": client_id_entry.get(),
            "details": details_entry.get(),
            "state": state_entry.get(),
            "large_image": large_image_entry.get(),
            "small_image": small_image_entry.get(),
            "buttons": [
                {"label": button1_text_entry.get(), "url": button1_url_entry.get()},
                {"label": button2_text_entry.get(), "url": button2_url_entry.get()}
            ]
        }
        with open('configs/config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("Данные сохранены в файл config.json")

    def import_config():
        global data
        try:
            # Открываем диалоговое окно проводника для выбора файла .json
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], initialdir="configs")
            if not file_path:
                root.lift()

            # Считываем данные из выбранного файла
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if set(data.keys()) != set(template_config.keys()):
                messagebox.showinfo("Ошибка", "Файл конфигурации не соответствует ожидаемому шаблону.")
                root.lift()
                return

            for button in data.get("buttons", []):
                if set(button.keys()) != set(template_config["buttons"][0].keys()):
                    messagebox.showerror("Ошибка", "Один из элементов 'buttons' не соответствует ожидаемому шаблону.")
                    root.lift()
                    return

            client_id_entry.delete(0, END)
            client_id_entry.insert(0, data.get("client_id", ""))

            details_entry.delete(0, END)
            details_entry.insert(0, data.get("details", ""))

            state_entry.delete(0, END)
            state_entry.insert(0, data.get("state", ""))

            large_image_entry.delete(0, END)
            large_image_entry.insert(0, data.get("large_image", ""))

            small_image_entry.delete(0, END)
            small_image_entry.insert(0, data.get("small_image", ""))

            button1_text_entry.delete(0, END)
            button1_text_entry.insert(0, data.get("buttons", [])[0].get("label", ""))

            button1_url_entry.delete(0, END)
            button1_url_entry.insert(0, data.get("buttons", [])[0].get("url", ""))

            button2_text_entry.delete(0, END)
            button2_text_entry.insert(0, data.get("buttons", [])[1].get("label", ""))

            button2_url_entry.delete(0, END)
            button2_url_entry.insert(0, data.get("buttons", [])[1].get("url", ""))

            root.lift()

        except FileNotFoundError:
            pass  # Можно добавить обработку ошибки, если нужно

    def export_json():
        # Считываем значения из каждой клетки ввода
        client_id = client_id_entry.get()
        details = details_entry.get()
        state = state_entry.get()
        large_image = large_image_entry.get()
        small_image = small_image_entry.get()
        buttons = [
            {"label": button1_text_entry.get(), "url": button1_url_entry.get()},
            {"label": button2_text_entry.get(), "url": button2_url_entry.get()}
        ]

        data_dict = {
            "client_id": client_id,
            "details": details,
            "state": state,
            "large_image": large_image,
            "small_image": small_image,
            "buttons": buttons
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="configs")
        if not file_path:
            root.lift()

        with open(file_path, "w", encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

        root.lift()

    root = Toplevel(window)
    root.title("Редактирование config.json")
    root.geometry("1000x800")
    root.title("Config")
    root.iconbitmap('assets/icon.ico')
    root.geometry(f"{window_weight}x{window_height}+{start_x}+{start_y}")

    root.configure(bg="#333333")

    data = load_data()

    frame = Frame(root, bg="#333333")
    # frame.pack(expand=True, fill="both", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    def is_ru_lang_keyboard():
        u = ctypes.windll.LoadLibrary("user32.dll")
        pf = getattr(u, "GetKeyboardLayout")
        return hex(pf(0)) == '0x4190419'

    def keys(event):
        if is_ru_lang_keyboard():
            if event.keycode == 86:
                event.widget.event_generate("<<Paste>>")

    client_id_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    client_id_entry.insert(0, data.get("client_id", ""))
    client_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    client_id_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Client ID:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=0, column=0, sticky="e")

    details_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    details_entry.insert(0, data.get("details", ""))
    details_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    details_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Details:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=1, column=0, sticky="e")

    state_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    state_entry.insert(0, data.get("state", ""))
    state_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    state_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="State:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=2, column=0, sticky="e")

    large_image_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    large_image_entry.insert(0, data.get("large_image", ""))
    large_image_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    large_image_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Large Image:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=3, column=0, sticky="e")

    small_image_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    small_image_entry.insert(0, data.get("small_image", ""))
    small_image_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    small_image_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Small Image:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=4, column=0, sticky="e")

    button1_text_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    button1_text_entry.insert(0, data.get("buttons", [])[0].get("label", ""))
    button1_text_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
    button1_text_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Button1 Text:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=5, column=0, sticky="e")

    button1_url_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    button1_url_entry.insert(0, data.get("buttons", [])[0].get("url", ""))
    button1_url_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")
    button1_url_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Button1 URL:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=6, column=0, sticky="e")

    button2_text_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    button2_text_entry.insert(0, data.get("buttons", [])[1].get("label", ""))
    button2_text_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
    button2_text_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Button2 Text:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=7, column=0, sticky="e")

    button2_url_entry = Entry(frame, bg="#444444", fg="white", font=("Arial", 16), insertbackground="white")
    button2_url_entry.insert(0, data.get("buttons", [])[1].get("url", ""))
    button2_url_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
    button2_url_entry.bind("<Control-KeyPress>", keys)
    Label(frame, text="Button2 URL:", fg="white", bg='#444444', font=("Arial", 16)).grid(row=8, column=0, sticky="e")

    def change_on_hover(button, color_on_hover, color_on_leave):
        button.bind("<Enter>", lambda e: button.config(bg=color_on_hover))
        button.bind("<Leave>", lambda e: button.config(bg=color_on_leave))

    save_button = Button(root, text="Сохранить", command=save_data, bg="#555555", fg="white", height=5, width=30,
                         font=("Arial", 10, "bold"))
    save_button.pack(side="right", padx=10, pady=10, anchor="se")

    import_button = Button(root, text="Import Config", command=import_config, bg="#555555", fg="white", height=2,
                           width=11, font=("Arial", 10, "bold"))
    import_button.pack(side="left", padx=10, pady=10, anchor="sw")

    export_button = Button(root, text="Export Config", command=export_json, bg="#555555", fg="white", height=2,
                           width=11, font=("Arial", 10, "bold"))
    export_button.pack(side="left", padx=10, pady=10, anchor="sw")

    refresh_button = Button(root, text="Refresh", command=reload_config_and_RPC, bg="#555555", fg="white", height=5,
                           width=30, font=("Arial", 10, "bold"))
    refresh_button.pack(side="bottom", padx=10, pady=10, anchor= "se")


    change_on_hover(save_button, "#4C4C4C", "#555555")
    change_on_hover(import_button, "#4C4C4C", "#555555")
    change_on_hover(export_button, "#4C4C4C", "#555555")
    change_on_hover(refresh_button, "#4C4C4C", "#555555")

    root.mainloop()

def open_folder():
    local_appdata_path = os.getenv('LOCALAPPDATA')
    bush_presence_path = os.path.join(local_appdata_path, 'BushPresence')
    subprocess.Popen(['explorer.exe', bush_presence_path])



def menu_action(icon, item):
    if str(item) == 'Exit':
        icon.stop()
        os._exit(0)
    elif str(item) == 'Config':
        open_config()
    elif str(item) == 'README':
        open_readme()
    elif str(item) == 'Refresh':
        Refresh()
    elif str(item) == 'Show Interface':
        window.deiconify()
    elif str(item) == 'Discord':
        open_discord()
    elif str(item) == 'Program Folder':
        open_folder()



image = Image.open("assets/icon.png")
icon = pystray.Icon("name", image, "BushPresence", menu=pystray.Menu(
    pystray.MenuItem('Show Interface', menu_action),
    pystray.MenuItem('Config', menu_action),
    pystray.MenuItem('README', menu_action),
    pystray.MenuItem('Refresh', menu_action),
    pystray.MenuItem('Discord', menu_action),
    pystray.MenuItem('Program Folder', menu_action),
    pystray.MenuItem('Exit', menu_action)
))



gui_thread = threading.Thread(target=create_gui)
gui_thread.start()

check_for_update()

icon.run()

