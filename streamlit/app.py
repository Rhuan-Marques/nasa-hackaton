import streamlit as st
from data_loading import load_data
from visualization import plot_data
from inference import make_inferences

def main():
    st.title("Data Analysis App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.write("Data Loaded:")
            st.write(df)

            # Display column names for debugging
            st.write("Column Names:", df.columns)

            # Verify expected columns if needed
            expected_columns = [
                "Source Name", "Sample Name", "Characteristics[Organism]",
                "Characteristics[Strain]", "Characteristics[Sex]",
                "Characteristics[Material Type]", "Factor Value[Spaceflight]",
                "Factor Value[Duration]", "Factor Value[Age]",
                "Protocol REF", "Parameter Value[Light Cycle]",
                "Parameter Value[Diet]", "Parameter Value[Sample Storage Temperature]"
            ]
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                st.warning(f"Missing columns: {missing_columns}")

            # Plot data
            plot_data(df)

            # Make inferences
            make_inferences(df)

if __name__ == "__main__":
    main()
