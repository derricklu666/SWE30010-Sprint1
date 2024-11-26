import random
import re
import spacy
import json

class SimpleChatbot:
    def __init__(self):
        # Load the small English model
        self.nlp = spacy.load('en_core_web_sm')
        
        self.patterns = {
            r'hi|hello|hey': ['Hello!', 'Hi there!', 'Hey!'],
            r'how are you': ['I\'m doing well, thanks!', 'Great! How are you?'],
            r'what is your name': ['I\'m SimpleBot!', 'You can call me SimpleBot'],
            r'bye|goodbye': ['Goodbye!', 'See you later!', 'Take care!'],
            r'weather': ['I cannot check the weather, I\'m a simple chatbot.'],
            r'help': ['I can chat about basic topics. Try saying hello!'],
        }
        self.load_patterns()
    
    def load_patterns(self):
        try:
            with open('training_data.json', 'r') as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            self.save_patterns()

    def save_patterns(self):
        with open('training_data.json', 'w') as f:
            json.dump(self.patterns, f, indent=2)

    def train(self, pattern, response):
        if pattern in self.patterns:
            if response not in self.patterns[pattern]:
                self.patterns[pattern].append(response)
        else:
            self.patterns[pattern] = [response]
        self.save_patterns()
    
    def preprocess(self, text):
        # Process the text with spaCy
        doc = self.nlp(text.lower())
        
        # Filter out stop words and punctuation, lemmatize tokens
        tokens = [token.lemma_ for token in doc 
                 if not token.is_stop and not token.is_punct and token.is_alpha]
        
        return ' '.join(tokens)
    
    def get_response(self, user_input):
        # Preprocess the input using spaCy
        processed_input = self.preprocess(user_input)
        
        # First try matching the processed input
        for pattern, responses in self.patterns.items():
            if re.search(pattern, processed_input):
                return random.choice(responses)
        
        # If no match found, try matching the original input (for better pattern matching)
        user_input = user_input.lower()
        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input):
                return random.choice(responses)
                
        return "I'm not sure how to respond to that. Try asking something else!"

def main():
    chatbot = SimpleChatbot()
    print("SimpleBot: Hi! I'm a simple chatbot. Type 'bye' to exit.")
    print("To train me, use format: train:pattern:response")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'goodbye']:
            print("SimpleBot:", chatbot.get_response(user_input))
            break
        elif user_input.startswith('train:'):
            try:
                _, pattern, response = user_input.split(':')
                chatbot.train(pattern, response)
                print("SimpleBot: Thanks, I learned that!")
            except ValueError:
                print("SimpleBot: Training format is train:pattern:response")
        else:
            response = chatbot.get_response(user_input)
            print("SimpleBot:", response)

if __name__ == "__main__":
    main()