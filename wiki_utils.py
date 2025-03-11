import wikipediaapi
import wikipedia
from translate import Translator
import streamlit as st
import time

@st.cache_data(ttl=3600)
def get_wikipedia_search_results(query, language="en"):
    """
    Search Wikipedia for articles matching the query in specified language
    
    Args:
        query (str): The search term
        language (str): Language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        list: List of article titles matching the query
    """
    if not query:
        return []
    
    try:
        # Set the language for the Wikipedia API
        wikipedia.set_lang(language)
        # Search for articles with the given query
        search_results = wikipedia.search(query, results=10)
        return search_results
    except Exception as e:
        st.error(f"Error searching Wikipedia: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def get_article_content(title, language="en"):
    """
    Get the content of a Wikipedia article
    
    Args:
        title (str): The title of the article
        language (str): Language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        dict: Dictionary containing article title, summary, content and URL
    """
    if not title:
        return None
    
    try:
        # Initialize Wikipedia API with the specified language
        wiki_wiki = wikipediaapi.Wikipedia(language)
        # Get the page
        page = wiki_wiki.page(title)
        
        if not page.exists():
            return None
        
        return {
            "title": page.title,
            "summary": page.summary,
            "content": page.text,
            "url": page.fullurl
        }
    except Exception as e:
        st.error(f"Error retrieving article: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_available_languages(title, source_lang="en"):
    """
    Get available languages for a Wikipedia article
    
    Args:
        title (str): The title of the article
        source_lang (str): Source language code
        
    Returns:
        dict: Dictionary of language codes and titles
    """
    if not title:
        return {}
    
    try:
        # Initialize Wikipedia API
        wiki_wiki = wikipediaapi.Wikipedia(source_lang)
        # Get the page
        page = wiki_wiki.page(title)
        
        if not page.exists():
            return {}
        
        # Get langlinks (article versions in other languages)
        langlinks = page.langlinks
        available_langs = {lang: langlinks[lang].title for lang in langlinks}
        
        # Add the source language
        available_langs[source_lang] = title
        
        return available_langs
    except Exception as e:
        st.error(f"Error retrieving language versions: {str(e)}")
        return {}

@st.cache_data(ttl=3600)
def get_article_in_language(title, lang):
    """
    Get article content in the specified language
    
    Args:
        title (str): Title of the article in the specified language
        lang (str): Language code
        
    Returns:
        dict: Article content in the specified language
    """
    return get_article_content(title, lang)

def translate_text(text, to_lang, from_lang='auto'):
    """
    Translate text using free translation library
    
    Args:
        text (str): Text to translate
        to_lang (str): Target language code
        from_lang (str): Source language code
        
    Returns:
        str: Translated text
    """
    if not text:
        return ""
    
    try:
        # Using translate library (free but with limitations)
        translator = Translator(to_lang=to_lang, from_lang=from_lang)
        
        # For long texts, we need to split it into smaller chunks
        # to avoid exceeding translate library's limits
        chunk_size = 500  # Characters
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        translated_chunks = []
        for chunk in chunks:
            translation = translator.translate(chunk)
            translated_chunks.append(translation)
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
        
        return ' '.join(translated_chunks)
    except Exception as e:
        st.warning(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails

# Dictionary mapping language codes to language names
LANGUAGE_DICT = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ko': 'Korean',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'da': 'Danish',
    'pl': 'Polish',
    'uk': 'Ukrainian',
    'el': 'Greek',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'vi': 'Vietnamese',
    'fa': 'Persian',
    'tr': 'Turkish',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'th': 'Thai'
}

def get_language_name(lang_code):
    """
    Get the full language name from a language code
    
    Args:
        lang_code (str): Language code (e.g., 'en', 'es')
        
    Returns:
        str: Full language name
    """
    return LANGUAGE_DICT.get(lang_code, lang_code)
