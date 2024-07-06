from resources.parser.grammar import Grammar
from resources.semantic_analyzer.semantic import SemanticAnalyzer

class SDDParser:
    def __init__(self, grammar_text):
        self.semantic_analyzer = SemanticAnalyzer()
        self.grammar = Grammar(grammar_text)

    def parse(self, data):
        self.grammar.parse(data)
        self.semantic_analyzer.analyze(self.grammar.get_tree())

'''
if __name__ == '__main__':
    try:
        with open('./src/resources/grammar.txt') as grammar_text:
            with open('./data.txt') as data:
                parser = SDDParser(grammar_text.read())
                parser.parse(data.read())
    except Exception as e:
        print(e)
'''