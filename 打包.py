import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

# 安装依赖
def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        messagebox.showinfo("完成", "依赖安装成功！\nPyInstaller 已安装")
    except Exception as e:
        messagebox.showerror("错误", f"安装失败：{str(e)}")

# 打包 exe
def build_exe(script_path, app_name, icon_path=""):
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 单文件
        "--windowed", # 无控制台
        f"--name={app_name}", # 程序名
    ]
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    cmd.append(script_path)

    try:
        subprocess.check_call(cmd)
        return True
    except:
        return False

# 生成 Inno 安装脚本
def create_iss_script(app_name, exe_path, output_dir):
    iss_content = f"""[Setup]
AppName={app_name}
AppVersion=1.0
DefaultDirName={{autopf}}\\{app_name}
DefaultGroupName={app_name}
OutputDir={output_dir}
OutputBaseFilename={app_name}_Setup
Compression=lzma
SolidCompression=yes
Uninstallable=yes

[Files]
Source: "{exe_path}"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\{app_name}"; Filename: "{{app}}\\{app_name}.exe"
Name: "{{commondesktop}}\\{app_name}"; Filename: "{{app}}\\{app_name}.exe"
"""
    iss_path = os.path.join(output_dir, f"{app_name}_installer.iss")
    with open(iss_path, "w", encoding="utf-8") as f:
        f.write(iss_content)
    return iss_path

# 编译安装包
def compile_installer(iss_path):
    iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not os.path.exists(iscc_path):
        iscc_path = filedialog.askopenfilename(title="找到 ISCC.exe", filetypes=[("EXE", "*.exe")])
    
    try:
        subprocess.check_call([iscc_path, iss_path])
        return True
    except:
        return False

# GUI 主程序
class InstallerMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("安装包生成器 v1.0")
        self.root.geometry("600x400")

        # 变量
        self.script_path = tk.StringVar()
        self.app_name = tk.StringVar(value="MyApp")
        self.icon_path = tk.StringVar()
        self.status_text = tk.StringVar(value="准备就绪")

        # UI
        ttk.Label(root, text="程序源码：").pack(pady=5)
        ttk.Entry(root, textvariable=self.script_path, width=60).pack()
        ttk.Button(root, text="选择文件", command=self.select_script).pack(pady=2)

        ttk.Label(root, text="应用名称：").pack(pady=5)
        ttk.Entry(root, textvariable=self.app_name, width=30).pack()

        ttk.Label(root, text="图标（.ico）：").pack(pady=5)
        ttk.Entry(root, textvariable=self.icon_path, width=60).pack()
        ttk.Button(root, text="选择图标", command=self.select_icon).pack(pady=2)

        ttk.Button(root, text="安装依赖", command=lambda: Thread(target=install_dependencies, daemon=True).start()).pack(pady=5)
        ttk.Button(root, text="开始生成安装包", command=self.start_build, style="Accent.TButton").pack(pady=10)

        ttk.Label(root, textvariable=self.status_text).pack(pady=5)

    def select_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("所有文件", "*.*")])
        if path:
            self.script_path.set(path)

    def select_icon(self):
        path = filedialog.askopenfilename(filetypes=[("图标", "*.ico")])
        if path:
            self.icon_path.set(path)

    def start_build(self):
        Thread(target=self.build_thread, daemon=True).start()

    def build_thread(self):
        self.status_text.set("正在打包 exe...")
        if not build_exe(self.script_path.get(), self.app_name.get(), self.icon_path.get()):
            messagebox.showerror("失败", "EXE 打包失败")
            return

        self.status_text.set("正在生成安装脚本...")
        exe_path = os.path.join("dist", f"{self.app_name.get()}.exe")
        iss_file = create_iss_script(self.app_name.get(), exe_path, "dist")

        self.status_text.set("正在编译安装包...")
        if compile_installer(iss_file):
            self.status_text.set("✅ 安装包生成完成！")
            messagebox.showinfo("成功", f"安装包已保存到：\n{os.path.abspath('dist')}")
            os.startfile("dist")
        else:
            messagebox.showerror("失败", "安装包编译失败")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("Accent.TButton", font=("微软雅黑", 10, "bold"))
    InstallerMaker(root)
    root.mainloop()