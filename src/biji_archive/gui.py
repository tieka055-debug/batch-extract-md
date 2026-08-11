from __future__ import annotations

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from .exporter import export_url
from .naming import collection_name

class App:
    def __init__(self) -> None:
        self.root = tk.Tk(); self.root.title("Biji Archive"); self.root.geometry("720x430")
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.url = tk.StringVar(); self.output = tk.StringVar(value=str(Path.cwd() / "exports"))
        self.profile = tk.StringVar(value=str(Path.home() / ".biji-archive" / "chrome-profile")); self.limit = tk.StringVar(value="0")
        frame = ttk.Frame(self.root, padding=20); frame.pack(fill="both", expand=True); frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="Biji Archive", font=("Arial", 20, "bold")).grid(column=0, row=0, columnspan=3, sticky="w")
        ttk.Label(frame, text="首次导出会打开独立 Chrome，请在窗口内完成登录。", wraplength=650).grid(column=0,row=1,columnspan=3,sticky="w",pady=(6,18))
        self._field(frame, "知识库 URL", self.url, 2)
        self._field(frame, "输出目录", self.output, 3, browse=True)
        self._field(frame, "登录配置目录", self.profile, 4, browse=True)
        self._field(frame, "最多导出篇数（0=全部）", self.limit, 5)
        self.button = ttk.Button(frame, text="开始导出", command=self.start); self.button.grid(column=1,row=6,sticky="w",pady=14)
        self.status = tk.StringVar(value="准备就绪"); ttk.Label(frame,textvariable=self.status).grid(column=0,row=7,columnspan=3,sticky="w")
        self.log = tk.Text(frame,height=10,wrap="word"); self.log.grid(column=0,row=8,columnspan=3,sticky="nsew"); frame.rowconfigure(8,weight=1)
        self.root.after(100, self.poll)
    def _field(self, frame, label, value, row, browse=False):
        ttk.Label(frame,text=label).grid(column=0,row=row,sticky="w",pady=5); ttk.Entry(frame,textvariable=value).grid(column=1,row=row,sticky="ew",pady=5)
        if browse: ttk.Button(frame,text="选择",command=lambda: self.choose(value)).grid(column=2,row=row,padx=(8,0))
    def choose(self, variable):
        result=filedialog.askdirectory(initialdir=variable.get() or str(Path.home()))
        if result: variable.set(result)
    def start(self):
        if not self.url.get().startswith(("https://", "http://")):
            self.status.set("请输入完整知识库 URL"); return
        self.button.configure(state="disabled"); self.status.set("浏览器启动中…")
        threading.Thread(target=self.worker, daemon=True).start()
    def worker(self):
        try:
            out=Path(self.output.get())/collection_name(self.url.get())
            r=export_url(self.url.get(),out,Path(self.profile.get()),int(self.limit.get() or 0))
            self.events.put(("done",f"完成：{r.exported} 篇\n{r.output_dir}"))
        except Exception as e: self.events.put(("done",f"失败：{type(e).__name__}: {e}"))
    def poll(self):
        try:
            while True:
                kind,msg=self.events.get_nowait(); self.log.insert("end",str(msg)+"\n"); self.log.see("end"); self.status.set("完成"); self.button.configure(state="normal")
        except queue.Empty: pass
        self.root.after(100,self.poll)

def main() -> None: App().root.mainloop()
