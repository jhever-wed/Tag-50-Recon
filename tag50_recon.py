
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Tag 50 Reconciliation App (Dual-Key Match)")

# Upload files
sf_file = st.file_uploader("Upload Salesforce Tag 50 File", type=["xlsx"])
gmi_file = st.file_uploader("Upload GMI Tag 50 File", type=["xlsx"])

if sf_file and gmi_file:
    try:
        # Read the uploaded Excel files
        salesforce_df = pd.read_excel(sf_file)
        gmi_df = pd.read_excel(gmi_file)

        # Normalize key columns
        salesforce_df["Tag 50 Name"] = salesforce_df["Tag 50 Name"].astype(str).str.strip().str.upper()
        salesforce_df["Trading Account"] = salesforce_df["Trading Account"].astype(str).str.strip().str.upper()
        gmi_df["TUSER"] = gmi_df["TUSER"].astype(str).str.strip().str.upper()
        gmi_df["00003"] = gmi_df["00003"].astype(str).str.strip().str.upper()

        # Merge for reconciliation on both keys
        merged = pd.merge(
            salesforce_df,
            gmi_df,
            left_on=["Tag 50 Name", "Trading Account"],
            right_on=["TUSER", "00003"],
            how="outer",
            indicator=True
        )

        # Split into result categories
        matched = merged[merged["_merge"] == "both"]
        only_in_sf = merged[merged["_merge"] == "left_only"]
        only_in_gmi = merged[merged["_merge"] == "right_only"]

        # Show results
        st.subheader("Matched Tag 50s + Trading Account")
        st.dataframe(matched)

        st.subheader("Only in Salesforce")
        st.dataframe(only_in_sf)

        st.subheader("Only in GMI")
        st.dataframe(only_in_gmi)

        # Prepare downloadable Excel output
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            matched.to_excel(writer, sheet_name="Matched", index=False)
            only_in_sf.to_excel(writer, sheet_name="Only in Salesforce", index=False)
            only_in_gmi.to_excel(writer, sheet_name="Only in GMI", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Reconciliation Report",
            data=output,
            file_name="Tag50_Reconciliation_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload both Salesforce and GMI Excel files.")
