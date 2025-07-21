import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import copy

# 初始化表数据（文档中连接代价计算需用到的统计信息）
tables = {
    1: {'T': 1000, 'V': 10, 'name': 'R1'},
    2: {'T': 500, 'V': 20, 'name': 'R2'},
    3: {'T': 800, 'V': 15, 'name': 'R3'},
    4: {'T': 1200, 'V': 25, 'name': 'R4'}
}

# 计算两表连接代价（文档中连接代价公式）
def join_cost(r, s):
    return (r['T'] * s['T']) / max(r['V'], s['V'])

# 计算完整连接顺序的总代价（左深树结构）
def total_cost(order):
    current = tables[order[0]]
    cost = 0
    for i in range(1, len(order)):
        next_table = tables[order[i]]
        step_cost = join_cost(current, next_table)
        cost += step_cost
        # 模拟中间结果的统计信息（行数简化为连接代价，不同值取较小值）
        current = {
            'T': int(step_cost),
            'V': min(current['V'], next_table['V'])
        }
    return cost

# 初始化种群（随机生成左深连接顺序）
def init_population(size=4):
    population = []
    base = [1, 2, 3, 4]
    for _ in range(size):
        random.shuffle(base)
        population.append(copy.deepcopy(base))
    return population

# 计算适应度（代价的倒数，文档中适应度越高表示计划越优）
def calculate_fitness(population):
    fitness = []
    costs = []
    for individual in population:
        cost = total_cost(individual)
        costs.append(cost)
        fitness.append(1 / cost)  # 代价越小，适应度越高
    return fitness, costs

# 轮盘赌选择
def select(population, fitness):
    # 计算所有个体的适应度总和
    total_fit = sum(fitness)
    # 计算每个个体被选中的概率（适应度/总适应度）
    probabilities = [f / total_fit for f in fitness]
    # 初始化选择结果列表
    selected = []
    
    # 进行与种群大小相同次数的选择
    for _ in range(len(population)):
        # 生成0到1之间的随机数
        rand = random.random()
        # 初始化累积概率
        cumulative = 0
        # 轮盘赌选择过程
        for i, p in enumerate(probabilities):
            # 累加概率
            cumulative += p
            # 当累积概率大于等于随机数时，选中当前个体
            if cumulative >= rand:
                # 深拷贝被选中的个体（避免引用问题）
                selected.append(copy.deepcopy(population[i]))
                break
    # 返回选择结果
    return selected

# 两点交叉（交换中间片段，保持左深树结构合法性）
def crossover(parent1, parent2, prob=0.8):
    """
    两点交叉函数：模拟生物学中的基因交叉过程
    parent1, parent2: 两个父代个体（连接顺序）
    prob: 交叉概率，默认0.8表示80%的概率进行交叉
    """
    # 判断是否进行交叉操作（基于交叉概率）
    if random.random() < prob:
        # 选择两个交叉点：在位置1和2之间随机选择两个不同的点
        # range(1, 3)表示在索引1和2中选择，避免选择首尾位置
        point1, point2 = sorted(random.sample(range(1, 3), 2))  # 选择中间两个位置交叉
        
        # 执行交叉操作：交换两个父代在交叉点之间的基因片段
        # child1 = parent1的前段 + parent2的中段 + parent1的后段
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        # child2 = parent2的前段 + parent1的中段 + parent2的后段
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        
        # 修复重复元素（确保每个表只出现一次）
        def fix_duplicates(child, parent):
            """
            修复交叉后可能产生的重复元素问题
            child: 需要修复的子代个体
            parent: 对应的父代个体（用于确定缺失的元素）
            """
            seen = set()        # 记录已经出现的表编号
            duplicates = []     # 记录重复元素的位置索引
            
            # 遍历子代个体，找出重复的元素位置
            for i, val in enumerate(child):
                if val in seen:
                    # 如果当前元素已经出现过，记录其位置为重复位置
                    duplicates.append(i)
                else:
                    # 如果是第一次出现，加入已见集合
                    seen.add(val)
            
            # 找出缺失的元素：父代中有但子代中没有的元素
            missing = [v for v in parent if v not in seen]
            
            # 用缺失的元素替换重复的元素
            for i, pos in enumerate(duplicates):
                child[pos] = missing[i]
            
            return child
        
        # 分别修复两个子代个体的重复问题
        child1 = fix_duplicates(child1, parent1)
        child2 = fix_duplicates(child2, parent2)
        
        # 返回修复后的两个子代个体
        return child1, child2
    else:
        # 如果不进行交叉（概率为1-prob），直接返回原始父代
        return parent1, parent2

