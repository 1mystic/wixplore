#!/usr/bin/env python3
"""
Language Extraction Agent
Extracts and analyzes language patterns, text features, and linguistic insights
"""

import sys
import json
import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import Counter, defaultdict

def extract_language_features(file_path, parameters=None):
    """
    Extract and analyze language patterns from text data
    
    Args:
        file_path (str): Path to the data file
        parameters (dict): Optional language extraction parameters
    
    Returns:
        dict: Language analysis results
    """
    try:
        # Default parameters
        default_params = {
            'detect_languages': True,
            'extract_keywords': True,
            'analyze_sentiment': False,  # Placeholder for future implementation
            'min_word_length': 3,
            'max_keywords': 50,
            'include_patterns': True,
            'text_columns': 'auto'  # Auto-detect or specify column names
        }
        
        if parameters:
            default_params.update(parameters)
        
        # Read data
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.json':
            df = pd.read_json(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Identify text columns
        if default_params['text_columns'] == 'auto':
            text_columns = identify_text_columns(df)
        else:
            text_columns = default_params['text_columns']
        
        if not text_columns:
            return {
                'status': 'success',
                'message': 'No text columns found for language analysis',
                'text_columns': [],
                'analysis': {}
            }
        
        analysis_results = {}
        
        for col in text_columns:
            col_analysis = analyze_text_column(df[col], default_params)
            analysis_results[col] = col_analysis
        
        # Global analysis across all text columns
        global_analysis = perform_global_text_analysis(df, text_columns, default_params)
        
        # Language detection summary
        language_summary = summarize_languages(analysis_results)
        
        # Pattern analysis
        pattern_analysis = analyze_text_patterns(df, text_columns)
        
        # Cultural context extraction (placeholder for domain-specific analysis)
        cultural_context = extract_cultural_context(df, text_columns)
        
        result = {
            'status': 'success',
            'text_columns': text_columns,
            'column_analysis': analysis_results,
            'global_analysis': global_analysis,
            'language_summary': language_summary,
            'pattern_analysis': pattern_analysis,
            'cultural_context': cultural_context,
            'recommendations': generate_language_recommendations(analysis_results, global_analysis),
            'parameters_used': default_params
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': str(e.__class__.__name__)
        }

def identify_text_columns(df):
    """Identify columns that contain text data"""
    text_columns = []
    
    for col in df.columns:
        if df[col].dtype == 'object':
            # Sample some values to check if they contain meaningful text
            sample_values = df[col].dropna().head(100)
            
            if len(sample_values) > 0:
                # Check average length and word count
                avg_length = sample_values.astype(str).str.len().mean()
                has_spaces = sample_values.astype(str).str.contains(' ').sum() / len(sample_values)
                
                # Consider it text if average length > 10 and many values contain spaces
                if avg_length > 10 and has_spaces > 0.3:
                    text_columns.append(col)
    
    return text_columns

def analyze_text_column(text_series, params):
    """Analyze a single text column"""
    text_data = text_series.dropna().astype(str)
    
    if len(text_data) == 0:
        return {'error': 'No valid text data found'}
    
    analysis = {}
    
    # Basic statistics
    analysis['basic_stats'] = {
        'total_texts': len(text_data),
        'avg_length': float(text_data.str.len().mean()),
        'max_length': int(text_data.str.len().max()),
        'min_length': int(text_data.str.len().min()),
        'total_characters': int(text_data.str.len().sum())
    }
    
    # Word analysis
    all_text = ' '.join(text_data.values)
    words = extract_words(all_text, params['min_word_length'])
    
    analysis['word_analysis'] = {
        'total_words': len(words),
        'unique_words': len(set(words)),
        'avg_words_per_text': len(words) / len(text_data),
        'vocabulary_richness': len(set(words)) / len(words) if words else 0
    }
    
    # Keyword extraction
    if params['extract_keywords']:
        analysis['keywords'] = extract_keywords(words, params['max_keywords'])
    
    # Language detection (simple heuristic)
    if params['detect_languages']:
        analysis['language_detection'] = detect_language_heuristic(all_text)
    
    # Text patterns
    if params['include_patterns']:
        analysis['patterns'] = detect_text_patterns(text_data)
    
    return analysis

def extract_words(text, min_length=3):
    """Extract words from text"""
    # Simple word extraction
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [word for word in words if len(word) >= min_length]

def extract_keywords(words, max_keywords=50):
    """Extract most frequent keywords"""
    word_counts = Counter(words)
    
    # Filter out common stop words (basic list)
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
        'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'a', 'an',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'shall'
    }
    
    filtered_counts = {word: count for word, count in word_counts.items() 
                      if word not in stop_words and len(word) > 2}
    
    return dict(Counter(filtered_counts).most_common(max_keywords))

def detect_language_heuristic(text):
    """Simple language detection using character patterns"""
    text_lower = text.lower()
    
    # Simple heuristics for common languages
    language_patterns = {
        'english': ['the', 'and', 'of', 'to', 'in', 'is', 'you', 'that', 'it', 'he'],
        'spanish': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se'],
        'french': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
        'german': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
        'italian': ['il', 'di', 'che', 'e', 'la', 'per', 'un', 'in', 'con', 'del']
    }
    
    language_scores = {}
    
    for lang, patterns in language_patterns.items():
        score = sum(1 for pattern in patterns if pattern in text_lower)
        language_scores[lang] = score
    
    if language_scores:
        detected_language = max(language_scores, key=language_scores.get)
        confidence = language_scores[detected_language] / len(language_patterns[detected_language])
        
        return {
            'detected_language': detected_language,
            'confidence': round(confidence, 2),
            'all_scores': language_scores
        }
    
    return {'detected_language': 'unknown', 'confidence': 0}

