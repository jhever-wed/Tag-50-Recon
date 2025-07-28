
import pandas as pd

# Load Salesforce and GMI files
salesforce_df = pd.read_excel("tag50 with accounts.xlsx")
gmi_df = pd.read_excel("tag50 GMI.xlsx")

# Normalize comparison columns
salesforce_df["Tag 50 Name"] = salesforce_df["Tag 50 Name"].astype(str).strip().str.upper()
gmi_df["TUSER"] = gmi_df["TUSER"].astype(str).strip().str.upper()

# Merge on Tag 50 field
merged = pd.merge(
    salesforce_df,
    gmi_df,
    left_on="Tag 50 Name",
    right_on="TUSER",
    how="outer",
    indicator=True
)

# Separate matches and mismatches
matched = merged[merged['_merge'] == 'both']
only_in_salesforce = merged[merged['_merge'] == 'left_only']
only_in_gmi = merged[merged['_merge'] == 'right_only']

# Output all results to Excel
with pd.ExcelWriter("Tag50_Reconciliation_Report.xlsx") as writer:
    matched.to_excel(writer, sheet_name="Matched", index=False)
    only_in_salesforce.to_excel(writer, sheet_name="Only in Salesforce", index=False)
    only_in_gmi.to_excel(writer, sheet_name="Only in GMI", index=False)

print("[✔] Reconciliation complete. Output saved to Tag50_Reconciliation_Report.xlsx")
