
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PHCIP School Submission Dashboard", layout="wide")

st.title("📊 PHCIP School Submission Dashboard")
st.markdown("Upload the **master PHCIP school list** and the **submitted schools list** to generate a district-wise dashboard showing total, submitted, and pending schools.")

# Upload master school list
master_file = st.file_uploader("📂 Upload Master PHCIP School List", type=["xlsx"], key="master")
# Upload submitted school list
submitted_file = st.file_uploader("📂 Upload Submitted Schools List", type=["xlsx"], key="submitted")

if master_file and submitted_file:
    try:
        # Load master school list
        df_master = pd.read_excel(master_file, sheet_name=0, engine='openpyxl')
        # Load submitted school list
        df_submitted = pd.read_excel(submitted_file, sheet_name=0, engine='openpyxl')

        # Count total schools per district
        total_schools = df_master['District'].value_counts().reset_index()
        total_schools.columns = ['District', 'Total Schools']

        # Count submitted schools per district
        submitted_schools = df_submitted['District'].value_counts().reset_index()
        submitted_schools.columns = ['District', 'Submitted']

        # Merge and calculate pending
        dashboard = pd.merge(total_schools, submitted_schools, on='District', how='left')
        dashboard['Submitted'] = dashboard['Submitted'].fillna(0).astype(int)
        dashboard['Pending'] = dashboard['Total Schools'] - dashboard['Submitted']

        # Add total row
        total_row = pd.DataFrame([{
            'District': 'Total',
            'Total Schools': dashboard['Total Schools'].sum(),
            'Submitted': dashboard['Submitted'].sum(),
            'Pending': dashboard['Pending'].sum()
        }])
        dashboard = pd.concat([dashboard, total_row], ignore_index=True)

        # Display dashboard
        st.subheader("📋 District-wise Summary")
        st.dataframe(dashboard, use_container_width=True)

        # Download button
        output = BytesIO()
        dashboard.to_excel(output, index=False, engine='openpyxl')
        st.download_button(
            label="📥 Download Dashboard as Excel",
            data=output.getvalue(),
            file_name="school_submission_dashboard.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
else:
    st.info("Please upload both files to generate the dashboard.")
