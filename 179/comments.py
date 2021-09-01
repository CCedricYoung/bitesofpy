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
    # '''
    # def __init__(self, name, sound, num_legs):
    #     """
    #     Parameters
    #     ----------
    #     name : str
    #         The name of the animal
    #     sound : str
    #         The sound the animal makes
    #     num_legs : int, optional
    #         The number of legs the animal (default is 4)
    #     """
    #     self.name = name
    #     self.sound = sound
    #     self.num_legs = num_legs
    # ''',
    '''
"""this is
my awesome script
"""
# importing modules
import re

def hello(name):
    """my function docstring"""
    return f'hello {name}'  # my inline comment
    ''',
]

def strip_comments(code):
    return re.sub(r'(\n\s*?# .*|  #.*|\n\s*"""(.|\n)*?""")(?=\n)', '', code, re.MULTILINE)

for line in inputs:
    print(strip_comments(line))
