import re

inputs = [
    # '''
    # def hello_world():
    #     # A simple comment preceding a simple print statement
    #     print("Hello World")  # say hi
    # ''',
    # '''
    # def say_hello(name):
    #     """A simple function that says hello... Richie style"""
    #     print(f"Hello {name}, is it me you're looking for?")
    # ''',
    # '''
    # class SimpleClass:
    #     """Class docstrings go here."""
    
    #     def say_hello(self, name: str):
    #         """Class method docstrings go here."""
    #         print(f'Hello {name}')
    # ''',
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
    result = []
    is_docstring = False
    for line in code.splitlines():
        doc_parts = len(line.split('"""'))
        if doc_parts == 3:
            continue

        if doc_parts == 2:
            is_docstring = not is_docstring
            continue

        if is_docstring:
            continue

        # remove whole line comment
        if re.match(r'^\s*#.*$', line):
            continue

        result.append(re.sub(r'  #.*$', '', line))

    print('\n'.join(result))
    return '\n'.join(result)

for line in inputs:
    strip_comments(line)
