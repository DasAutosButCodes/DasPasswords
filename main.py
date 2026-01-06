import random, json, os, time
import customtkinter as ctk

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_+=:;<,>.?/"
PATH = os.path.join(os.environ["USERPROFILE"], "Documents", "PasswordApp")
os.makedirs(PATH, exist_ok=True)

class PasswordRelated(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DasPasswords!")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.passwords = {}

        # PASSWORD GENERATOR SECTION #
        self.generator_frame = ctk.CTkFrame(self, width=500, height=570)
        self.generator_frame.pack(padx=(25, 10), pady=15, side="left")
        self.generator_frame.pack_propagate(False)

        self.pas_text = ctk.CTkLabel(self.generator_frame, text="Пароль", font=("Arial", 12), text_color="grey")
        self.pas_text.pack(anchor="w", pady=(25, 0), padx=(12, 0))
        self.pas_frame = ctk.CTkFrame(self.generator_frame, fg_color="transparent")
        self.pas_frame.pack(fill="x")
        self.pas_entry = ctk.CTkEntry(self.pas_frame, width=365, height=45, font=("Arial", 24))
        self.pas_entry.pack(padx=(10, 0), side="left", anchor="nw")
        self.pas_reroll = ctk.CTkButton(self.pas_entry, command=self.generate_password, width=25, height=25, text="⟳", font=("Arial", 24), fg_color="transparent")
        self.pas_reroll.place(in_=self.pas_entry, relx=1.0, x=-5, rely=0.5, anchor="e")
        self.pas_copy = ctk.CTkButton(self.pas_frame, command=lambda: self.copy(self.pas_entry.get()), width=45, height=45, text="📋", font=("Segoe UI Emoji", 24))
        self.pas_copy.pack(side="left", padx=10)
        self.pas_save = ctk.CTkButton(self.pas_frame, command=lambda: self.open_password_dialog(), width=45, height=45, text="💾", font=("Segoe UI Emoji", 24))
        self.pas_save.pack(side="left")

        self.leng_text = ctk.CTkLabel(self.generator_frame, text="Длина пароля", font=("Arial", 12), text_color="grey")
        self.leng_text.pack(anchor="w", pady=(15, 0), padx=(12, 0))
        self.pas_length_frame = ctk.CTkFrame(self.generator_frame, fg_color="transparent")
        self.pas_length_frame.pack(fill="x")
        self.length = ctk.IntVar(value=12)
        self.pas_length = ctk.CTkSlider(self.pas_length_frame, height=20, width=450, from_=1, to=50, number_of_steps=49, orientation="horizontal", variable=self.length,
                                        command=self.generate_password)
        self.pas_length.pack(padx=(10, 5), side="left")
        self.length_text = ctk.CTkLabel(self.pas_length_frame, text="", font=("Arial", 24))
        self.length_text.pack(side="left")

        self.addUppercase = ctk.BooleanVar()
        self.addLowercase = ctk.BooleanVar()
        self.addDigits = ctk.BooleanVar()
        self.addSymbols = ctk.BooleanVar()

        self.set_text = ctk.CTkLabel(self.generator_frame, text="Изменить символы", font=("Arial", 12), text_color="grey")
        self.set_text.pack(anchor="w", pady=(15, 0), padx=(12, 0))
        self.settings_frame = ctk.CTkFrame(self.generator_frame, fg_color="transparent")
        self.settings_frame.pack(fill="x")
        self.lowercase_switch = ctk.CTkSwitch(self.settings_frame, text="a-z", variable=self.addLowercase, font=("Arial", 24), switch_width=100, switch_height=25, command=lambda: self.update_chars(LOWER, self.addLowercase))
        self.lowercase_switch.grid(row=0, column=0, padx=45, pady=10)
        self.uppercase_switch = ctk.CTkSwitch(self.settings_frame, text="A-Z", variable=self.addUppercase, font=("Arial", 24), switch_width=100, switch_height=25, command=lambda:self.update_chars(UPPER, self.addUppercase))
        self.uppercase_switch.grid(row=1, column=0, padx=45, pady=10)
        self.digits_switch = ctk.CTkSwitch(self.settings_frame, text="1-9", variable=self.addDigits, font=("Arial", 24), switch_width=100, switch_height=25, command=lambda:self.update_chars(DIGITS, self.addDigits))
        self.digits_switch.grid(row=0, column=1, padx=45, pady=10)
        self.symbols_switch = ctk.CTkSwitch(self.settings_frame, text="@!#", variable=self.addSymbols, font=("Arial", 24), switch_width=100, switch_height=25, command=lambda:self.update_chars(SYMBOLS, self.addSymbols))
        self.symbols_switch.grid(row=1, column=1, padx=45, pady=10)

        self.set_text = ctk.CTkLabel(self.generator_frame, text="Разрешенные символы", font=("Arial", 12),
                                     text_color="grey")
        self.set_text.pack(anchor="w", pady=(15, 0), padx=(12, 0))
        self.allowed_chars = ctk.CTkTextbox(self.generator_frame, height=120, font=("Arial", 24), fg_color="gray23")
        self.allowed_chars.pack(fill="x", padx=10)

        # PASSWORD MANAGER SECTION #
        self.manager_frame = ctk.CTkFrame(self, width=380, height=570)
        self.manager_frame.pack(padx=(10, 25), pady=15, side="right")
        self.manager_frame.pack_propagate(False)

        self.inner_frame = ctk.CTkScrollableFrame(self.manager_frame)
        self.inner_frame.pack(fill="both", expand=True)

        self.on_open()

    def generate_password(self, length=None):
        if length == None: length = self.length.get()
        length = int(length)
        self.length_text.configure(text=length)

        text = self.allowed_chars.get("1.0", "end-1c")
        if not text: return
        password = "".join(random.choice(text) for _ in range(length))
        self.pas_entry.delete(0, "end")
        self.pas_entry.insert(0, password)

    def update_chars(self, chars, toggled):
        current = set(self.allowed_chars.get("1.0", "end-1c"))
        if toggled.get():
            current.update(chars)
        else:
            current.difference_update(chars)
        self.allowed_chars.delete("1.0", "end")
        self.allowed_chars.insert("1.0", "".join(sorted(current)))

    def create_pas_frame(self, mark, login, password):
        login_frame = ctk.CTkFrame(self.inner_frame)
        login_frame.pack(pady=(10, 5), padx=10, fill="x")
        log_font, pas_font = 26, 18
        mark_label = ctk.CTkLabel(login_frame, text=self.shorten(mark, 10), font=("Arial", 12), text_color="grey")
        mark_label.pack(padx=5, pady=(3, 0), anchor="w")
        login_label = ctk.CTkLabel(login_frame, text=self.shorten(login, 12), font=("Arial", log_font, "bold"))
        login_label.pack(pady=(0, 5), padx=5, anchor="w")
        password_label = ctk.CTkLabel(login_frame, text=self.shorten(password, 16), font=("Arial", pas_font))
        password_label.pack(pady=(3, 10), padx=5, anchor="w")

        id = str(int(time.time() * 1000))
        login_data = {
            "mark": mark,
            "login": login,
            "password": password,
            "id": id
        }
        self.passwords[id] = login_data

        card_data = {
            "mark": mark_label,
            "login": login_label,
            "password": password_label,
            "card": login_frame
        }

        copy_log_btn = ctk.CTkButton(login_frame, text="👤", command=lambda: self.copy(login_data["login"]),
                                     width=35, height=35, font=("Arial", 24), fg_color="transparent")
        copy_log_btn.place(relx=0.85, rely=0.4, anchor='center')

        copy_pas_btn = ctk.CTkButton(login_frame, text="🗝", command=lambda: self.copy(login_data["password"]),
                                     width=35, height=35, font=("Arial", 24), fg_color="transparent")
        copy_pas_btn.place(relx=0.85, rely=0.75, anchor='center')

        def open_editor(event, pid=id):
            self.open_password_dialog(self.passwords[pid], card_data)

        for clickable in login_frame, login_label, password_label:
            clickable.bind("<Button-1>", open_editor)
            clickable.bind("<Enter>", lambda e: login_frame.configure(cursor="hand2"))
        login_frame.bind("<Leave>", lambda e: login_frame.configure(cursor=""))

    def open_password_dialog(self, pas_data=None, card_data=None):
        is_edit = pas_data is not None

        root, mark_entry, login_entry, password_entry = self.password_window(
            pas_data["mark"] if is_edit else "",
            pas_data["login"] if is_edit else "",
            pas_data["password"] if is_edit else self.pas_entry.get()
        )

        def save():
            mark = mark_entry.get("0.0", "end-1c")
            login = login_entry.get("0.0", "end-1c")
            password = password_entry.get("0.0", "end-1c")

            if is_edit:
                pas_data.update({"mark": mark, "login": login, "password": password})
                card_data["mark"].configure(text=self.shorten(mark, 10))
                card_data["login"].configure(text=self.shorten(login, 12))
                card_data["password"].configure(text=self.shorten(password, 16))
            else:
                self.create_pas_frame(mark, login, password)

            root.destroy()

        save_btn = ctk.CTkButton(root, text="Сохранить", font=("Arial", 26), command=save)
        save_btn.pack()

        def delete_login():
            root.destroy()
            card_data["card"].destroy()
            self.passwords.pop(pas_data['id'])

        if is_edit:
            delete_btn = ctk.CTkButton(root, text="🗑", width=40, height=40, font=("Arial", 22), fg_color="#8B0000", hover_color="#A00000",
                                       command=delete_login)
            delete_btn.place(relx=0.8, rely=0.845)

    def password_window(self, mark, login, password):
        root = ctk.CTkToplevel(self)
        root.bind("<Escape>", lambda e: root.destroy())
        root.geometry("350x420")
        root.title("Сохранение пароля")
        root.attributes("-topmost", True)
        root.grab_set()

        mark_txt = ctk.CTkLabel(root, text="С чем связан", text_color="gray55", font=("Arial", 12))
        mark_txt.place(x=15, y=5)
        mark_entry = ctk.CTkTextbox(root, width=325, height=50, font=("Arial", 24))
        mark_entry.insert(0.0, mark)
        mark_entry.pack(pady=(30, 15), padx=12)

        login_txt = ctk.CTkLabel(root, text="Логин", text_color="gray55", font=("Arial", 12))
        login_txt.place(x=15, y=85)
        login_entry = ctk.CTkTextbox(root, width=325, height=100, font=("Arial", 24))
        login_entry.insert(0.0, login)
        login_entry.pack(pady=15, padx=12)

        password_txt = ctk.CTkLabel(root, text="Пароль", text_color="gray55", font=("Arial", 12))
        password_txt.place(x=15, y=215)
        password_entry = ctk.CTkTextbox(root, width=325, height=100, font=("Arial", 24))
        password_entry.insert(0.0, password)
        password_entry.pack(pady=15, padx=12)

        root.after(100, login_entry.focus)
        return root, mark_entry, login_entry, password_entry

    def copy(self, copy):
        self.clipboard_clear()
        self.clipboard_append(copy)
        self.update()

    def shorten(self, s, l):
        return s if len(s) <= l else f"{s[:l]}…"

    def on_open(self):
        path = os.path.join(PATH, "dasPasswords.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # password generator
                for key, value in data["settings"].items():
                    if key in ["addUppercase", "addLowercase", "addDigits", "addSymbols"]:
                        getattr(self, key).set(value)
                self.allowed_chars.insert("1.0", data["settings"]["allowed_chars"].strip())
                self.length.set(data["settings"]["length"])
                self.generate_password()
                # password manager
                if data["passwords"]:
                    for i in list(data["passwords"].values()):
                        self.create_pas_frame(i["mark"], i["login"], i["password"])


    def on_close(self):
        path = os.path.join(PATH, "dasPasswords.json")
        settings_data = {
            "addUppercase": self.addUppercase.get(),
            "addLowercase": self.addLowercase.get(),
            "addDigits": self.addDigits.get(),
            "addSymbols": self.addSymbols.get(),
            "length": self.length.get(),
            "allowed_chars": self.allowed_chars.get("1.0", "end-1c")
        }
        data = {
            "settings": settings_data,
            "passwords": self.passwords,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.destroy()

if __name__ == "__main__":
    app = PasswordRelated()
    app.mainloop()