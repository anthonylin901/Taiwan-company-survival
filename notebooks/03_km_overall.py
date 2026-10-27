import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# Mac 顯示中文的字型
plt.rcParams["font.family"] = "Arial Unicode MS"

# 讀取存活分析表
df = pd.read_csv("../data/processed/survival_2015.csv")

# 建立並計算 KM 曲線
kmf = KaplanMeierFitter()
kmf.fit(
    durations=df["duration_months"],
    event_observed=df["event"],
    label="2015 年設立的公司",
)

# 印出幾個關鍵時間點的存活率
print(kmf.survival_function_at_times([12, 36, 60, 120]))
print("中位存活月數：", kmf.median_survival_time_)

# 畫圖
kmf.plot_survival_function()
plt.xlabel("成立後月數")
plt.ylabel("存活率")
plt.title("台灣 2015 年設立公司的存活曲線")
plt.ylim(0, 1)
plt.savefig("../reports/figures/km_overall.png", dpi=150)
plt.show()