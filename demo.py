from itertools import combinations

# 道具产出情况
maps = {
    1: ["A", "B"],
    2: ["A", "C"],
    3: ["B", "D"],
    4: ["C", "E"],
    5: ["D", "F"],
    6: ["E", "F"],
    7: ["A", "D"],
    8: ["B", "C"],
}
# 道具需求量更新为题目要求的数量
needs_update = {"A": 99, "B": 0, "C": 0, "D": 2, "E": 2, "F": 2}

# 地图刷取次数记录
map_counts = {map_id: 0 for map_id in maps}

# 循环，直到所有道具需求被满足
while not all(need <= 0 for need in needs_update.values()):
    # 对每个地图，计算它的贡献度
    contributions = {}
    for map_id, items in maps.items():
        contribution = sum(max(0, needs_update[item]) for item in items)
        contributions[map_id] = contribution

    # 选择贡献度最高的地图
    max_contribution_map = max(contributions, key=contributions.get)

    # 更新道具需求量
    for item in maps[max_contribution_map]:
        needs_update[item] -= 1

    # 更新地图刷取次数
    map_counts[max_contribution_map] += 1

# 检查是否所有需求都满足并输出地图刷取次数
all_satisfied = all(need <= 0 for need in needs_update.values())

for map_id, count in map_counts.items():
    if count > 0:
        print(f"地图{map_id}刷取{count}次")
