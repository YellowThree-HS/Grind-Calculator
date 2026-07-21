import tkinter as tk
from tkinter import messagebox

class MapItemsCalculator:
    def __init__(self, master):
        self.master = master
        master.title("刷图计算器（锑食版）V1.3")
        master.geometry("500x500")
        master.minsize(440, 380)

        # 预设的地图产出配置
        self.default_map_items = {
            "神殿": ["A", "B"],
            "深渊": ["C", "D"],
            "城堡": ["E", "F"],
            "港口": ["A", "C"],
            "火山": ["B", "D"],
            "花园": ["A", "F"],
            "飞船": ["D", "E"]
        }

        # ===== 上方统一容器（左对齐） =====
        top_frame = tk.Frame(master)
        top_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # 地图道具配置（左栏）
        map_frame = tk.LabelFrame(top_frame, text="地图道具配置", padx=3, pady=3)
        map_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 3), sticky="nw")
        tk.Label(map_frame, text="地图", font=("", 8, "bold"), width=4).grid(row=0, column=0, padx=2)
        tk.Label(map_frame, text="道具1", font=("", 8, "bold"), width=4).grid(row=0, column=1, padx=2)
        tk.Label(map_frame, text="道具2", font=("", 8, "bold"), width=4).grid(row=0, column=2, padx=2)

        self.entries = {}
        for r, (map_name, items) in enumerate(self.default_map_items.items(), start=1):
            tk.Label(map_frame, text=map_name, width=4, anchor="e").grid(row=r, column=0, padx=2)
            entry_A = tk.Entry(map_frame, width=5, justify="center")
            entry_A.insert(0, items[0])
            entry_A.grid(row=r, column=1, padx=2)
            entry_B = tk.Entry(map_frame, width=5, justify="center")
            entry_B.insert(0, items[1])
            entry_B.grid(row=r, column=2, padx=2)
            self.entries[map_name] = (entry_A, entry_B)

        # 所需道具数量（右栏）
        item_frame = tk.LabelFrame(top_frame, text="所需道具数量（支持加减法）", padx=3, pady=3)
        item_frame.grid(row=0, column=1, pady=(0, 3), sticky="nw")
        self.entry_items = {}
        for i, item in enumerate(["A", "B", "C", "D", "E", "F"]):
            tk.Label(item_frame, text=f"道具 {item}", width=6, anchor="e").grid(row=i, column=0, padx=2)
            entry = tk.Entry(item_frame, width=8, justify="center")
            entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=2)
            self.entry_items[item] = entry

        # 操作按钮
        button_frame = tk.Frame(top_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        tk.Button(button_frame, text="重置", command=self.reset, width=7).pack(side="left", padx=1)
        tk.Button(button_frame, text="读取", command=self.load, width=7).pack(side="left", padx=1)
        tk.Button(button_frame, text="保存", command=self.save, width=7).pack(side="left", padx=1)
        tk.Button(button_frame, text="计算", command=self.calculate, width=7).pack(side="left", padx=1)
        self.calc_method = tk.StringVar(value="min")
        tk.Radiobutton(button_frame, text="最小地图", variable=self.calc_method, value="min").pack(
            side="left", padx=(8, 1))
        tk.Radiobutton(button_frame, text="最大地图", variable=self.calc_method, value="max").pack(
            side="left", padx=1)

        # ===== 下方：计算结果 =====
        result_frame = tk.LabelFrame(master, text="计算结果", padx=3, pady=3)
        result_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.result_text = tk.Text(result_frame, width=30, state="disabled")
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 制作信息
        tk.Label(master, text="制作by98服小白233\n改进by114服某不知名玩家",
                 anchor="w", justify="left", fg="gray").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5)

    # 计算方法
    def calculate(self):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        maps = {}
        for map_name, (entry_A, entry_B) in self.entries.items():
            item_A = entry_A.get().strip().upper()
            item_B = entry_B.get().strip().upper()
            if not item_A or not item_B:
                self.result_text.insert(tk.END, f'错误：地图"{map_name}"的道具输入不能为空\n')
                self.result_text.config(state="disabled")
                return
            if not (item_A.isalpha() and len(item_A) == 1 and item_B.isalpha() and len(item_B) == 1):
                self.result_text.insert(tk.END, f'错误：地图"{map_name}"的道具必须是单个字母\n')
                self.result_text.config(state="disabled")
                return
            maps[map_name] = [item_A, item_B]

        needs = {}
        for item, entry in self.entry_items.items():
            entry_text = entry.get().strip()
            if not entry_text:
                needs[item] = 0
                continue
            allowed = set("0123456789+-() ")
            if not all(c in allowed for c in entry_text):
                self.result_text.insert(tk.END, f'错误：道具"{item}"输入包含非法字符\n')
                self.result_text.config(state="disabled")
                return
            try:
                result = eval(entry_text)
                if not isinstance(result, (int, float)):
                    raise ValueError
                needs[item] = result
            except Exception:
                self.result_text.insert(tk.END, f'错误：道具"{item}"输入无效: {entry_text}\n')
                self.result_text.config(state="disabled")
                return

        map_counts = {map_name: 0 for map_name in self.default_map_items}
        if self.calc_method.get() == "max":
            while not all(need <= 0 for need in needs.values()):
                contributions = {}
                max_contribution = float("-inf")
                max_contribution_map = None
                for map_name, items in maps.items():
                    contribution = sum(max(0, needs[item]) for item in items)
                    contributions[map_name] = contribution
                    if contribution >= max_contribution:
                        max_contribution = contribution
                        max_contribution_map = map_name

                if max_contribution_map:
                    for item in maps[max_contribution_map]:
                        needs[item] -= 1
                    map_counts[max_contribution_map] += 1
                else:
                    break
        else:
            while not all(need <= 0 for need in needs.values()):
                contributions = {}
                for map_name, items in maps.items():
                    contribution = sum(max(0, needs[item]) for item in items)
                    contributions[map_name] = contribution
                max_contribution_map = max(contributions, key=contributions.get, default=None)
                if max_contribution_map:
                    for item in maps[max_contribution_map]:
                        needs[item] -= 1
                    map_counts[max_contribution_map] += 1
                else:
                    break

        result_text = ""
        for map_name, count in map_counts.items():
            if count > 0:
                result_text += f"地图{map_name}刷取{count}次\n"

        if not result_text:
            result_text = "无需刷图"

        self.result_text.insert(tk.END, "需要刷的次数：\n" + result_text)
        self.result_text.config(state="disabled")

    def reset(self):
        if not messagebox.askyesno("确认重置", "确定要重置所有设置为默认值吗？\n此操作不可撤销。"):
            return
        for map_name, (entry_A, entry_B) in self.entries.items():
            items = self.default_map_items[map_name]
            entry_A.delete(0, tk.END)
            entry_A.insert(0, items[0])
            entry_B.delete(0, tk.END)
            entry_B.insert(0, items[1])
        for entry in self.entry_items.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        self.calc_method.set("min")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

    def save(self):
        if not messagebox.askyesno("确认保存", "保存配置将覆盖 map_data.txt 中的现有配置。\n确定要继续吗？"):
            return
        try:
            with open("map_data.txt", "w", encoding="utf-8") as f:
                for map_name, (entry_A, entry_B) in self.entries.items():
                    f.write(f"{map_name}:{entry_A.get()},{entry_B.get()}\n")
                f.write("NEEDS:\n")
                for item, entry in self.entry_items.items():
                    f.write(f"{item}:{entry.get()}\n")
                f.write(f"METHOD:{self.calc_method.get()}\n")
            messagebox.showinfo("保存成功", "配置已保存到 map_data.txt")
        except PermissionError:
            messagebox.showerror("保存失败", "没有写入权限，无法保存文件")
        except OSError as e:
            messagebox.showerror("保存失败", f"写入文件时出错：{e}")

    def load(self):
        if not __import__("os").path.exists("map_data.txt"):
            messagebox.showwarning("读取失败", "未找到 map_data.txt 文件")
            return
        try:
            with open("map_data.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            mode = "maps"
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == "NEEDS:":
                    mode = "needs"
                    continue
                if line.startswith("METHOD:"):
                    method = line.split(":", 1)[1]
                    self.calc_method.set(method)
                    continue
                if mode == "maps":
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        map_name = parts[0]
                        items = parts[1].split(",")
                        if map_name in self.entries and len(items) == 2:
                            self.entries[map_name][0].delete(0, tk.END)
                            self.entries[map_name][0].insert(0, items[0])
                            self.entries[map_name][1].delete(0, tk.END)
                            self.entries[map_name][1].insert(0, items[1])
                elif mode == "needs":
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        item = parts[0]
                        if item in self.entry_items:
                            self.entry_items[item].delete(0, tk.END)
                            self.entry_items[item].insert(0, parts[1])
            messagebox.showinfo("读取成功", "配置已从 map_data.txt 加载")
        except PermissionError:
            messagebox.showerror("读取失败", "没有读取权限")
        except OSError as e:
            messagebox.showerror("读取失败", f"读取文件时出错：{e}")
def main():
    root = tk.Tk()
    app = MapItemsCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
