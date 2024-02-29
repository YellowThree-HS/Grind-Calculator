import tkinter as tk

class MapItemsCalculator:
    def __init__(self, master):
        self.master = master
        master.title("刷图计算器（锑食版）V1.0")

        # 创建Frame
        map_frame = tk.Frame(master)
        item_frame = tk.Frame(master)
        result_frame = tk.Frame(master)
        map_frame.grid(row=0, column=0, padx=10, pady=10)
        item_frame.grid(row=0, column=1, padx=10, pady=10)
        result_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


        # 预设的地图产出配置
        self.default_map_items = {
            "神殿": ["A", "B"],
            "深渊": ["A", "C"],
            "城堡": ["B", "D"],
            "港口": ["C", "E"],
            "火山": ["D", "F"],
            "花园": ["E", "F"],
            "飞船": ["A", "D"]
        }

        # 创建地图道具输入
        self.entries = {}  # 确保这行在循环之前
        tk.Label(map_frame, text="输入地图道具：（大写字母）").grid(row=0, column=0, columnspan=2)
        row = 1
        for map_name, items in self.default_map_items.items():
            tk.Label(map_frame, text=map_name).grid(row=row, column=0)
            entry_A = tk.Entry(map_frame)
            entry_A.insert(0, items[0])  # 设置默认值
            entry_A.grid(row=row, column=1)
            entry_B = tk.Entry(map_frame)
            entry_B.insert(0, items[1])  # 设置默认值
            entry_B.grid(row=row, column=2)
            self.entries[map_name] = (entry_A, entry_B)  # 更新self.entries字典
            row += 1

        # 创建所需道具输入
        self.entry_items = {}  # 确保这行在循环之前
        # 创建所需道具的输入框, 并设置默认值为0
        for i, item in enumerate(["A", "B", "C", "D", "E", "F"], start=1):
            label = tk.Label(item_frame, text=item)  # 使用item_frame作为父容器
            label.grid(row=i, column=0)
            entry = tk.Entry(item_frame)  # 使用item_frame作为父容器
            entry.insert(0, "0")  # 设置默认值为 "0"
            entry.grid(row=i, column=1)
            self.entry_items[item] = entry  # 将输入框加入到字典中

        # 添加重置按钮
        self.reset_button = tk.Button(result_frame, text="重置", command=self.reset)
        self.reset_button.grid(row=0, column=0, sticky="w", padx=(5,0), pady=(5, 0))

        # 添加保存按钮
        self.save_button = tk.Button(result_frame, text="保存", command=self.save)
        self.save_button.grid(row=0, column=1, sticky="w", padx=(5,0), pady=(5, 0))

        # 添加读取按钮
        self.load_button = tk.Button(result_frame, text="读取", command=self.load)
        self.load_button.grid(row=0, column=2, sticky="w", padx=(5,0), pady=(5, 0))

        # 创建计算按钮和结果显示标签
        self.calculate_button = tk.Button(result_frame, text="计算", command=self.calculate)
        self.calculate_button.grid(row=0, column=3, sticky="w", padx=(5,0), pady=(5, 0))

        # 切换计算方法的选项
        self.calc_method = tk.StringVar(value="min")
        self.calc_min_button = tk.Radiobutton(result_frame, text="最小地图", variable=self.calc_method, value="min")
        self.calc_max_button = tk.Radiobutton(result_frame, text="最大地图", variable=self.calc_method, value="max")
        self.calc_min_button.grid(row=0, column=4, sticky="w", padx=(5,0), pady=(5, 0))
        self.calc_max_button.grid(row=0, column=5, sticky="w", padx=(5,0), pady=(5, 0))
        # 创建结果显示标签
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=2, column=0)
        # 制作信息
        tk.Label(master, text="制作by98服小白233（只有计算有用，别的还没做）").grid(row=3, column=0, sticky="w", pady=(10, 0))

    # 计算方法
    def calculate(self):
        maps = {}
        for map_name, (entry_A, entry_B) in self.entries.items():
            item_A = entry_A.get().upper()
            item_B = entry_B.get().upper()
            maps[map_name] = [item_A, item_B]
        # 读取所需道具数量，并尝试解析可能的加法表达式
        needs = {}
        for item, entry in self.entry_items.items():
            entry_text = entry.get()
            try:
                # 确保输入仅包含数字和加号
                if all(c.isdigit() or c == '+' for c in entry_text.replace(" ", "")):
                    needs[item] = eval(entry_text)
                else:
                    raise ValueError(f"Invalid input for {item}: {entry_text}")
            except SyntaxError:
                self.result_label.config(text=f"无效输入: {entry_text}")
                return

        # 初始化地图刷取次数记录
        map_counts = {map_name: 0 for map_name in self.default_map_items}
        # 实现之前的算法逻辑
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

                # 更新需要的道具数量和地图刷取次数
                if max_contribution_map:
                    for item in maps[max_contribution_map]:
                        needs[item] -= 1
                    map_counts[max_contribution_map] += 1
                else:
                    break
        else:
            # 实现之前的算法逻辑
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

        # 显示结果，大于0次的地图才显示
        result_text = ""
        for map_name, count in map_counts.items():
            if count > 0:  # 只显示刷取次数大于0的地图
                result_text += f"地图{map_name}刷取{count}次\n"

        # 更新结果显示标签
        self.result_label.config(text="需要刷的次数：\n" + result_text)

    def reset(self):
        # 重置所有输入框到默认值
        pass

    def save(self):
        # 保存当前配置到map_data.txt
        pass

    def load(self):
        # 从map_data.txt加载配置
        pass
def main():
    root = tk.Tk()
    app = MapItemsCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
