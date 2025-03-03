class DFA:
    def __init__(self):
        # Define states for our simple DFA
        self.states = {
            'start': 0,
            'greeting': 1,
            'subject': 2,
            'verb': 3,
            'object': 4,
            'question': 5,
            'end': 6
        }
        
        # Current state
        self.current_state = self.states['start']
        
        # Define transition function
        self.transitions = {
            # From start state
            (self.states['start'], 'greeting'): self.states['greeting'],
            (self.states['start'], 'subject'): self.states['subject'],
            (self.states['start'], 'question_word'): self.states['question'],
            
            # From greeting state
            (self.states['greeting'], 'end'): self.states['end'],
            
            # From subject state
            (self.states['subject'], 'verb'): self.states['verb'],
            
            # From verb state
            (self.states['verb'], 'object'): self.states['object'],
            (self.states['verb'], 'end'): self.states['end'],
            
            # From object state
            (self.states['object'], 'end'): self.states['end'],
            
            # From question state
            (self.states['question'], 'rest'): self.states['end']
        }
        
        # Define accepting states
        self.accepting_states = [self.states['end'], self.states['greeting'], self.states['object'], self.states['verb']]
    
    def process(self, input_symbols):
        self.current_state = self.states['start']
        
        for symbol in input_symbols:
            if (self.current_state, symbol) in self.transitions:
                self.current_state = self.transitions[(self.current_state, symbol)]
            else:
                # If no valid transition, try to go to end
                if (self.current_state, 'end') in self.transitions:
                    self.current_state = self.transitions[(self.current_state, 'end')]
        
        return self.current_state in self.accepting_states