"""Streamlit web application for phishing URL classification."""

import streamlit as st
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from predict import predict_url, load_model


# Page configuration
st.set_page_config(
    page_title="Phishing URL Classifier",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .phishing-result {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .legitimate-result {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🔒 Phishing URL Classifier</div>', unsafe_allow_html=True)
st.markdown("""
This AI-powered tool analyzes URLs to detect potential phishing attempts.
Simply paste a URL below to check if it's safe or suspicious.
""")

# Load model (cached)
@st.cache_resource
def get_model():
    """Load and cache the trained model."""
    try:
        model_path = os.path.join('models', 'phishing_model.joblib')
        return load_model(model_path)
    except FileNotFoundError:
        return None

model = get_model()

# Check if model exists
if model is None:
    st.error("⚠️ Model not found! Please train the model first by running:")
    st.code("python src/train_model.py", language="bash")
    st.stop()

# Input section
st.markdown("---")
st.subheader("Enter URL to Analyze")

url_input = st.text_input(
    "URL",
    placeholder="https://example.com",
    help="Enter the full URL including http:// or https://"
)

# Analyze button
if st.button("🔍 Analyze URL", type="primary", use_container_width=True):
    if not url_input:
        st.warning("Please enter a URL to analyze.")
    else:
        with st.spinner("Analyzing URL..."):
            try:
                # Make prediction
                result = predict_url(url_input, model=model)
                
                # Display results
                st.markdown("---")
                st.subheader("Analysis Results")
                
                # Show URL being analyzed
                st.text(f"URL: {result['url']}")
                
                # Display prediction with styling
                if result['prediction'] == 'Phishing':
                    st.markdown(f"""
                        <div class="phishing-result">
                            <h3>⚠️ PHISHING DETECTED</h3>
                            <p>This URL appears to be a <strong>phishing attempt</strong>.</p>
                            <p><strong>Confidence:</strong> {result['confidence']:.1%}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.error("🚨 Do not enter personal information on this site!")
                else:
                    st.markdown(f"""
                        <div class="legitimate-result">
                            <h3>✓ LEGITIMATE</h3>
                            <p>This URL appears to be <strong>legitimate</strong>.</p>
                            <p><strong>Confidence:</strong> {result['confidence']:.1%}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success("✓ This URL appears safe, but always exercise caution online.")
                
                # Show probability breakdown
                st.markdown("### Probability Breakdown")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Legitimate",
                        f"{result['probabilities']['legitimate']:.1%}",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Phishing",
                        f"{result['probabilities']['phishing']:.1%}",
                        delta=None
                    )
                
                # Progress bars for visual representation
                st.markdown("### Visual Confidence")
                st.progress(result['probabilities']['legitimate'], text="Legitimate")
                st.progress(result['probabilities']['phishing'], text="Phishing")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

# Sidebar with information
st.sidebar.title("About")
st.sidebar.info("""
**Phishing URL Classifier**

This tool uses machine learning to detect phishing URLs based on:
- URL structure and length
- Domain characteristics
- Special character patterns
- Known suspicious indicators

**How it works:**
1. Extracts features from the URL
2. Analyzes patterns using trained ML model
3. Provides prediction with confidence score

**Note:** This is an educational project. Always verify URLs through multiple sources.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Example URLs to Test")
st.sidebar.code("https://www.google.com", language="text")
st.sidebar.code("http://192.168.1.1/login", language="text")
st.sidebar.code("http://bit.ly/suspicious", language="text")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Built with Python, scikit-learn, and Streamlit</p>
    <p>⚠️ Educational purposes only. Always verify URLs independently.</p>
</div>
""", unsafe_allow_html=True)
