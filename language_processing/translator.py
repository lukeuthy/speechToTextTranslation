from word_bank import WORD_BANK
from language_processing.cfg import CFG
from language_processing.dfa import DFA

def translate_to_malay(english_text):
    if not english_text:
        return ""
        
    # Preprocess text
    english_text = english_text.lower().strip()
    
    # First check if the full phrase is in our word bank
    if english_text in WORD_BANK:
        return WORD_BANK[english_text]
    
    # Tokenize the input
    tokens = english_text.split()
    
    # Use CFG to parse the sentence structure
    cfg = CFG()
    parse_result = cfg.parse(tokens)
    
    # Use DFA to validate the sentence structure
    dfa = DFA()
    is_valid = dfa.process(parse_result['structure'])
    
    if not is_valid:
        return "Cannot translate: unrecognized sentence structure"
    
    # Translate word by word
    translated_words = []
    for word in tokens:
        if word.lower() in WORD_BANK:
            translated_words.append(WORD_BANK[word.lower()])
        else:
            # Keep untranslated words as they are
            translated_words.append(word)
    
    # Apply Malay grammar rules - this is a basic implementation
    # In Malay, adjectives typically follow nouns (unlike English)
    # This is a simplified approach and won't work for all cases
    result = ' '.join(translated_words)
    
    return result

def analyze_text(english_text):
    if not english_text:
        return None
        
    tokens = english_text.split()
    cfg = CFG()
    parse_result = cfg.parse(tokens)
    dfa = DFA()
    is_valid = dfa.process(parse_result['structure'])
    
    return {
        'tokens': tokens,
        'structure': parse_result['structure'],
        'type': parse_result['type'],
        'valid': is_valid
    }