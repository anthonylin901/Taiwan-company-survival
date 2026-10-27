import pandas as pd

setup = pd.read_csv("../data/processed/setup_all.csv", dtype=str)
dissolve = pd.read_csv("../data/processed/dissolve_all.csv", dtype=str)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 10)

print("===== 設立清冊的重複 =====")
dup = setup[setup.duplicated("統一編號", keep=False)]
print(dup.sort_values("統一編號").drop(columns=["公司所在地"]))

print()
print("===== 解散清冊的重複（前 20 筆）=====")
dup = dissolve[dissolve.duplicated("統一編號", keep=False)]
print(dup.sort_values("統一編號").drop(columns=["公司所在地"]).head(20))