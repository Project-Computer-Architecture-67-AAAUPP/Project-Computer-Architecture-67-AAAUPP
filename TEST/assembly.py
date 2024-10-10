import sys

# Constants
MAXLINELENGTH = 1000  # Max length of a single line of code.
MAXLINES = 50          # Max assembly program length.
STACK_SIZE = 50       # Number of slots for the stack
# List of valid opcodes
VALID_OPCODES = ['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'halt', 'noop', '.fill']

# Symbolic Link Node (Linked List)
class SymbolicAddressNode:
    def __init__(self, label='', address=0):
        self.label = label
        self.address = address
        self.next = None

# Instruction Container
class InstructionNode:
    def __init__(self, address=0, opcode='', arg0='', arg1='', arg2=''):
        self.address = address
        self.opcode = opcode
        self.arg0 = arg0
        self.arg1 = arg1
        self.arg2 = arg2

# Helper function to open a file
def prepare_file(filename, mode):
    try:
        return open(filename, mode)
    except IOError:
        print(f"ERROR: Can't open file: {filename}!")
        sys.exit(1)

# Validate a label
def is_valid_label(label):
    if len(label) > 6:
        return False
    if not label[0].isalpha():
        return False
    return all(c.isalnum() for c in label)

# Add a new symbolic address to the linked list
def add_symbol(root, label, address):
    if not is_valid_label(label):
        print(f"ERROR: {label} is not a valid label. (see address {address})")
        sys.exit(1)

    node = root
    while node.next is not None:
        node = node.next
        if node.label == label:
            print(f"ERROR: Duplicate label, {label}, found. (see address {address})")
            sys.exit(1)

    new_node = SymbolicAddressNode(label, address)
    node.next = new_node

# Find the address of a symbolic label
def get_symbol_address(root, label):
    if not is_valid_label(label):
        print(f"ERROR: {label} is not a valid label.")
        sys.exit(1)

    node = root
    while node.next is not None:
        node = node.next
        if node.label == label:
            return node.address

    print(f"ERROR: Undeclared label {label}.")
    sys.exit(1)

# Read assembly instructions and populate the instruction list
def read_assembly(infile, root, instructions):
    i = 0  # indexor
    for line in infile:
        line = line.strip()
        if len(line) == 0:
            continue  # skip empty lines

        instructions[i] = InstructionNode(address=i)

        # Split the line into parts
        parts = line.split()

        # Check if the first part is a label (if it's not an opcode)
        if parts[0] not in VALID_OPCODES and is_valid_label(parts[0]):
            add_symbol(root, parts[0], i)
            parts = parts[1:]  # Remove the label from the line

        # Now process the rest of the line as the instruction
        if len(parts) > 0:
            instructions[i].opcode = parts[0]
        if len(parts) > 1:
            instructions[i].arg0 = parts[1]
        if len(parts) > 2:
            instructions[i].arg1 = parts[2]
        if len(parts) > 3:
            instructions[i].arg2 = parts[3]

        i += 1
        if i > MAXLINES:
            print(f"ERROR: Maximum program length exceeded. Maximum: {MAXLINES}")
            sys.exit(1)

    return i

# Write the binary representation to the output file
def write_binary(outfile, root, instructions, counter):
    for i in range(counter):
        outfile.write(f"{parse(root, instructions[i])}\n")

# Parse the instruction node and convert to binary
def parse(root, inode):
    if inode.opcode == 'add':
        return r_type(0 << 22, inode.arg0, inode.arg1, inode.arg2)
    elif inode.opcode == 'nand':
        return r_type(1 << 22, inode.arg0, inode.arg1, inode.arg2)
    elif inode.opcode == 'lw':
        offset = get_symbol_address(root, inode.arg2) if not inode.arg2.isdigit() else int(inode.arg2)
        return i_type(2 << 22, inode.arg0, inode.arg1, offset)
    elif inode.opcode == 'sw':
        offset = get_symbol_address(root, inode.arg2) if not inode.arg2.isdigit() else int(inode.arg2)
        return i_type(3 << 22, inode.arg0, inode.arg1, offset)
    elif inode.opcode == 'beq':
        if is_valid_label(inode.arg2):
            label_address = get_symbol_address(root, inode.arg2)
            offset = label_address - (inode.address + 1)  # Offset is relative to the next instruction
        else:
            offset = int(inode.arg2)

        if offset < -32768 or offset > 32767:
            print(f"ERROR: Offset {offset} out of range for beq at address {inode.address}")
            sys.exit(1)

        return i_type(4 << 22, inode.arg0, inode.arg1, offset)
    elif inode.opcode == 'jalr':
        return r_type(5 << 22, inode.arg0, inode.arg1, '0')  # Using r-type format for jalr
    elif inode.opcode == 'halt':
        return 6 << 22
    elif inode.opcode == 'noop':
        return 7 << 22
    elif inode.opcode == '.fill':
        if is_valid_label(inode.arg0):
            return get_symbol_address(root, inode.arg0)
        else:
            return int(inode.arg0)
    else:
        print(f"WARNING: Unrecognized opcode {inode.opcode} at address {inode.address}, skipping...")
        return 0

# Convert arguments to a bitstring representing an r-type instruction
def r_type(op, reg1, reg2, dest):
    regA = int(reg1)
    regB = int(reg2)
    destReg = int(dest)
    return (op | (regA << 19) | (regB << 16) | destReg)

# Convert arguments to a bitstring representing an i-type instruction
def i_type(op, reg1, reg2, offset):
    regA = int(reg1)
    regB = int(reg2)

    if offset < -32768 or offset > 32767:
        print(f"ERROR: Offset {offset} out of range for I-type instruction")
        sys.exit(1)

    if offset < 0:
        offset = (1 << 16) + offset  # Convert to 16-bit two's complement

    return (op | (regA << 19) | (regB << 16) | offset)

# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"ERROR: Usage: {sys.argv[0]} <assembly-code-file> <machine-code-file>")
        sys.exit(1)

    infile = prepare_file(sys.argv[1], 'r')
    outfile = prepare_file(sys.argv[2], 'w+')

    symbol_list = SymbolicAddressNode()
    instructions = [None] * MAXLINES

    instruction_counter = read_assembly(infile, symbol_list, instructions)
    write_binary(outfile, symbol_list, instructions, instruction_counter)

    infile.close()
    outfile.close()