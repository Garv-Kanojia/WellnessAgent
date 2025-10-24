import streamlit as st
from codee2 import Prompts

# Set page config for wide layout and groovy title
st.set_page_config(page_title="Wellness Companion", layout="wide", page_icon="🌟")

# Custom CSS for modern, stylish, groovy design
# Color theme: Dark black background with softer gold and purple accents
st.markdown("""
    <style>
    /* Global styles */
    body {
        background: #0F0F0F;
        font-family: 'Poppins', sans-serif;
        color: #E8E8E8;
    }
    .stApp {
        background: #0F0F0F;
    }
    /* Hide Streamlit header and menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Title styling - increased specificity */
    .stApp h1, h1 {
        font-size: 3em !important;
        color: #D4AF37 !important;
        text-shadow: 2px 2px 8px rgba(212, 175, 55, 0.3) !important;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Headers for plans - increased specificity */
    .stApp h2, h2, .stMarkdown h2, div[data-testid="stMarkdownContainer"] h2 {
        color: #D4AF37 !important;
        font-size: 1.8em !important;
        border-bottom: 2px solid #D4AF37 !important;
        padding-bottom: 10px !important;
        margin-bottom: 15px !important;
    }
    /* Text area styling */
    .stTextArea textarea {
        background-color: #1C1C1C;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        color: #E8E8E8;
    }
    .stTextArea textarea::placeholder {
        color: #A0A0A0;
        opacity: 1;
    }
    .stTextArea label {
        color: #D4AF37 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 10px !important;
    }
    /* Button styling - groovy and vibrant */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37, #C19A6B);
        color: #0F0F0F;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 12px 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(212, 175, 55, 0.4);
        margin-top: 20px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 10px rgba(193, 154, 107, 0.6);
        background: linear-gradient(135deg, #C19A6B, #D4AF37);
    }
    /* Columns for side-by-side display */
    .css-1y4p8pa {
        padding: 20px;
        background-color: #1C1C1C;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        margin: 10px;
    }
    /* Markdown content */
    .stMarkdown {
        font-size: 15px;
        line-height: 1.6;
        color: #E8E8E8;
    }
    /* Warning message */
    .stAlert {
        background-color: #2C2C2C;
        border-left: 5px solid #BB86FC;
        padding: 15px;
        border-radius: 10px;
        color: #E8E8E8;
    }
    
    /* Spinner animation */
    .spinner {
        border: 4px solid #2C2C2C;
        border-top: 4px solid #D4AF37;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        display: inline-block;
        vertical-align: middle;
        margin-left: 15px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .button-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App title with groovy emoji
st.title("🍴✨ Wellness Companion ✨💪")

# Input for health goal
user_prompt = st.text_area("Share your health, fitness, or nutrition goal here:", height=150, placeholder="E.g., 'Lose 10 pounds in 2 months with a vegetarian diet and home workouts.'")

# Initialize session state for loading
if 'is_loading' not in st.session_state:
    st.session_state['is_loading'] = False

# Create a centered container for button and spinner
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# Create columns with better ratio for centering
col_left, col_btn, col_spinner, col_right = st.columns([2, 1.5, 0.5, 2])

with col_btn:
    button_clicked = st.button("Generate Your Plan")

with col_spinner:
    if st.session_state['is_loading']:
        st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Process button click
if button_clicked:
    if user_prompt:
        # Set loading state
        st.session_state['is_loading'] = True
        
        # Clear previous result from session state to "clear history"
        if 'result' in st.session_state:
            del st.session_state['result']
        
        # Force rerun to show spinner
        st.rerun()

# Generate result if loading
if st.session_state.get('is_loading', False):
    # Create Prompts object and get response
    agent = Prompts(user_prompt)
    result = agent.response()
    
    # Store new result in session state
    st.session_state['result'] = result
    
    # Stop loading
    st.session_state['is_loading'] = False
    
    # Rerun to hide spinner and show results
    st.rerun()

# Show warning if button clicked without input
if button_clicked and not user_prompt:
    st.warning("Oops! Please enter a goal to get started. 🚀")

# Display plans side by side if result exists
if 'result' in st.session_state:
    result = st.session_state['result']
    
    # Check for error in result
    if "error" in result:
        st.error(result["error"])
    else:
        # Use columns for side-by-side display
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("🍎 Nutrition Plan")
            st.markdown(result["NutritionPlan"])
        
        with col2:
            st.header("🏋️ Fitness Plan")
            st.markdown(result["FitnessPlan"])