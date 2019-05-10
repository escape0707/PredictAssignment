# %% [markdown]
#  # 搜集碎片拼图游戏概率——编程求解与检验
#
#  **问题：**
#
#  有 $a$ 幅画，每一幅被分解为 $b$ 张碎片，所有碎片混合到一起，从里面随机抽取 $k$ 张 $(b<k<a*b)$，那么这 $k$ 张碎片恰好组合出至少一幅完整作品的概率为多少？
#
#  **假设的答案：**
#
#  $P = \frac{\sum_{i=1}^{\left \lfloor \frac{k}{b} \right \rfloor} (i \mod 2 * 2 - 1){a \choose i}{ab-ib \choose k-ib}}{{ab \choose k}}$
#
#  **实验与验证的设计：**
#  1. 组合数预处理函数
#  2. 枚举所有组合并验证的测试方法
#  3. 真正随机抽取并统计的测试方法
#  4. 预测函数
#  5. 同样条件下2-4三种方法的结果的统计与绘图表达
# %% [markdown]
#  ## 组合数预处理函数：
# %%
# The max resonable a * b
maxN = 100
# The pre-processed combination numbers
C = [[None] * (i + 1) for i in range(maxN)]


def preprocess() -> None:
    for i in range(maxN):
        for j in range(i + 1):
            if j in {0, i}:
                C[i][j] = 1
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
# %% [markdown]
#  测试预处理生成的结果：
# %%
preprocess()
C
# %% [markdown]
#  ## 枚举所有组合并计算概率：
# %%
import itertools

combinations = None


def enumerate_calc(a: int, b: int, k: int) -> float:
    """Calculate the possibility using enumerating method.

    Parameters
    ----------
    a : int
        Total of paintings
    b : int
        Total of fragments into which a painting was divided
    k : int
        Total of fragments picked

    Returns
    -------
    P : float
        The possibility that those fragments you picked can assemble at least one painting
    """

    combinations = itertools.combinations(range(a * b), k)
    # Total of combinations which at least contain one complete painting
    bingo_count = 0
    combination_count = 0

    for picked in combinations:
        combination_count += 1
        painting_index = 0
        fragment_count = 0
        for fragment in picked:
            index = fragment // b
            if index == painting_index:
                fragment_count += 1
            else:
                painting_index = index
                fragment_count = 1
            if fragment_count == b:
                bingo_count += 1
                break

    P = bingo_count / combination_count
    return P
# %% [markdown]
#  ## 我提出的解答函数：
# %%
def predict(a: int = 10, b: int = 9, k: int = 28) -> float:
    """Predict the possibility asked in the question.

    Parameters
    ----------
    a : int
        Total of paintings
    b : int
        Total of fragments into which a painting was divided
    k : int
        Total of fragments picked

    Returns
    -------
    P : float
        The possibility that those fragments you picked can assemble at least one painting
    """

    # Compute how many paintings can you assemble from k fragments at the most.
    maxI = k // b

    P = 0
    for i in range(1, maxI + 1):
        P += (i % 2 * 2 - 1) * C[a][i] * C[a * b - i * b][k - i * b]
    P /= C[a * b][k]

    return P
# %% [markdown]
#  ## 测试函数：
# %%
test = 6

def run_test(test_a = test, test_b = test):
    for a in range(1, test_a):
        for b in range(1, test_b):
            for k in range(b, a * b + 1):
                print(a, b, k)
                my_answer = predict(a, b, k)
                print(a, b, k)
                ground_truth = enumerate_calc(a, b, k)
                print(my_answer, ground_truth)
                if my_answer != ground_truth:
                    print('What?')
                    print(a, b, k)
                    return
    print('Finished.')
# %% [markdown]
#  进行测试：
# %%
run_test()                    