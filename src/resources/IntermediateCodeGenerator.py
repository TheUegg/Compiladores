class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []  # Lista para armazenar o código intermediário gerado

    def parse(self, data):
        # Implementação para transformar o código de entrada em código de três endereços
        lines = data.splitlines()
        
        for line in lines:
            if line.strip():  # Ignora linhas em branco
                code_line = self.process_line(line.strip())
                if code_line:
                    self.code.append(code_line)

    def process_line(self, line):
        # Implementação para processar cada linha de código e gerar código de três endereços
        # Aqui você deve implementar a lógica para transformar a linha de código em código de três endereços
        # Exemplo simplificado:
        parts = line.split()
        
        if len(parts) == 3 and parts[1] == '=':
            return f"{parts[2]} = {parts[0]} {parts[1]} {parts[2]}"  # Exemplo básico
        
        return None

    def get_code(self):
        # Retorna o código intermediário gerado
        return self.code
