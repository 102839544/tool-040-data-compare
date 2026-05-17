#!/usr/bin/env python3
"""
数据对比工具 - 对比两个CSV/JSON文件的差异
"""
import sys, json, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
import tkinter as tk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("数据对比工具 v1.0")
        root.geometry("900x650")
        self.file1 = None
        self.file2 = None
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#00796b", height=50)
        f.pack(fill="x")
        tk.Label(f, text="⚖️ 数据对比工具", font=("Arial",14,"bold"),
                 fg="white", bg="#00796b").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 文件选择
        ff = tk.Frame(main)
        ff.pack(fill="x", pady=10)
        
        tk.Button(ff, text="选择文件1", command=lambda: self.select_file(1),
                  bg="#00796b", fg="white", padx=12).pack(side="left", padx=5)
        self.file1_label = tk.Label(ff, text="未选择", fg="gray")
        self.file1_label.pack(side="left", padx=10)
        
        tk.Button(ff, text="选择文件2", command=lambda: self.select_file(2),
                  bg="#00796b", fg="white", padx=12).pack(side="left", padx=30)
        self.file2_label = tk.Label(ff, text="未选择", fg="gray")
        self.file2_label.pack(side="left", padx=10)
        
        # 对比选项
        of = tk.Frame(main)
        of.pack(fill="x", pady=5)
        tk.Label(of, text="对比键列：").pack(side="left")
        self.key_col = tk.Entry(of, width=20)
        self.key_col.pack(side="left", padx=5)
        self.key_col.insert(0, "id")
        
        tk.Button(of, text="开始对比", command=self.compare,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="right", padx=10)
        
        # 结果
        tk.Label(main, text="对比结果：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,5))
        self.result_txt = scrolledtext.ScrolledText(main, font=("Consolas",10), height=20)
        self.result_txt.pack(fill="both", expand=True)
        
        self.status = tk.Label(main, text="选择两个CSV或JSON文件进行对比",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def select_file(self, num):
        f = filedialog.askopenfilename(title=f"选择文件{num}",
             filetypes=[("数据文件","*.csv *.json")])
        if f:
            if num == 1:
                self.file1 = f
                self.file1_label.config(text=Path(f).name)
            else:
                self.file2 = f
                self.file2_label.config(text=Path(f).name)
    
    def compare(self):
        if not self.file1 or not self.file2:
            messagebox.showwarning("提示", "请选择两个文件")
            return
        if not HAS_PANDAS:
            messagebox.showerror("缺少依赖", "请运行：pip install pandas")
            return
        
        try:
            # 加载文件
            if self.file1.endswith(".json"):
                df1 = pd.read_json(self.file1)
            else:
                df1 = pd.read_csv(self.file1)
            
            if self.file2.endswith(".json"):
                df2 = pd.read_json(self.file2)
            else:
                df2 = pd.read_csv(self.file2)
            
            key = self.key_col.get().strip()
            if key not in df1.columns or key not in df2.columns:
                messagebox.showerror("错误", f"键列 '{key}' 不存在于文件中")
                return
            
            # 对比
            result = []
            result.append(f"文件1：{Path(self.file1).name} ({len(df1)} 行)")
            result.append(f"文件2：{Path(self.file2).name} ({len(df2)} 行)")
            result.append("=" * 50)
            
            # 找出差异
            set1 = set(df1[key].astype(str))
            set2 = set(df2[key].astype(str))
            
            only_in_1 = set1 - set2
            only_in_2 = set2 - set1
            common = set1 & set2
            
            result.append(f"\n仅文件1有：{len(only_in_1)} 条")
            if only_in_1 and len(only_in_1) <= 20:
                result.append("  " + ", ".join(sorted(only_in_1)))
            
            result.append(f"\n仅文件2有：{len(only_in_2)} 条")
            if only_in_2 and len(only_in_2) <= 20:
                result.append("  " + ", ".join(sorted(only_in_2)))
            
            result.append(f"\n共同记录：{len(common)} 条")
            
            self.result_txt.delete(1.0, "end")
            self.result_txt.insert(1.0, "\n".join(result))
            self.status.config(text="✅ 对比完成")
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 对比失败")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
