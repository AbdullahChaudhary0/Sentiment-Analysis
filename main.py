import streamlit as st
import google.generativeai as genai
import re

# Configure Gemini API
def configure_genai(api_key):
    genai.configure(api_key=api_key)

# Function to get Gemini response
def get_sentiment_analysis(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(f"""
    Analyze the sentiment of this text and identify specific words that contribute to the sentiment.
    Return the response in this exact format:
    Sentiment: [Positive/Negative/Neutral]
    Positive Words: [comma-separated list or None]
    Negative Words: [comma-separated list or None]
    
    Text: {prompt}
    """)
    return response.text

# Function to parse Gemini response
def parse_response(response):
    sentiment = re.search(r"Sentiment: (.*)", response).group(1)
    positive_words = re.search(r"Positive Words: (.*)", response)
    negative_words = re.search(r"Negative Words: (.*)", response)
    
    pos_words = positive_words.group(1).split(', ') if positive_words and positive_words.group(1) != 'None' else []
    neg_words = negative_words.group(1).split(', ') if negative_words and negative_words.group(1) != 'None' else []
    
    return sentiment, pos_words, neg_words

# Function to highlight words in text
def highlight_words(text, pos_words, neg_words):
    words = text.split()
    highlighted = []
    for word in words:
        clean_word = word.strip('.,?!').lower()
        if clean_word in [w.lower() for w in pos_words]:
            highlighted.append(f'<span style="color: #00FF00; font-weight: bold;">{word}</span>')
        elif clean_word in [w.lower() for w in neg_words]:
            highlighted.append(f'<span style="color: #FF0000; font-weight: bold;">{word}</span>')
        else:
            highlighted.append(word)
    return ' '.join(highlighted)

# Streamlit UI
st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

# Initial welcome screen
if 'show_main' not in st.session_state:
    st.title("🎉 Welcome to Sentiment Checker! 🎉")
    st.markdown("<div style='height: 200px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Get Started", key="start_button"):
            st.session_state.show_main = True
    st.markdown("<div style='height: 200px'></div>", unsafe_allow_html=True)
    st.stop()

# Main application
st.title("📝 Sentiment Analysis with Gemini")
st.markdown("---")

# API Key Input
api_key = st.text_input("🔑 Enter your Gemini API Key:", type="password")

if api_key:
    configure_genai(api_key)
    
    # Text input
    user_input = st.text_area("✍️ Enter your text here:", height=150)
    submit_button = st.button("🔍 Analyze Sentiment", disabled=not bool(user_input.strip()))

    if submit_button and user_input.strip():
        with st.spinner("🔮 Analyzing sentiment..."):
            try:
                # Get analysis from Gemini
                analysis = get_sentiment_analysis(user_input)
                sentiment, pos_words, neg_words = parse_response(analysis)
                
                # Display results
                st.markdown("---")
                emoji = "😊" if "Positive" in sentiment else "😢" if "Negative" in sentiment else "😐"
                st.subheader(f"{emoji} Sentiment: {sentiment}")
                
                # Highlighted text
                highlighted_text = highlight_words(user_input, pos_words, neg_words)
                st.markdown(f"""
                <div style="background-color: #2E2E2E; padding: 20px; border-radius: 10px; color: white;">
                    {highlighted_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Additional information
                with st.expander("📊 Analysis Details"):
                    st.write(f"**Original Text:**\n{user_input}")
                    st.write(f"**Detected Sentiment:** {sentiment}")
                    if pos_words:
                        st.write(f"🌈 **Positive Indicators:** {', '.join(pos_words)}")
                    if neg_words:
                        st.write(f"⛈️ **Negative Indicators:** {', '.join(neg_words)}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Add some styling
st.markdown("""
<style>
    .stTextArea textarea {
        color: white !important;
    }
    .st-bb {
        background-color: transparent;
    }
    .st-at {
        background-color: #0E1117;
    }
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)