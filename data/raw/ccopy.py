import pandas as pd

# 1. Load both CSV files
df_source = pd.read_csv("expert_labels_old.csv")
df_target = pd.read_csv("expert_labels.csv")

# 2. Copy the column over
df_target["review_id_1"] = df_source["review_id_1"].astype("Int64")
df_target["review_id_2"] = df_source["review_id_2"].astype("Int64")

# 3. Save the updated target CSV
df_target.to_csv("expert_labels_new.csv", index=False)