def detect_text_patterns(text_series):
    """Detect patterns in text data"""
    patterns = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_count = text_series.str.contains(email_pattern, regex=True).sum()
    if email_count > 0:
        patterns['emails'] = int(email_count)
    
    # URL pattern
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url_count = text_series.str.contains(url_pattern, regex=True).sum()
    if url_count > 0:
        patterns['urls'] = int(url_count)
    
    # Phone pattern (simple)
    phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
    phone_count = text_series.str.contains(phone_pattern, regex=True).sum()
    if phone_count > 0:
        patterns['phone_numbers'] = int(phone_count)
    
    # Hashtag pattern
    hashtag_pattern = r'#\w+'
    hashtag_count = text_series.str.contains(hashtag_pattern, regex=True).sum()
    if hashtag_count > 0:
        patterns['hashtags'] = int(hashtag_count)
    
    # Mention pattern
    mention_pattern = r'@\w+'
    mention_count = text_series.str.contains(mention_pattern, regex=True).sum()
    if mention_count > 0:
        patterns['mentions'] = int(mention_count)
    
    return patterns

def perform_global_text_analysis(df, text_columns, params):
    """Perform analysis across all text columns"""
    all_text = ""
    
    for col in text_columns:
        col_text = ' '.join(df[col].dropna().astype(str).values)
        all_text += " " + col_text
    
    if not all_text.strip():
        return {}
    
    # Global word analysis
    words = extract_words(all_text, params['min_word_length'])
    
    global_analysis = {
        'total_words_across_columns': len(words),
        'unique_words_across_columns': len(set(words)),
        'most_common_words': dict(Counter(words).most_common(20)),
        'vocabulary_diversity': len(set(words)) / len(words) if words else 0
    }
    
    # Character analysis
    global_analysis['character_analysis'] = {
        'total_characters': len(all_text),
        'alphabetic_ratio': sum(c.isalpha() for c in all_text) / len(all_text),
        'numeric_ratio': sum(c.isdigit() for c in all_text) / len(all_text),
        'whitespace_ratio': sum(c.isspace() for c in all_text) / len(all_text),
        'punctuation_ratio': sum(not c.isalnum() and not c.isspace() for c in all_text) / len(all_text)
    }
    
    return global_analysis

def summarize_languages(analysis_results):
    """Summarize language detection across all columns"""
    languages = defaultdict(int)
    total_confidence = 0
    
    for col, analysis in analysis_results.items():
        if 'language_detection' in analysis:
            lang_info = analysis['language_detection']
            languages[lang_info['detected_language']] += lang_info['confidence']
            total_confidence += lang_info['confidence']
    
    if languages:
        # Normalize confidence scores
        normalized_languages = {lang: conf/len(analysis_results) 
                              for lang, conf in languages.items()}
        
        primary_language = max(normalized_languages, key=normalized_languages.get)
        
        return {
            'primary_language': primary_language,
            'language_distribution': dict(normalized_languages),
            'confidence': round(normalized_languages[primary_language], 2)
        }
    
    return {'primary_language': 'unknown', 'confidence': 0}

def analyze_text_patterns(df, text_columns):
    """Analyze patterns across text columns"""
    pattern_summary = defaultdict(int)
    
    for col in text_columns:
        patterns = detect_text_patterns(df[col])
        for pattern_type, count in patterns.items():
            pattern_summary[pattern_type] += count
    
    return dict(pattern_summary)

def extract_cultural_context(df, text_columns):
    """Extract cultural context from text (placeholder for advanced analysis)"""
    cultural_indicators = {}
    
    # Simple cultural keyword detection
    cultural_keywords = {
        'food_terms': ['food', 'cuisine', 'dish', 'recipe', 'cooking', 'meal'],
        'location_terms': ['country', 'city', 'region', 'place', 'location'],
        'tradition_terms': ['tradition', 'culture', 'custom', 'heritage', 'festival'],
        'language_terms': ['language', 'speak', 'words', 'dialect', 'accent']
    }
    
    for col in text_columns:
        col_text = ' '.join(df[col].dropna().astype(str).values).lower()
        
        for category, keywords in cultural_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in col_text)
            if matches > 0:
                cultural_indicators[category] = matches
    
    return cultural_indicators

def generate_language_recommendations(analysis_results, global_analysis):
    """Generate recommendations based on language analysis"""
    recommendations = []
    
    # Check for multilingual content
    languages = set()
    for analysis in analysis_results.values():
        if 'language_detection' in analysis:
            languages.add(analysis['language_detection']['detected_language'])
    
    if len(languages) > 1:
        recommendations.append("Multilingual content detected - consider language-specific processing")
    
    # Check vocabulary richness
    if 'vocabulary_diversity' in global_analysis:
        diversity = global_analysis['vocabulary_diversity']
        if diversity > 0.7:
            recommendations.append("High vocabulary diversity - rich linguistic content")
        elif diversity < 0.3:
            recommendations.append("Low vocabulary diversity - consider content enrichment")
    
    # Check for patterns
    pattern_found = False
    for analysis in analysis_results.values():
        if 'patterns' in analysis and analysis['patterns']:
            pattern_found = True
            break
    
    if pattern_found:
        recommendations.append("Structured patterns detected - suitable for information extraction")
    
    return recommendations

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'File path required'}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    parameters = {}
    
    if len(sys.argv) > 2:
        try:
            parameters = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass
    
    result = extract_language_features(file_path, parameters)
    print(json.dumps(result, default=str))

if __name__ == '__main__':
    main()
