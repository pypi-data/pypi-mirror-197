"""
module to say hello
"""

def say_hello(name=None):
    """
    a function to greet!
    """
    if name is None:
        return "Hello, World"
    else:
        return f"Hello, {name}!"
