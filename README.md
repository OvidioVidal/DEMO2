# PE Fund Classifier Demo

An interactive Streamlit demo for classifying Private Equity funds using AI-powered analysis.

## Features

- 🔍 **Single Fund Analysis** - Analyze individual fund names with detailed breakdown
- 📁 **Batch Processing** - Upload Excel files with flexible column selection for bulk classification
- 🎯 **Sample Data Demo** - Pre-loaded examples to showcase capabilities
- 📊 **Visual Analytics** - Interactive charts and confidence gauges
- 📥 **Export Results** - Download classification results as CSV

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Upload all files from this folder to the repository

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Share with Client:**
   - Get the public URL from Streamlit Cloud
   - Share with your client for the demo

## File Structure

```
streamlit_demo/
├── app.py                    # Main Streamlit application
├── classifier.py             # PE Fund classifier logic
├── requirements.txt          # Python dependencies
├── testing_results.xlsx      # Training data
├── preqin_pe_funds.xlsx     # Sample input data
└── README.md                # This file
```

## Demo Instructions for Client

### Single Fund Analysis
1. Select "Single Fund Analysis" from the sidebar
2. Enter a fund name or click example buttons
3. Click "🚀 Analyze Fund"
4. View detailed classification results and confidence scores

### Batch Processing
1. Select "Batch File Processing" from the sidebar
2. Download sample Excel files or upload your own Excel file
3. Select which column contains the fund names from the dropdown
4. Preview the selected data and click "🚀 Process All Funds"
5. View summary statistics and download results

### Sample Data Demo
1. Select "Sample Data Demo" from the sidebar
2. Click "🚀 Run Sample Analysis"
3. See pre-loaded examples being classified in real-time

## Technical Notes

- **Training Data**: Uses machine learning on historical PE fund data
- **Multilingual Support**: Recognizes PE terms in English, Spanish, German, French, and Dutch
- **Pattern Matching**: Identifies fund naming patterns and structures
- **Confidence Scoring**: Provides reliability metrics for each classification

## Support

For technical support or questions about the classifier, contact the development team. 