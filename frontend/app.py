import streamlit as st
import time

# Minimal page configuration
st.set_page_config(
    page_title="Mike - Research Assistant",
    page_icon="•",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS styling with taller input box
st.markdown("""
<style>
    .main {padding: 0.5rem !important;}
    .stChatInput {bottom: 5rem !important; width: 90% !important; left: 5% !important;}
    .stChatMessage {padding: 8px 12px !important; border-radius: 12px !important;}
    [data-testid="stVerticalBlock"] {gap: 0.1rem !important;}
    .stMarkdown p {margin: 0.1em 0 !important; font-size: 0.95rem !important;}
    header {visibility: hidden; height: 0 !important;}
    footer {visibility: hidden;}
    .stTextInput textarea {min-height: 100px !important; padding: 12px !important; font-size: 0.9rem !important;}
    [data-testid="stAppViewContainer"] {background-color: #fafafa;}
    .compact-radio {padding: 0 !important; margin: 0 !important;}
    .compact-radio .stRadio > div {flex-direction: row !important; gap: 1rem;}
    .tab-button {padding: 0.3rem 0.8rem !important; font-size: 0.8rem !important;}
    .chat-container {margin-bottom: 6rem !important;}
</style>
""", unsafe_allow_html=True)

# App state
if "mode" not in st.session_state:
    st.session_state.mode = "assistant"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "papers" not in st.session_state:
    st.session_state.papers = []

# Compact header with mode toggle
col1, col2 = st.columns([3,1])
with col1:
    st.markdown("""
    <div style='margin-bottom: 0.5rem;'>
        <h3 style='margin: 0;'>Hi, I'm Mike</h3>
        <p style='color: #666; margin: 0; font-size: 0.9rem;'>Academic Research Assistant</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Compact mode selector
    st.session_state.mode = st.radio(
        "Mode",
        ["Assistant", "Papers"],
        index=0 if st.session_state.mode == "assistant" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="mode_selector"
    )

# Main content area
if st.session_state.mode == "Assistant":
    # Chat interface in a container with bottom margin
    with st.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a research question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner(""):
                time.sleep(0.8)
                response = f"""I've analyzed your question about "{prompt}". Here's what I found:
                
- **Key Paper**: "Recent Advances in the Field" (2023) by Smith et al.
- **Trends**: Growing interest in this area with 32% more papers last year
- **Recommendation**: You should review these 3 foundational papers first"""
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:  # Paper Search mode
    # Compact search interface
    search_query = st.text_input(
        "Search papers",
        placeholder="Keywords, title, or author",
        key="paper_search"
    )
    
    # Minimal filters
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Year", ["All", "Last 5 years", "2020s", "2010s"], index=1)
    with col2:
        discipline = st.selectbox("Field", ["All", "CS", "Biology", "Physics", "Social Sciences"], index=0)
    
    if st.button("Search", type="primary"):
        with st.spinner("Finding relevant papers..."):
            time.sleep(1)
            st.session_state.papers = [
                {
                    "title": "Deep Learning Approaches to NLP",
                    "authors": "Smith, Johnson, Lee",
                    "year": 2023,
                    "abstract": "Novel architecture achieving state-of-the-art results..."
                },
                {
                    "title": "Quantum Computing Breakthroughs",
                    "authors": "Chen, Wang",
                    "year": 2022,
                    "abstract": "New method reduces error rates significantly..."
                }
            ]
    
    # Paper results
    if st.session_state.papers:
        st.markdown("**Search Results**")
        for i, paper in enumerate(st.session_state.papers):
            with st.expander(f"{paper['title']} ({paper['year']})"):
                st.caption(f"Authors: {paper['authors']}")
                st.write(paper['abstract'])
                st.button("Cite", key=f"cite_{i}")
                st.button("Save", key=f"save_{i}")