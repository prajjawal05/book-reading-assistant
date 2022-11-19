from enum import Enum

class InstructionType(Enum):
    LIST_BOOKS = "LIST_BOOKS",
    LAST_READING = "LAST_READING"
    READ_BOOK = "READ_BOOK"
    CONTINUE_READING = "CONTINUE_READING"
    PAUSE = "PAUSE"


INSTRUCTIONS = [{
    "type": InstructionType.LIST_BOOKS,
    "inputMessages": ['what.*books.*have.*', '.*list.*books.*'],
    "outputMessage": "The books that you have are:"
},
{
    "type": InstructionType.LAST_READING,
    "inputMessages": ['.*last.*reading.*'],
    "outputMessage": "Last book read"
}, 
{
    "type": InstructionType.CONTINUE_READING,
    "inputMessages": ['.*continue.*'],
    "outputMessage": "Continue book read"
}, 
{
    "type": InstructionType.READ_BOOK,
    "inputMessages": ['read.*'],
    "outputMessage": "Reading book"
}, 
{
    "type": InstructionType.PAUSE,
    "inputMessages": ['pause'],
    "outputMessage": "Welcome!"
}]

INSTRUCTIONS_AVAILABLE = """
1. List all the books you have.
2. Last reading book
3. Continue reading book
4. Read a book:
    a. From where you left.
    b. From the beginning.
5. Pause a reading book
"""

# todo: increase instruction set, make more ui interactive