from resources.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from resources.parser.parser import Parser
from resources.semantic_analyzer.semantic import SemanticAnalyzer
from resources.parser.grammar import Grammar

class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_scope = None
        self.symbol_table = None

    def generate_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def add_code(self, code):
        self.code.append(code)

    def parse(self, data,  sema):
        
        # Obtain symbol table and AST
        self.symbol_table = sema.get_symbol_table()
        ast_root = sema.get_ast_root()

        # Generate intermediate code
        
        print(self.generate_code(ast_root))

    def generate_code(self, node):
        if node is None:
            return

        if node.symbol() == "PROGRAM":
            for child in node.children:
                self.generate_code(child)
        elif node.symbol() == "FUNCDEF":
            self.generate_function(node)
        elif node.symbol() == "STATEMENT":
            self.generate_statement(node)
        elif node.symbol() == "EXPRESSION":
            self.generate_expression(node)
        else:
            pass

    def generate_function(self, node):
        func_name = node.children[1].lexeme()
        self.add_code(f"function {func_name}:")
        self.current_scope = self.symbol_table.get_scope(func_name)
        
        for param in node.children[3].children:
            self.add_code(f"param {param.lexeme()}")
        
        for statement in node.children[6].children:
            self.generate_code(statement)
        
        self.add_code("end function")
        self.current_scope = self.current_scope.parent

    def generate_statement(self, node):
        if node.children[0].symbol() == "VARDECL":
            self.generate_var_declaration(node.children[0])
        elif node.children[0].symbol() == "ATRIBSTAT":
            self.generate_assignment(node.children[0])
        elif node.children[0].symbol() == "PRINTSTAT":
            self.generate_print(node.children[0])
        elif node.children[0].symbol() == "READSTAT":
            self.generate_read(node.children[0])
        elif node.children[0].symbol() == "RETURNSTAT":
            self.generate_return(node.children[0])
        elif node.children[0].symbol() == "IFSTAT":
            self.generate_if_statement(node.children[0])
        elif node.children[0].symbol() == "FORSTAT":
            self.generate_for_loop(node.children[0])
        elif node.children[0].symbol() == "STATELIST":
            for statement in node.children[0].children:
                self.generate_code(statement)

    def generate_var_declaration(self, node):
        var_type = node.children[0].lexeme()
        var_name = node.children[1].lexeme()
        self.add_code(f"declare {var_type} {var_name}")

    def generate_assignment(self, node):
        lvalue = self.generate_lvalue(node.children[0])
        expression = self.generate_expression(node.children[1])
        self.add_code(f"{lvalue} = {expression}")

    def generate_print(self, node):
        expression = self.generate_expression(node.children[0])
        self.add_code(f"print {expression}")

    def generate_read(self, node):
        lvalue = self.generate_lvalue(node.children[0])
        self.add_code(f"read {lvalue}")

    def generate_return(self, node):
        if node.children:
            expression = self.generate_expression(node.children[0])
            self.add_code(f"return {expression}")
        else:
            self.add_code("return")

    def generate_if_statement(self, node):
        condition = self.generate_expression(node.children[0])
        true_label = self.generate_label()
        end_label = self.generate_label()
        
        self.add_code(f"if {condition} goto {true_label}")
        if len(node.children) > 2:  # If there's an else clause
            self.generate_code(node.children[2])
        self.add_code(f"goto {end_label}")
        self.add_code(f"{true_label}:")
        self.generate_code(node.children[1])
        self.add_code(f"{end_label}:")

    def generate_for_loop(self, node):
        init = node.children[0]
        condition = node.children[1]
        update = node.children[2]
        body = node.children[3]

        self.generate_code(init)
        start_label = self.generate_label()
        end_label = self.generate_label()

        self.add_code(f"{start_label}:")
        cond_result = self.generate_expression(condition)
        self.add_code(f"if not {cond_result} goto {end_label}")
        self.generate_code(body)
        self.generate_code(update)
        self.add_code(f"goto {start_label}")
        self.add_code(f"{end_label}:")

    def generate_expression(self, node):
        if node.children:
            for child in node.children:
                self.generate_expression(child)

    def generate_lvalue(self, node):
        if len(node.children) == 1:  # Simple variable
            return node.children[0].lexeme()
        else:  # Array access
            array = node.children[0].lexeme()
            index = self.generate_expression(node.children[1])
            return f"{array}[{index}]"

    def get_code(self):
        return "\n".join(self.code)
