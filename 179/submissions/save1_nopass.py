import re

def strip_comments(code):
    # remove whole line strip_comments r'\s*#.*$\n' => ''
    
    code = re.sub(r'\s*#.*$\n', '', code)
    
    # remove side comments 
    code = re.sub(r'  #.*$', '', code)
    
    return code