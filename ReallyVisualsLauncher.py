import os, sys, json, threading, subprocess, uuid, hashlib, urllib.request, tkinter as tk
from tkinter import ttk, messagebox, simpledialog

APP_NAME = "ReallyVisuals"
ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = getattr(sys, "_MEIPASS", ROOT)
GAME_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), ".minecraft")
CONFIG = os.path.join(ROOT, "launcher_config.json")
VERSIONS = ["1.12.2", "1.16.5", "1.20.1", "1.20.4", "1.21.1", "1.21.4", "1.21.11"]
ORANGE = "#ff7918"
BG = "#101012"
PANEL = "#17171b"
MUTED = "#85858f"
WHITE = "#f4f4f5"

def load_config():
    try:
        with open(CONFIG, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return {"username": "Player", "version": "1.16.5", "memory": 4, "fabric": True, "accounts": ["Player"]}

def save_config(c):
    with open(CONFIG, "w", encoding="utf-8") as f: json.dump(c, f, ensure_ascii=False, indent=2)

class Launcher:
    def __init__(self, root):
        self.root = root
        self.cfg = load_config()
        self.root.title("ReallyVisuals Launcher")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        self.busy = False
        self.page = "home"
        self.status = tk.StringVar(value="Готов к запуску")
        self.build()
        self.show_page("home")

    def button(self, parent, text, command, primary=False, width=None):
        b = tk.Button(parent, text=text, command=command, bg=ORANGE if primary else "#242429",
                      fg="#171719" if primary else WHITE, activebackground="#ff9145" if primary else "#33333a",
                      activeforeground="#111111" if primary else WHITE, relief="flat", bd=0,
                      font=("Segoe UI", 10, "bold"), padx=18, pady=11, cursor="hand2")
        if width: b.configure(width=width)
        return b

    def build(self):
        top = tk.Frame(self.root, bg="#141416", height=66)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="RV", fg=ORANGE, bg="#141416", font=("Segoe UI Black", 25, "bold")).pack(side="left", padx=(22,12))
        tk.Label(top, text="ReallyVisuals", fg=WHITE, bg="#141416", font=("Segoe UI", 16, "bold")).pack(side="left")
        self.account_btn = self.button(top, self.cfg.get("username","Player")+"  ▾", self.accounts)
        self.account_btn.pack(side="right", padx=20, pady=12)
        self.nav = tk.Frame(self.root, bg="#141416", height=48)
        self.nav.pack(fill="x")
        for label, page in [("Главная","home"),("Visuals","visuals"),("Версии","versions"),("Настройки","settings")]:
            self.button(self.nav, label, lambda p=page:self.show_page(p)).pack(side="left", padx=(16,0), pady=5)
        self.body = tk.Frame(self.root, bg=BG)
        self.body.pack(fill="both", expand=True, padx=28, pady=24)
        footer = tk.Frame(self.root, bg="#141416", height=42)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(footer, text="reallyvisuals  •  Windows 11", bg="#141416", fg=MUTED, font=("Segoe UI",9)).pack(side="left", padx=20)
        tk.Label(footer, textvariable=self.status, bg="#141416", fg=MUTED, font=("Segoe UI",9)).pack(side="right", padx=20)

    def clear(self):
        for w in self.body.winfo_children(): w.destroy()

    def show_page(self, page):
        self.page = page
        self.clear()
        if page == "home": self.home()
        elif page == "visuals": self.visuals()
        elif page == "versions": self.versions_page()
        else: self.settings()

    def title(self, parent, text, sub=None):
        tk.Label(parent, text=text, bg=BG, fg=WHITE, font=("Segoe UI",25,"bold")).pack(anchor="w")
        if sub: tk.Label(parent, text=sub, bg=BG, fg=MUTED, font=("Segoe UI",10)).pack(anchor="w", pady=(5,18))

    def home(self):
        left = tk.Frame(self.body, bg=BG)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(self.body, bg=PANEL, width=390)
        right.pack(side="right", fill="y", padx=(25,0))
        right.pack_propagate(False)
        tk.Label(left, text="REALLY VISUALS", fg=ORANGE, bg="#392114", padx=14, pady=8, font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(95,20))
        tk.Label(left, text="Визуал —", fg=WHITE, bg=BG, font=("Segoe UI",26,"bold")).pack(anchor="w")
        tk.Label(left, text="без компромиссов", fg=ORANGE, bg=BG, font=("Segoe UI",26,"bold")).pack(anchor="w")
        tk.Label(left, text="Minecraft launcher • Fabric • Visuals", fg=MUTED, bg=BG, font=("Segoe UI",11)).pack(anchor="w", pady=(14,30))
        row = tk.Frame(left, bg=BG); row.pack(anchor="w")
        self.button(row, "Играть  ▶", self.play, True, 17).pack(side="left", padx=(0,12))
        self.button(row, "Установить версию", lambda:self.show_page("versions")).pack(side="left")
        tk.Label(left, text="Выбранная версия", bg=BG, fg=MUTED, font=("Segoe UI",10)).pack(anchor="w", pady=(35,5))
        tk.Label(left, text=self.cfg.get("version","1.16.5"), bg=BG, fg=WHITE, font=("Segoe UI",17,"bold")).pack(anchor="w")
        tk.Label(right, text="ПРОФИЛЬ ЗАПУСКА", bg=PANEL, fg=ORANGE, font=("Segoe UI",10,"bold")).pack(anchor="w", padx=24, pady=(25,14))
        for label, value in [("Игрок",self.cfg.get("username","Player")),("Minecraft",self.cfg.get("version","1.16.5")),("Загрузчик","Fabric" if self.cfg.get("fabric",True) and self.cfg.get("version")!="1.12.2" else "Vanilla"),("Память",str(self.cfg.get("memory",4))+" GB")]:
            box=tk.Frame(right,bg="#202025"); box.pack(fill="x", padx=20, pady=5)
            tk.Label(box,text=label,bg="#202025",fg=MUTED,font=("Segoe UI",9)).pack(anchor="w",padx=13,pady=(8,0))
            tk.Label(box,text=value,bg="#202025",fg=WHITE,font=("Segoe UI",11,"bold")).pack(anchor="w",padx=13,pady=(0,8))
        self.button(right,"Управление аккаунтами",self.accounts).pack(fill="x", padx=20, pady=(18,8))
        self.button(right,"Настройки запуска",lambda:self.show_page("settings")).pack(fill="x", padx=20)

    def visuals(self):
        self.title(self.body,"Visuals","Визуальные профили и совместимость модификаций")
        note=tk.Frame(self.body,bg=PANEL); note.pack(fill="x",pady=5)
        tk.Label(note,text="ReallyVisuals 1.0.0",bg=PANEL,fg=ORANGE,font=("Segoe UI",16,"bold")).pack(anchor="w",padx=20,pady=(18,4))
        tk.Label(note,text="Загруженный тобой JAR — Fabric-мод для Minecraft 1.16.5.",bg=PANEL,fg=WHITE,font=("Segoe UI",11)).pack(anchor="w",padx=20)
        tk.Label(note,text="На других версиях этот JAR не включается: нужны отдельные совместимые сборки.",bg=PANEL,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=20,pady=(5,18))
        self.button(self.body,"Установить ReallyVisuals для 1.16.5",self.install_mod,True).pack(anchor="w",pady=15)
        tk.Label(self.body,text="Другие версии пока используют чистый Minecraft/Fabric. Раздел Visuals здесь — управление доступностью мода, а не подмена игровых шейдеров.",bg=BG,fg=MUTED,wraplength=800,justify="left").pack(anchor="w",pady=8)

    def versions_page(self):
        self.title(self.body,"Версии Minecraft","Выбери игровую версию и загрузчик")
        grid=tk.Frame(self.body,bg=BG); grid.pack(anchor="w")
        self.version_var=tk.StringVar(value=self.cfg.get("version","1.16.5"))
        for i,v in enumerate(VERSIONS):
            r,c=divmod(i,4)
            rb=tk.Radiobutton(grid,text=v,variable=self.version_var,value=v,indicatoron=0,width=16,padx=10,pady=14,
                bg="#242429",fg=WHITE,selectcolor=ORANGE,activebackground="#33333a",activeforeground=WHITE,
                font=("Segoe UI",11,"bold"),command=self.version_changed)
            rb.grid(row=r,column=c,padx=7,pady=7)
        self.fabric_var=tk.BooleanVar(value=self.cfg.get("fabric",True))
        tk.Checkbutton(self.body,text="Установить Fabric (для 1.12.2 недоступен — будет Vanilla)",variable=self.fabric_var,
                       bg=BG,fg=WHITE,selectcolor=PANEL,activebackground=BG,activeforeground=WHITE,font=("Segoe UI",10)).pack(anchor="w",pady=20)
        self.button(self.body,"Сохранить выбор",self.save_version,True).pack(anchor="w")
        self.button(self.body,"Установить выбранную версию",self.install_selected).pack(anchor="w",pady=12)

    def version_changed(self):
        pass

    def save_version(self):
        self.cfg["version"]=self.version_var.get()
        self.cfg["fabric"]=self.fabric_var.get()
        save_config(self.cfg); self.status.set("Версия сохранена"); self.show_page("versions")

    def settings(self):
        self.title(self.body,"Настройки","Параметры запуска Minecraft")
        tk.Label(self.body,text="Выделенная память (GB)",bg=BG,fg=WHITE,font=("Segoe UI",11,"bold")).pack(anchor="w")
        self.mem_var=tk.IntVar(value=int(self.cfg.get("memory",4)))
        ttk.Style().configure("TCombobox",fieldbackground=PANEL,background=PANEL,foreground=WHITE)
        combo=ttk.Combobox(self.body,textvariable=self.mem_var,values=[2,3,4,6,8,10,12],state="readonly",width=10)
        combo.pack(anchor="w",pady=8)
        tk.Label(self.body,text="Папка игры: "+GAME_DIR,bg=BG,fg=MUTED,font=("Segoe UI",9),wraplength=850).pack(anchor="w",pady=15)
        self.button(self.body,"Сохранить настройки",self.save_settings,True).pack(anchor="w")
        tk.Label(self.body,text="Аккаунты: локальные профили (ник для одиночной игры/LAN). Для официальных онлайн-серверов потребуется вход Microsoft.",bg=BG,fg=MUTED,wraplength=850,justify="left").pack(anchor="w",pady=20)

    def save_settings(self):
        self.cfg["memory"]=int(self.mem_var.get()); save_config(self.cfg); self.status.set("Настройки сохранены")

    def accounts(self):
        win=tk.Toplevel(self.root); win.title("Аккаунты"); win.geometry("420x390"); win.configure(bg=BG)
        tk.Label(win,text="Профили игрока",bg=BG,fg=WHITE,font=("Segoe UI",18,"bold")).pack(anchor="w",padx=20,pady=18)
        lb=tk.Listbox(win,bg=PANEL,fg=WHITE,selectbackground=ORANGE,relief="flat",font=("Segoe UI",11),height=9)
        lb.pack(fill="both",expand=True,padx=20)
        accounts=self.cfg.setdefault("accounts",[self.cfg.get("username","Player")])
        for a in accounts: lb.insert("end",a)
        def choose():
            s=lb.curselection()
            if s:
                self.cfg["username"]=accounts[s[0]]; save_config(self.cfg)
                self.account_btn.configure(text=self.cfg["username"]+"  ▾"); self.status.set("Профиль выбран"); win.destroy(); self.show_page(self.page)
        def add():
            name=simpledialog.askstring("Новый профиль","Введи игровой ник:",parent=win)
            if name and name.strip():
                name=name.strip()[:16]
                if name not in accounts: accounts.append(name); lb.insert("end",name); save_config(self.cfg)
        def delete():
            s=lb.curselection()
            if s and len(accounts)>1:
                idx=s[0]; accounts.pop(idx); lb.delete(idx); save_config(self.cfg)
        row=tk.Frame(win,bg=BG); row.pack(fill="x",padx=20,pady=14)
        self.button(row,"Выбрать",choose,True).pack(side="left",padx=(0,7))
        self.button(row,"＋ Создать",add).pack(side="left",padx=7)
        self.button(row,"Удалить",delete).pack(side="left",padx=7)

    def set_busy(self, val, message=None):
        self.busy=val
        if message: self.root.after(0,lambda:self.status.set(message))

    def worker(self, fn):
        if self.busy: return
        self.set_busy(True,"Подготовка…")
        def run():
            try: fn()
            except Exception as e:
                self.root.after(0,lambda:messagebox.showerror("ReallyVisuals Launcher",str(e)))
                self.set_busy(False,"Ошибка")
            else: self.set_busy(False,"Готово")
        threading.Thread(target=run,daemon=True).start()

    def get_lib(self):
        try: import minecraft_launcher_lib
        except ImportError:
            self.root.after(0,lambda:self.status.set("Устанавливаю компонент запуска…"))
            subprocess.check_call([sys.executable,"-m","pip","install","minecraft-launcher-lib"])
            import minecraft_launcher_lib
        return minecraft_launcher_lib

    def install_selected(self):
        self.save_version()
        version=self.cfg["version"]; use_fabric=self.cfg.get("fabric",True) and version!="1.12.2"
        def task():
            lib=self.get_lib()
            self.set_busy(True,"Загрузка Minecraft "+version+"…")
            lib.install.install_minecraft_version(version,GAME_DIR)
            if use_fabric:
                self.set_busy(True,"Установка Fabric…")
                lib.fabric.install_fabric(version,GAME_DIR)
            self.root.after(0,lambda:messagebox.showinfo("Установка завершена",f"Minecraft {version} установлен"+(" с Fabric." if use_fabric else ".")))
        self.worker(task)

    def install_mod(self):
        def task():
            lib=self.get_lib()
            version="1.16.5"
            lib.install.install_minecraft_version(version,GAME_DIR)
            lib.fabric.install_fabric(version,GAME_DIR)
            mods=os.path.join(GAME_DIR,"mods"); os.makedirs(mods,exist_ok=True)
            src=os.path.join(RESOURCE_DIR,"reallyvisuals-1.0.0.jar")
            if not os.path.isfile(src): raise FileNotFoundError("В папке лаунчера нет reallyvisuals-1.0.0.jar")
            shutil.copy2(src,os.path.join(mods,"reallyvisuals-1.0.0.jar"))
            self.root.after(0,lambda:messagebox.showinfo("Готово","Fabric для 1.16.5 установлен. ReallyVisuals JAR скопирован в .minecraft/mods."))
        import shutil
        self.worker(task)

    def play(self):
        version=self.cfg.get("version","1.16.5")
        def task():
            lib=self.get_lib()
            # install if missing; for Fabric the installed profile is version-loader
            use_fabric=self.cfg.get("fabric",True) and version!="1.12.2"
            target=version
            if use_fabric:
                try: lib.fabric.install_fabric(version,GAME_DIR)
                except Exception: pass
                # locate installed fabric profile
                candidates=[x["id"] for x in lib.utils.get_installed_versions(GAME_DIR)]
                matches=[x for x in candidates if x.startswith("fabric-loader-") and version in x]
                if matches: target=sorted(matches)[-1]
            else:
                lib.install.install_minecraft_version(version,GAME_DIR)
            username=self.cfg.get("username","Player")
            offline_uuid=uuid.uuid3(uuid.NAMESPACE_DNS,"OfflinePlayer:"+username).hex
            options={"username":username,"uuid":offline_uuid,"token":"0",
                     "jvmArguments":[f"-Xmx{self.cfg.get('memory',4)}G"],
                     "launcherName":"ReallyVisuals","launcherVersion":"1.0.0"}
            command=lib.command.get_minecraft_command(target,GAME_DIR,options)
            self.set_busy(True,"Запускаю Minecraft…")
            subprocess.Popen(command,cwd=GAME_DIR)
            self.root.after(0,lambda:self.status.set("Minecraft запущен"))
        self.worker(task)

if __name__ == "__main__":
    root=tk.Tk()
    try: ttk.Style().theme_use("clam")
    except Exception: pass
    Launcher(root)
    root.mainloop()
