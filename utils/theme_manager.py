import streamlit as st

def initialize_theme():
    """Initialize theme state"""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True  # Default to dark mode

def toggle_theme():
    """Toggle between dark and light theme"""
    st.session_state.dark_mode = not st.session_state.dark_mode

def get_theme_colors():
    """Get theme-specific colors"""
    if st.session_state.dark_mode:
        return {
            'primary_bg': '#0F1419',
            'secondary_bg': '#1A202C',
            'card_bg': 'rgba(26, 32, 44, 0.8)',
            'form_bg': 'rgba(45, 55, 72, 0.8)',
            'text_color': '#E2E8F0',
            'border_color': 'rgba(255, 255, 255, 0.1)',
            'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #F093FB 100%)',
            'input_bg': 'rgba(45, 55, 72, 0.9)',
            'input_border': 'rgba(255, 255, 255, 0.2)',
            'secondary_text': '#A0AEC0',
            'label_color': '#CBD5E0'
        }
    else:
        return {
            'primary_bg': '#FFFFFF',
            'secondary_bg': '#F8FAFC',
            'card_bg': 'rgba(255, 255, 255, 0.95)',
            'form_bg': 'rgba(248, 250, 252, 0.95)',
            'text_color': '#1A202C',
            'border_color': 'rgba(0, 0, 0, 0.15)',
            'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #F093FB 100%)',
            'input_bg': '#FFFFFF',
            'input_border': 'rgba(0, 0, 0, 0.25)',
            'secondary_text': '#4A5568',
            'label_color': '#2D3748'
        }

def render_theme_toggle():
    """Render theme toggle button"""
    colors = get_theme_colors()
    
    # Create a container for the toggle button in the top right
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col3:
        theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
        theme_text = "Light" if st.session_state.dark_mode else "Dark"
        
        if st.button(f"{theme_icon} {theme_text}", key="theme_toggle", help="Toggle theme"):
            toggle_theme()
            st.rerun()

def get_dynamic_css():
    """Generate dynamic CSS based on current theme"""
    colors = get_theme_colors()
    
    return f"""
    <style>
    /* Dynamic Theme CSS */
    .stApp {{
        background: {'linear-gradient(135deg, #0F1419 0%, #1A202C 50%, #2D3748 100%)' if st.session_state.dark_mode else 'linear-gradient(135deg, #FFFFFF 0%, #F7FAFC 50%, #EDF2F7 100%)'};
        color: {colors['text_color']};
    }}
    
    /* Main content background */
    .main > div {{
        background: transparent;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: {'linear-gradient(180deg, #1A202C 0%, #2D3748 100%)' if st.session_state.dark_mode else 'linear-gradient(180deg, #F7FAFC 0%, #EDF2F7 100%)'};
        border-right: 1px solid {colors['border_color']};
    }}
    
    /* Tab content */
    .tab-content {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Form containers */
    .form-container {{
        background: {colors['form_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Results containers */
    .results-container {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Insights container */
    .insights-container {{
        background: {colors['form_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Metric cards */
    .metric-card {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Input styling */
    .stSelectbox > div > div {{
        background: {colors['input_bg']} !important;
        border: 1px solid {colors['input_border']} !important;
        color: {colors['text_color']} !important;
        box-shadow: {'0 2px 8px rgba(0, 0, 0, 0.1)' if not st.session_state.dark_mode else '0 2px 8px rgba(0, 0, 0, 0.3)'} !important;
    }}
    
    .stSelectbox > div > div > div {{
        color: {colors['text_color']} !important;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        color: {colors['text_color']} !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        color: {colors['text_color']} !important;
    }}
    
    .stTextInput > div > div > input {{
        background: {colors['input_bg']} !important;
        border: 1px solid {colors['input_border']} !important;
        color: {colors['text_color']} !important;
        box-shadow: {'0 2px 8px rgba(0, 0, 0, 0.1)' if not st.session_state.dark_mode else '0 2px 8px rgba(0, 0, 0, 0.3)'} !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: {colors['gradient']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* Labels and text styling */
    .stSelectbox label, .stTextInput label, .stSlider label, .stRadio label {{
        color: {colors['label_color']} !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}
    
    /* Form section headers */
    .stMarkdown h4 {{
        color: {colors['text_color']} !important;
        border-bottom: 2px solid #667eea !important;
        padding-bottom: 0.5rem !important;
    }}
    
    /* Slider styling - Fixed for both themes */
    .stSlider > div > div > div > div {{
        background: {colors['input_bg']} !important;
    }}
    
    .stSlider > div > div > div > div > div {{
        background: {colors['gradient']} !important;
    }}
    
    .stSlider > div > div > div > div > div > div {{
        background: white !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        background: {colors['form_bg']};
        border: 1px solid {colors['border_color']};
    }}
    
    /* Checkboxes */
    .stCheckbox > div {{
        background: {colors['form_bg']};
        border: 1px solid {colors['border_color']};
    }}
    
    /* Dataframes */
    .stDataFrame {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Expanders */
    .stExpander {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    /* Alerts */
    .stAlert {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border_color']};
        backdrop-filter: blur(10px);
    }}
    
    .stAlert > div {{
        color: {colors['text_color']};
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        background: {colors['secondary_bg']};
        border: 1px solid {colors['border_color']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {'#A0AEC0' if st.session_state.dark_mode else '#4A5568'};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {colors['gradient']};
        color: white;
    }}
    
    /* Theme toggle button styling */
    .theme-toggle-container {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
    }}
    
    /* Progress bar */
    .stProgress > div > div {{
        background: {colors['gradient']};
    }}
    
    /* Dropdown menu styling */
    .stSelectbox ul {{
        background: {colors['input_bg']} !important;
        border: 1px solid {colors['input_border']} !important;
        color: {colors['text_color']} !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }}
    
    .stSelectbox ul li {{
        color: {colors['text_color']} !important;
        background: {colors['input_bg']} !important;
    }}
    
    .stSelectbox ul li:hover {{
        background: {'rgba(102, 126, 234, 0.1)' if not st.session_state.dark_mode else 'rgba(102, 126, 234, 0.2)'} !important;
        color: {colors['text_color']} !important;
    }}
    
    /* Radio button styling */
    .stRadio > div > label {{
        color: {colors['text_color']} !important;
    }}
    
    .stRadio > div > label > div {{
        color: {colors['text_color']} !important;
    }}
    
    /* Markdown text styling */
    .stMarkdown p {{
        color: {colors['text_color']} !important;
    }}
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: {colors['text_color']} !important;
    }}
    
    /* Sidebar text styling */
    .css-1d391kg .stMarkdown p {{
        color: {colors['text_color']} !important;
    }}
    
    /* Ensure all text is readable */
    .stApp * {{
        color: {colors['text_color']} !important;
    }}
    
    /* Override specific elements that need different colors */
    .stButton > button, .stButton > button * {{
        color: white !important;
    }}
    
    .metric-value {{
        color: {colors['text_color']} !important;
    }}
    
    .metric-label {{
        color: {colors['secondary_text']} !important;
    }}
    </style>
    """