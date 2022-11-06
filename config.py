from enum import Enum

class InstructionType(Enum):
    LIST_BOOKS = "LIST_BOOKS",
    LAST_READING = "LAST_READING"
    READ_BOOK = "READ_BOOK"
    STOP = "STOP"


INSTRUCTIONS = [{
    "type": InstructionType.LIST_BOOKS,
    "inputMessages": ['what books', 'list books'],
    "outputMessage": "The books that you have are:"
},
{
    "type": InstructionType.LAST_READING,
    "inputMessages": ['last reading'],
    "outputMessage": "The books that you were last reading was:"
},
{
    "type": InstructionType.READ_BOOK,
    "inputMessages": ['read me'],
    "outputMessage": "Reading book"
}, 
{
    "type": InstructionType.STOP,
    "inputMessages": ['stop'],
    "outputMessage": "Welcome!"
}]

INSTRUCTIONS_AVAILABLE = """
1. List all the books you have.
2. Continue listening the last book.
3. Read a book:
    a. From where you left.
    b. From the beginning.
"""

# todo: increase instruction set, make more ui interactive