# 变异（随机交换两个位置，文档中变异用于增加多样性）
def mutate(individual, prob=0.2):
    if random.random() < prob:
        i, j = random.sample(range(4), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# 可视化每一代的优化过程
def visualize_optimization(history, costs_history):
    generations = len(history)
    fig, axes = plt.subplots(generations, 2, figsize=(15, 5*generations))
    fig.suptitle('遗传算法优化多表连接顺序过程（左深树）', fontsize=16)
    
    for gen in range(generations):
        population = history[gen]
        costs = costs_history[gen]
        best_idx = np.argmin(costs)
        
        # 左侧：展示当前代所有个体的连接顺序
        ax1 = axes[gen, 0] if generations > 1 else axes[0]
        ax1.set_title(f'第{gen+1}代 连接顺序（最优用绿色标记）')
        ax1.axis('off')
        for i, individual in enumerate(population):
            order_text = '((( '
            for idx, table in enumerate(individual):
                order_text += tables[table]['name']
                if idx < 3:
                    order_text += ' ⋈ '
            order_text += ' )))'
            color = 'green' if i == best_idx else 'black'
            ax1.text(0.1, 0.9 - i*0.2, order_text, fontsize=10, 
                    verticalalignment='top', color=color)
            ax1.text(0.8, 0.9 - i*0.2, f'代价: {int(costs[i])}', 
                    verticalalignment='top')
        
        # 右侧：代价变化曲线
        ax2 = axes[gen, 1] if generations > 1 else axes[1]
        ax2.set_title(f'第{gen+1}代 代价分布')
        ax2.bar([f'个体{i+1}' for i in range(len(costs))], costs, 
                color=['green' if i == best_idx else 'blue' for i in range(len(costs))])
        ax2.set_ylabel('总连接代价')
        ax2.axhline(y=min(costs), color='r', linestyle='--', label=f'最优代价: {int(min(costs))}')
        ax2.legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()

# 主函数：执行遗传算法并可视化
def main():
    population = init_population(size=4)
    generations = 3
    history = [population]
    costs_history = []
    
    # 计算初始代价
    fitness, costs = calculate_fitness(population)
    costs_history.append(costs)
    
    for gen in range(generations - 1):
        # 选择
        selected = select(population, fitness)
        # 交叉
        next_pop = []
        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            parent2 = selected[i+1] if i+1 < len(selected) else selected[0]
            child1, child2 = crossover(parent1, parent2)
            next_pop.append(child1)
            next_pop.append(child2)
        # 变异
        for i in range(len(next_pop)):
            next_pop[i] = mutate(next_pop[i])
        # 更新种群和历史
        population = next_pop[:4]  # 保持种群规模
        history.append(population)
        # 计算新代价
        fitness, costs = calculate_fitness(population)
        costs_history.append(costs)
    
    # 可视化
    visualize_optimization(history, costs_history)
    
    # 输出最终结果
    best_gen = np.argmin([min(c) for c in costs_history])
    best_cost = min(costs_history[best_gen])
    best_idx = costs_history[best_gen].index(best_cost)
    best_order = history[best_gen][best_idx]
    print(f"最优连接顺序: ((({tables[best_order[0]]['name']} ⋈ {tables[best_order[1]]['name']}) ⋈ {tables[best_order[2]]['name']}) ⋈ {tables[best_order[3]]['name']}))")
    print(f"最小连接代价: {int(best_cost)}")

if __name__ == "__main__":
    main()