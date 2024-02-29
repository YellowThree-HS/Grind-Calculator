import tkinter as tk

class MapItemsCalculator:
    def __init__(self, master):
        self.master = master
        master.title("地图道具计算器")

        # 预设的地图产出配置
        self.default_map_items = {
            "地图1": ["A", "B"],
            "地图2": ["A", "C"],
            "地图3": ["B", "D"],
            "地图4": ["C", "E"],
            "地图5": ["D", "F"],
            "地图6": ["E", "F"],
            "地图7": ["A", "D"],
            "地图8": ["B", "C"]
        }

        # 标签：提示用户输入地图道具
        self.label = tk.Label(master, text="输入地图道具：")
        self.label.grid(row=0, column=0, columnspan=3)

        # 创建地图道具的输入框，并设置默认值
        self.entries = {}
        row = 1
        for map_name, items in self.default_map_items.items():
            label = tk.Label(master, text=map_name)
            label.grid(row=row, column=0)
            entry_A = tk.Entry(master)
            entry_A.insert(0, items[0])  # 设置默认值
            entry_A.grid(row=row, column=1)
            entry_B = tk.Entry(master)
            entry_B.insert(0, items[1])  # 设置默认值
            entry_B.grid(row=row, column=2)
            self.entries[map_name] = (entry_A, entry_B)
            row += 1

        # 标签：提示用户输入所需道具数量
        self.label_needed_items = tk.Label(master, text="输入所需道具数量：")
        self.label_needed_items.grid(row=row, column=0, columnspan=3)

        # 创建所需道具的输入框
        self.entry_items = {}
        for i, item in enumerate(["A", "B", "C", "D", "E", "F"], start=1):
            label = tk.Label(master, text=item)
            label.grid(row=row + i, column=0)
            entry = tk.Entry(master)
            entry.grid(row=row + i, column=1)
            self.entry_items[item] = entry

        # 创建计算按钮
        self.calculate_button = tk.Button(master, text="计算", command=self.calculate)
        self.calculate_button.grid(row=row + 7, column=0, columnspan=3)

        # 创建结果显示标签
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=row + 8, column=0, columnspan=3)

    # 计算方法
    def calculate(self):
        # 从输入框读取地图产出配置
        maps = {}
        for map_name, (entry_A, entry_B) in self.entries.items():
            item_A = entry_A.get().upper()
            item_B = entry_B.get().upper()
            maps[map_name] = [item_A, item_B]

        # 读取所需道具数量
        needs = {item: int(entry.get()) for item, entry in self.entry_items.items()}

        # 初始化地图刷取次数记录
        map_counts = {map_name: 0 for map_name in self.default_map_items}

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

        # 显示结果
        result_text = "\n".join([f"{map_name}: {count}次" for map_name, count in map_counts.items()])
        self.result_label.config(text="需要刷的次数：\n" + result_text)

def main():
    root = tk.Tk()
    app = MapItemsCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
