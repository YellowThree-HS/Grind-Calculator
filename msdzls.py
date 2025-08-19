import tkinter as tk
from tkinter import messagebox
import os

class MapItemsCalculator:
    def __init__(self, master):
        self.master = master
        master.title("刷图计算器（锑食版）V1.1")
        master.geometry("500x500")  # 设置初始窗口大小

        # 创建Frame
        map_frame = tk.Frame(master)
        item_frame = tk.Frame(master)
        result_frame = tk.Frame(master)
        map_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        item_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
        result_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

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

        # 创建地图道具输入
        self.entries = {}
        tk.Label(map_frame, text="输入地图道具：（大写字母）").grid(row=0, column=0, columnspan=2, sticky="w")
        row = 1
        for map_name, items in self.default_map_items.items():
            tk.Label(map_frame, text=map_name).grid(row=row, column=0, sticky="w")
            entry_A = tk.Entry(map_frame, width=5)
            entry_A.insert(0, items[0])
            entry_A.grid(row=row, column=1, sticky="w")
            entry_B = tk.Entry(map_frame, width=5)
            entry_B.insert(0, items[1])
            entry_B.grid(row=row, column=2, sticky="w")
            self.entries[map_name] = (entry_A, entry_B)
            row += 1

        # 创建所需道具输入
        self.entry_items = {}
        tk.Label(item_frame, text="输入所需道具数量：（支持加法）").grid(row=0, column=0, columnspan=2, sticky="w")
        for i, item in enumerate(["A", "B", "C", "D", "E", "F"], start=1):
            label = tk.Label(item_frame, text=item, anchor="w")
            label.grid(row=i, column=0, sticky="w")
            entry = tk.Entry(item_frame, width=10)
            entry.insert(0, "0")
            entry.grid(row=i, column=1, sticky="w")
            self.entry_items[item] = entry

        # 添加重置按钮
        self.reset_button = tk.Button(result_frame, text="重置", command=self.reset)
        self.reset_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # 添加保存按钮
        self.save_button = tk.Button(result_frame, text="保存", command=self.save)
        self.save_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 添加读取按钮
        self.load_button = tk.Button(result_frame, text="读取", command=self.load)
        self.load_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # 创建计算按钮
        self.calculate_button = tk.Button(result_frame, text="计算", command=self.calculate)
        self.calculate_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # 切换计算方法的选项
        self.calc_method = tk.StringVar(value="min")
        self.calc_min_button = tk.Radiobutton(result_frame, text="最小地图", variable=self.calc_method, value="min")
        self.calc_max_button = tk.Radiobutton(result_frame, text="最大地图", variable=self.calc_method, value="max")
        self.calc_min_button.grid(row=0, column=4, padx=5, sticky="w")
        self.calc_max_button.grid(row=0, column=5, padx=5, sticky="w")
        
        # 创建结果显示区域（使用Text组件支持多行显示）
        self.result_frame = tk.Frame(master)
        self.result_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nw")
        
        tk.Label(self.result_frame, text="计算结果：", anchor="w").grid(row=0, column=0, sticky="w")
        self.result_text = tk.Text(self.result_frame, height=8, width=50)
        self.result_text.grid(row=1, column=0, sticky="nw")
        scrollbar = tk.Scrollbar(self.result_frame, command=self.result_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 制作信息 - 使用Frame确保左对齐
        info_frame = tk.Frame(master)
        info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # 创建左对齐的标签
        info_label = tk.Label(
            info_frame, 
            text="制作by98服小白233\n改进by114服某不知名玩家\n部分代码由Deepseek生成，请仔细甄别",
            justify=tk.LEFT,  # 设置文本左对齐
            anchor="w"  # 设置锚点为西（左）
        )
        info_label.pack(anchor="w")  # 在Frame内左对齐

    def calculate(self):
        maps = {}
        for map_name, (entry_A, entry_B) in self.entries.items():
            item_A = entry_A.get().upper().strip()
            item_B = entry_B.get().upper().strip()
            if item_A == "" or item_B == "":
                self.show_result("错误：地图道具不能为空")
                return
            maps[map_name] = [item_A, item_B]
        
        # 验证道具字母是否有效
        all_items = set(item for items in maps.values() for item in items)
        for item in all_items:
            if len(item) != 1 or not item.isalpha():
                self.show_result(f"错误：无效的道具标识 '{item}'\n请使用单个大写字母")
                return
        
        # 读取所需道具数量
        needs = {}
        for item, entry in self.entry_items.items():
            entry_text = entry.get().strip()
            try:
                # 移除空格后尝试计算表达式
                if entry_text == "":
                    needs[item] = 0
                else:
                    # 安全地计算表达式（仅支持数字和加法）
                    expr = entry_text.replace(" ", "")
                    if any(c not in "0123456789+" for c in expr):
                        raise ValueError("包含非法字符")
                    needs[item] = eval(expr)
            except Exception as e:
                self.show_result(f"错误：{item}的输入 '{entry_text}' 无效\n只支持数字和加法")
                return
        
        # 初始化地图刷取次数记录
        map_counts = {map_name: 0 for map_name in self.default_map_items}
        
        # 创建临时需要的道具数量副本
        temp_needs = needs.copy()
        
        # 实现算法逻辑
        if self.calc_method.get() == "max":
            while not all(need <= 0 for need in temp_needs.values()):
                contributions = {}
                max_contribution = float("-inf")
                max_contribution_map = None
                
                for map_name, items in maps.items():
                    contribution = 0
                    for item in items:
                        if item in temp_needs and temp_needs[item] > 0:
                            contribution += temp_needs[item]
                    contributions[map_name] = contribution
                    
                    if contribution > max_contribution:
                        max_contribution = contribution
                        max_contribution_map = map_name
                
                if max_contribution_map:
                    for item in maps[max_contribution_map]:
                        if item in temp_needs:
                            temp_needs[item] = max(0, temp_needs[item] - 1)
                    map_counts[max_contribution_map] += 1
                else:
                    break
        else:  # min方法
            while not all(need <= 0 for need in temp_needs.values()):
                contributions = {}
                for map_name, items in maps.items():
                    contribution = 0
                    for item in items:
                        if item in temp_needs and temp_needs[item] > 0:
                            contribution += temp_needs[item]
                    contributions[map_name] = contribution
                
                # 找到贡献最大的地图
                max_contribution_map = max(contributions, key=contributions.get)
                
                if contributions[max_contribution_map] > 0:
                    for item in maps[max_contribution_map]:
                        if item in temp_needs:
                            temp_needs[item] = max(0, temp_needs[item] - 1)
                    map_counts[max_contribution_map] += 1
                else:
                    break
        
        # 显示结果
        result_lines = []
        total_maps = 0
        for map_name, count in map_counts.items():
            if count > 0:
                result_lines.append(f"地图 {map_name} 刷取 {count} 次")
                total_maps += count
        
        if total_maps == 0:
            result_lines.append("无需刷任何地图")
        else:
            result_lines.insert(0, f"总计需要刷 {total_maps} 次地图：")
        
        self.show_result("\n".join(result_lines))

    def reset(self):
        """重置所有输入到默认值"""
        # 重置地图道具输入
        for map_name, (entry_A, entry_B) in self.entries.items():
            default_A, default_B = self.default_map_items[map_name]
            entry_A.delete(0, tk.END)
            entry_A.insert(0, default_A)
            entry_B.delete(0, tk.END)
            entry_B.insert(0, default_B)
        
        # 重置所需道具数量
        for entry in self.entry_items.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        
        # 清空结果显示
        self.result_text.delete(1.0, tk.END)
        messagebox.showinfo("重置成功", "已恢复到默认配置")

    def save(self):
        """保存当前配置到文件"""
        try:
            with open("map_data.txt", "w", encoding="utf-8") as f:
                # 保存地图配置
                for map_name, (entry_A, entry_B) in self.entries.items():
                    item_A = entry_A.get().strip()
                    item_B = entry_B.get().strip()
                    f.write(f"{map_name}:{item_A},{item_B}\n")
                
                # 保存道具需求配置
                for item, entry in self.entry_items.items():
                    value = entry.get().strip()
                    f.write(f"{item}:{value}\n")
            
            messagebox.showinfo("保存成功", "配置已保存到 map_data.txt")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存配置时出错:\n{str(e)}")

    def load(self):
        """从文件加载配置"""
        if not os.path.exists("map_data.txt"):
            messagebox.showerror("加载失败", "找不到配置文件 map_data.txt")
            return
        
        try:
            with open("map_data.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # 处理地图配置（前7行）
            for i, line in enumerate(lines[:7]):
                parts = line.strip().split(":")
                if len(parts) < 2:
                    continue
                
                map_name = parts[0]
                items = parts[1].split(",")
                if map_name in self.entries and len(items) == 2:
                    entry_A, entry_B = self.entries[map_name]
                    entry_A.delete(0, tk.END)
                    entry_A.insert(0, items[0])
                    entry_B.delete(0, tk.END)
                    entry_B.insert(0, items[1])
            
            # 处理道具需求配置（后6行）
            for i, line in enumerate(lines[7:13]):
                parts = line.strip().split(":")
                if len(parts) == 2:
                    item = parts[0]
                    value = parts[1]
                    if item in self.entry_items:
                        entry = self.entry_items[item]
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
            
            messagebox.showinfo("加载成功", "配置已从 map_data.txt 加载")
        except Exception as e:
            messagebox.showerror("加载失败", f"加载配置时出错:\n{str(e)}")

    def show_result(self, text):
        """在结果区域显示文本"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

def main():
    root = tk.Tk()
    app = MapItemsCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
