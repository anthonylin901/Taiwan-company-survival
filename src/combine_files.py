import glob
import pandas as pd

for kind in ["setup", "dissolve"]:

    # 找出資料夾裡所有 CSV 檔
    files = sorted(glob.glob(f"../data/raw/{kind}/*.csv"))
    print(kind, "檔案數：", len(files))

    tables = []
    for path in files:
        df = pd.read_csv(path, dtype=str)
        df = df.drop(columns=["代表人"], errors="ignore")
        df["source_file"] = path.split("/")[-1]
        tables.append(df)

    # 把所有月份接在一起
    all_df = pd.concat(tables, ignore_index=True)
    all_df.to_csv(f"../data/processed/{kind}_all.csv", index=False)

    print("總筆數：", len(all_df))
    print("不重複統編數：", all_df["統一編號"].nunique())
    print("欄位：", all_df.columns.tolist())
    print()