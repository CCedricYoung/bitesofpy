import re

inputs = [
    '''
    def hello_world():
        # A simple comment preceding a simple print statement
        print("Hello World")
    ''',
    '''
    def say_hello(name):
        """A simple function that says hello... Richie style"""
        print(f"Hello {name}, is it me you're looking for?")
    ''',
    '''
    class SimpleClass:
        """Class docstrings go here."""
    
        def say_hello(self, name: str):
            """Class method docstrings go here."""
            print(f'Hello {name}')
    ''',
    '''
    def __init__(self, name, sound, num_legs):
        """
        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        num_legs : int, optional
            The number of legs the animal (default is 4)
        """
        self.name = name
        self.sound = sound
        self.num_legs = num_legs
    ''',
]

def strip_comments(code):
    # remove whole line strip_comments r'\s*#.*$\n' => ''
    
    code = re.sub(r'\s*#.*$\n', '', code)
    
    # remove side comments 
    code = re.sub(r'  #.*$', '', code)

    print(code)    
    return code

if __file__ ==  '__main__':
    for line in inputs:
        strip_comments(line)
