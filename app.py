import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from classifier import EnhancedPEFundClassifier, FundClassificationResult
import io

# Page configuration
st.set_page_config(
    page_title="PE Fund Classifier Demo",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.success { border-left: 5px solid #28a745; }
.warning { border-left: 5px solid #ffc107; }
.danger { border-left: 5px solid #dc3545; }
.info { border-left: 5px solid #17a2b8; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🏦 Private Equity Fund Classifier")
    st.markdown("**AI-powered classification of investment funds**")
    
    # Sidebar
    st.sidebar.header("📋 Demo Options")
    
    demo_mode = st.sidebar.selectbox(
        "Choose Demo Mode:",
        ["Single Fund Analysis", "Batch File Processing", "Sample Data Demo"]
    )
    
    # Initialize classifier
    @st.cache_resource
    def load_classifier():
        return EnhancedPEFundClassifier()
    
    classifier = load_classifier()
    
    if demo_mode == "Single Fund Analysis":
        single_fund_demo(classifier)
    elif demo_mode == "Batch File Processing":
        batch_processing_demo(classifier)
    else:
        sample_data_demo(classifier)

def single_fund_demo(classifier):
    st.header("🔍 Single Fund Analysis")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fund_name = st.text_input(
            "Enter Fund Name:",
            placeholder="e.g., Apollo Global Management Fund VII",
            help="Enter the name of the fund you want to classify"
        )
        
        if st.button("🚀 Analyze Fund", type="primary"):
            if fund_name:
                analyze_single_fund(classifier, fund_name)
            else:
                st.warning("Please enter a fund name to analyze.")
    
    with col2:
        st.markdown("### 📖 Examples")
        example_funds = [
            "KKR North America Fund XIII",
            "Blackstone Capital Partners VII",
            "Deutsche Bank AG",
            "Apple Venture Fund II",
            "Restaurant Holdings LLC"
        ]
        
        for fund in example_funds:
            if st.button(f"Try: {fund}", key=fund):
                analyze_single_fund(classifier, fund)

def analyze_single_fund(classifier, fund_name):
    with st.spinner("Analyzing fund..."):
        result = classifier.classify_fund(fund_name)
    
    # Results display
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        classification_color = {
            'definite_pe': '🟢',
            'likely_pe': '🟡', 
            'uncertain': '🟠',
            'not_pe': '🔴'
        }
        st.metric(
            "Classification",
            f"{classification_color.get(result.classification, '⚪')} {result.classification.replace('_', ' ').title()}"
        )
    
    with col2:
        st.metric("Confidence", f"{result.confidence:.1%}")
    
    with col3:
        st.metric("Score", f"{result.score:.2f}")
    
    with col4:
        st.metric("Fund Type", result.fund_type.replace('_', ' ').title())
    
    # Detailed breakdown
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("🔍 Classification Reasons")
        for i, reason in enumerate(result.reasons, 1):
            st.write(f"{i}. {reason}")
    
    with col2:
        # Confidence gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = result.confidence * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence %"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

def batch_processing_demo(classifier):
    st.header("📁 Batch File Processing")
    
    st.markdown("""
    Upload an Excel file with fund names to classify multiple funds at once.
    You can specify which column contains the fund names.
    """)
    
    # Sample files section
    with st.expander("📥 Download Sample Excel Files"):
        st.markdown("**Try these sample files to test the functionality:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Sample 1: 'NAME' column**")
            with open('sample_funds.xlsx', 'rb') as f:
                st.download_button(
                    label="📄 Download sample_funds.xlsx",
                    data=f.read(),
                    file_name="sample_funds.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            st.markdown("**Sample 2: 'Company Name' column**")
            with open('sample_company_names.xlsx', 'rb') as f:
                st.download_button(
                    label="📄 Download sample_company_names.xlsx",
                    data=f.read(),
                    file_name="sample_company_names.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            st.markdown("**Sample 3: 'Fund' column**")
            with open('sample_fund_names.xlsx', 'rb') as f:
                st.download_button(
                    label="📄 Download sample_fund_names.xlsx",
                    data=f.read(),
                    file_name="sample_fund_names.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload an Excel file with fund names"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! Found {len(df)} rows and {len(df.columns)} columns.")
            
            # Show preview
            with st.expander("📋 Data Preview"):
                st.dataframe(df.head(10))
            
            # Column selection
            st.subheader("📊 Column Selection")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                column_name = st.selectbox(
                    "Select the column that contains fund names:",
                    options=df.columns.tolist(),
                    help="Choose the column header that contains the fund names you want to classify"
                )
            
            with col2:
                st.markdown("**Available Columns:**")
                for col in df.columns:
                    st.write(f"• {col}")
            
            # Show sample data from selected column
            if column_name:
                st.markdown(f"**Sample data from '{column_name}' column:**")
                sample_data = df[column_name].dropna().head(5).tolist()
                for i, sample in enumerate(sample_data, 1):
                    st.write(f"{i}. {sample}")
                
                # Validation
                non_null_count = df[column_name].notna().sum()
                st.info(f"Found {non_null_count} non-empty entries in '{column_name}' column")
                
                if st.button("🚀 Process All Funds", type="primary"):
                    if non_null_count > 0:
                        process_batch_funds(classifier, df, column_name)
                    else:
                        st.error("❌ The selected column has no valid fund names to process.")
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

def process_batch_funds(classifier, df, column_name):
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    fund_names = df[column_name].dropna()
    total_funds = len(fund_names)
    
    for idx, fund_name in enumerate(fund_names):
        # Update progress
        progress = (idx + 1) / total_funds
        progress_bar.progress(progress)
        status_text.text(f"Processing fund {idx + 1}/{total_funds}: {str(fund_name)[:50]}...")
        
        # Classify fund
        result = classifier.classify_fund(str(fund_name))
        results.append({
            'Fund Name': result.fund_name,
            'Classification': result.classification,
            'Confidence': f"{result.confidence:.1%}",
            'Score': round(result.score, 2),
            'Fund Type': result.fund_type,
            'Reasons': '; '.join(result.reasons)
        })
    
    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Display results
    st.success("✅ Processing complete!")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    classification_counts = results_df['Classification'].value_counts()
    total_pe = classification_counts.get('definite_pe', 0) + classification_counts.get('likely_pe', 0)
    pe_rate = (total_pe / len(results_df)) * 100
    
    with col1:
        st.metric("Total Funds", len(results_df))
    with col2:
        st.metric("PE Funds Identified", total_pe)
    with col3:
        st.metric("PE Success Rate", f"{pe_rate:.1f}%")
    
    # Classification breakdown
    st.subheader("📊 Classification Breakdown")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Pie chart
        fig = px.pie(
            values=classification_counts.values,
            names=classification_counts.index,
            title="Classification Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart
        fig = px.bar(
            x=classification_counts.index,
            y=classification_counts.values,
            title="Classification Counts",
            labels={'x': 'Classification', 'y': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Results table
    st.subheader("📋 Detailed Results")
    st.dataframe(results_df, use_container_width=True)
    
    # Download button
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="pe_fund_classification_results.csv",
        mime="text/csv"
    )

def sample_data_demo(classifier):
    st.header("🎯 Sample Data Demo")
    
    st.markdown("See the classifier in action with pre-loaded sample data:")
    
    sample_funds = [
        "Apollo Global Management Fund VIII",
        "KKR North America Fund XIV", 
        "Blackstone Capital Partners VIII",
        "Deutsche Bank Investment Division",
        "McDonald's Restaurant Holdings",
        "Sequoia Capital Growth Fund III",
        "Berkshire Hathaway Energy Partners",
        "Goldman Sachs Private Capital",
        "JPMorgan Chase Commercial Bank",
        "Vista Equity Partners Fund VII"
    ]
    
    if st.button("🚀 Run Sample Analysis", type="primary"):
        results = []
        progress_bar = st.progress(0)
        
        for idx, fund_name in enumerate(sample_funds):
            progress_bar.progress((idx + 1) / len(sample_funds))
            result = classifier.classify_fund(fund_name)
            results.append(result)
        
        # Display results
        results_data = []
        for result in results:
            results_data.append({
                'Fund Name': result.fund_name,
                'Classification': result.classification,
                'Confidence': f"{result.confidence:.1%}",
                'Score': round(result.score, 2),
                'Fund Type': result.fund_type
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True)
        
        # Summary
        classification_counts = results_df['Classification'].value_counts()
        total_pe = classification_counts.get('definite_pe', 0) + classification_counts.get('likely_pe', 0)
        
        st.success(f"✅ Identified {total_pe} out of {len(sample_funds)} funds as PE funds!")

if __name__ == "__main__":
    main() 