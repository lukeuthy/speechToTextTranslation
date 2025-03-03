class CFG:
    def __init__(self):
        # Define production rules for a simple English sentence structure
        self.rules = {
            'S': [['NP', 'VP']],                     # Sentence → Noun Phrase + Verb Phrase
            'NP': [['DET', 'N'], ['PRO']],           # Noun Phrase → Determiner + Noun, or Pronoun
            'VP': [['V'], ['V', 'NP'], ['V', 'ADJ']] # Verb Phrase → Verb, Verb + Noun Phrase, or Verb + Adjective
        }
        
        # Define terminal categories
        self.terminals = {
            'DET': ['the', 'a', 'my', 'your', 'this', 'that'],
            'N': ['water', 'food', 'friend', 'car', 'house', 'book', 'money', 'love', 'help'],
            'PRO': ['i', 'you', 'he', 'she', 'it', 'we', 'they'],
            'V': ['is', 'am', 'are', 'want', 'need', 'like', 'love', 'have', 'see'],
            'ADJ': ['good', 'bad', 'happy', 'sad', 'big', 'small']
        }
    
    def parse(self, tokens):
        # Simple parsing to identify sentence components
        result = {'structure': [], 'type': 'unknown'}
        
        # Check for greeting patterns
        if any(greeting in ' '.join(tokens).lower() for greeting in ['hello', 'good morning', 'good afternoon', 'good evening']):
            result['type'] = 'greeting'
            result['structure'] = ['greeting']
            return result
            
        # Check for question patterns
        if tokens and tokens[0].lower() in ['what', 'who', 'where', 'when', 'how', 'why']:
            result['type'] = 'question'
            result['structure'] = ['question_word', 'rest']
            return result
            
        # Check for basic subject-verb pattern
        if len(tokens) >= 2:
            if tokens[0].lower() in self.terminals['PRO'] and tokens[1].lower() in self.terminals['V']:
                result['type'] = 'statement'
                result['structure'] = ['subject', 'verb', 'object']
                return result
        
        return result