import streamlit as st
from wiki_utils import (
    get_wikipedia_search_results,
    get_article_content,
    get_available_languages,
    get_article_in_language,
    translate_text,
    get_language_name,
    LANGUAGE_DICT
)

# Page configuration
st.set_page_config(
    page_title="TruePedia - Multilingual Wikipedia Search",
    page_icon="📚",
    layout="wide"
)

# CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .article-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1565C0;
        margin-bottom: 1rem;
    }
    .article-summary {
        font-size: 1.1rem;
        color: #424242;
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .lang-button {
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .article-content {
        font-size: 1rem;
        line-height: 1.5;
    }
    .wiki-link {
        color: #1565C0;
        text-decoration: none;
    }
    .wiki-link:hover {
        text-decoration: underline;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #757575;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'current_article' not in st.session_state:
    st.session_state.current_article = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'available_languages' not in st.session_state:
    st.session_state.available_languages = {}
if 'current_language' not in st.session_state:
    st.session_state.current_language = 'en'
if 'translate_to' not in st.session_state:
    st.session_state.translate_to = None
if 'show_translation' not in st.session_state:
    st.session_state.show_translation = False

# Title and description
st.markdown('<div class="main-header">TruePedia</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Multilingual Wikipedia Search & Translation</div>', unsafe_allow_html=True)

# Sidebar for search and settings
with st.sidebar:
    st.subheader("Search Wikipedia")
    
    # Language selection for search
    search_lang = st.selectbox(
        "Search Language", 
        options=list(LANGUAGE_DICT.keys()),
        format_func=lambda x: f"{get_language_name(x)} ({x})"
    )
    
    # Search box
    search_query = st.text_input("Enter your search query", key="search_box")
    
    if st.button("Search"):
        if search_query:
            with st.spinner(f"Searching Wikipedia in {get_language_name(search_lang)}..."):
                st.session_state.search_results = get_wikipedia_search_results(search_query, search_lang)
                st.session_state.current_article = None
                st.session_state.available_languages = {}
                st.session_state.current_language = search_lang
                st.session_state.show_translation = False
    
    # Show search results if available
    if st.session_state.search_results:
        st.subheader("Search Results")
        for idx, result in enumerate(st.session_state.search_results):
            if st.button(f"{result}", key=f"result_{idx}"):
                with st.spinner(f"Loading article: {result}..."):
                    st.session_state.current_article = get_article_content(result, st.session_state.current_language)
                    if st.session_state.current_article:
                        st.session_state.available_languages = get_available_languages(
                            result, 
                            st.session_state.current_language
                        )
                        st.session_state.show_translation = False
    
    # Translation settings
    if st.session_state.current_article:
        st.subheader("Translation")
        st.session_state.translate_to = st.selectbox(
            "Translate To",
            options=list(LANGUAGE_DICT.keys()),
            format_func=lambda x: f"{get_language_name(x)} ({x})",
            key="translate_lang"
        )
        
        if st.button("Translate Article"):
            st.session_state.show_translation = True
    
    st.markdown("""
    <div class="footer">
        TruePedia uses Wikipedia API and free translation libraries<br>
        💡 Search in any language and explore articles across languages
    </div>
    """, unsafe_allow_html=True)

# Main content area
if st.session_state.current_article:
    article = st.session_state.current_article
    
    # Display article title and summary
    st.markdown(f'<div class="article-title">{article["title"]}</div>', unsafe_allow_html=True)
    
    # Display Wikipedia link
    st.markdown(f'<a href="{article["url"]}" target="_blank" class="wiki-link">📖 View on Wikipedia</a>', unsafe_allow_html=True)
    
    # Display language options
    st.subheader("Available Languages")
    
    # Create columns for language buttons
    cols = st.columns(4)
    
    # Sort languages by name for better organization
    sorted_langs = sorted(
        st.session_state.available_languages.items(), 
        key=lambda x: get_language_name(x[0])
    )
    
    for idx, (lang_code, lang_title) in enumerate(sorted_langs):
        col_idx = idx % 4
        with cols[col_idx]:
            if st.button(
                f"{get_language_name(lang_code)} ({lang_code})",
                key=f"lang_{lang_code}",
                use_container_width=True
            ):
                with st.spinner(f"Loading article in {get_language_name(lang_code)}..."):
                    st.session_state.current_article = get_article_in_language(lang_title, lang_code)
                    st.session_state.current_language = lang_code
                    st.session_state.show_translation = False
                    st.experimental_rerun()
    
    # Create tabs for summary and full content
    summary_tab, content_tab = st.tabs(["Summary", "Full Content"])
    
    with summary_tab:
        # If translation is requested, show translated summary
        if st.session_state.show_translation and st.session_state.translate_to != st.session_state.current_language:
            with st.spinner(f"Translating summary to {get_language_name(st.session_state.translate_to)}..."):
                translated_summary = translate_text(
                    article["summary"],
                    st.session_state.translate_to,
                    st.session_state.current_language
                )
                st.markdown(f'<div class="article-summary">{translated_summary}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="article-summary">{article["summary"]}</div>', unsafe_allow_html=True)
    
    with content_tab:
        # If translation is requested, show translated content
        if st.session_state.show_translation and st.session_state.translate_to != st.session_state.current_language:
            with st.spinner(f"Translating content to {get_language_name(st.session_state.translate_to)}..."):
                # Only translate a portion of the content to avoid rate limits
                content_preview = article["content"][:3000] + "..." if len(article["content"]) > 3000 else article["content"]
                translated_content = translate_text(
                    content_preview,
                    st.session_state.translate_to,
                    st.session_state.current_language
                )
                st.markdown(f'<div class="article-content">{translated_content}</div>', unsafe_allow_html=True)
                if len(article["content"]) > 3000:
                    st.info("Only a portion of the content has been translated due to length limitations.")
        else:
            st.markdown(f'<div class="article-content">{article["content"]}</div>', unsafe_allow_html=True)
else:
    # Welcome message when no article is selected
    st.info("👈 Search for a Wikipedia article in any language to get started!")
    
    # Brief instructions
    st.markdown("""
    ### How to use TruePedia:
    
    1. 🔍 **Search**: Enter a query and select your preferred language
    2. 📝 **Select**: Choose an article from the search results
    3. 🌐 **Explore**: View the article in different languages
    4. 🔄 **Translate**: Translate the article content to your preferred language
    
    TruePedia gives you access to Wikipedia content across multiple languages and provides translation capabilities to help you understand content in different languages.
    """)
