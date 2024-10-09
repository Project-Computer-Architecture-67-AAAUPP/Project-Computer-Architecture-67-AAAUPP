import sys

# แปลง opcode เป็นเลขฐานสอง
OPCODES = {
    'add': '000',
    'nand': '001',
    'lw': '010',
    'sw': '011',
    'beq': '100',
    'jalr': '101',
    'halt': '110',
    'noop': '111'
}

# รวบรวม label และ address ของมัน
def first_pass(input_file):
    labels = {}
    address = 0
    # เปิดไฟล์โดยใช้ encoding 'utf-8'
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            # ข้ามบรรทัดที่เป็นคอมเมนต์หรือบรรทัดว่าง
            parts = line.split()
            if len(parts) > 0 and not parts[0].startswith('#'):
                # ตรวจสอบว่าบรรทัดนั้นมี label
                if parts[0] not in OPCODES and parts[0] != '.fill':
                    if parts[0] in labels:
                        print(f"Error: Duplicate label '{parts[0]}' at address {address}")
                        sys.exit(1)
                    labels[parts[0]] = address
                address += 1
    return labels

# แปลงคำสั่ง assembly เป็น machine code
def assemble_instruction(line, labels, current_address):
    parts = line.split()
    if len(parts) == 0 or parts[0].startswith('#'):
        return None  # ข้ามบรรทัดว่างหรือคอมเมนต์
    # ตรวจสอบว่ามี label ในบรรทัด
    if parts[0] not in OPCODES and parts[0] != '.fill':
        parts = parts[1:]  # ข้าม label ไป
    instruction = parts[0]
    if instruction in OPCODES:
        opcode = OPCODES[instruction]
        if instruction in ['add', 'nand']:  # R-type
            reg_a = int(parts[1])
            reg_b = int(parts[2])
            dest_reg = int(parts[3])
            return f"{opcode}{reg_a:03b}{reg_b:03b}{'0' * 13}{dest_reg:03b}"
        elif instruction in ['lw', 'sw', 'beq']:  # I-type
            reg_a = int(parts[1])
            reg_b = int(parts[2])
            offset_field = parts[3]
            
            # ตรวจสอบว่า offset_field เป็น label หรือไม่
            if offset_field in labels:
                # คำนวณ offset เป็น address ของ label - (current_address + 1)
                offset = labels[offset_field] - (current_address + 1)
            else:
                try:
                    offset = int(offset_field)  # ถ้าเป็นตัวเลข, ใช้ค่าตัวเลขนั้นโดยตรง
                except ValueError:
                    print(f"Error: Invalid offset or label in line: {line}")
                    sys.exit(1)

            # ตรวจสอบว่า offset อยู่ในช่วง -32768 ถึง 32767
            if offset < -32768 or offset > 32767:
                print(f"Error: Offset {offset} out of range at line: {line}")
                sys.exit(1)

            # แปลง offset เป็น 16-bit two's complement
            offset = offset & 0xFFFF  # เก็บเฉพาะ 16 บิต
            return f"{opcode}{reg_a:03b}{reg_b:03b}{offset:016b}"
        elif instruction == 'jalr':  # J-type
            reg_a = int(parts[1])
            reg_b = int(parts[2])
            return f"{opcode}{reg_a:03b}{reg_b:03b}{'0' * 16}"
        elif instruction in ['halt', 'noop']:  # O-type
            return f"{opcode}" + "0" * 22
    elif instruction == '.fill':  # จัดการกับคำสั่ง .fill
        value = parts[1]
        if value in labels:
            return str(labels[value])  # คืนค่า address ของ label
        else:
            try:
                return str(int(value))  # คืนค่าตัวเลขโดยตรง
            except ValueError:
                print(f"Error: Invalid .fill value in line: {line}")
                sys.exit(1)
    return None  # กรณีที่คำสั่งไม่ถูกต้อง

# อ่านไฟล์ Assembly และแปลงเป็น Machine Code
def assemble(input_file, output_file):
    labels = first_pass(input_file)  # เก็บ label ก่อน
    # เปิดไฟล์โดยใช้ encoding 'utf-8'
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        address = 0
        for line in infile:
            parts = line.split()
            if len(parts) == 0 or parts[0].startswith('#'):
                continue  # ข้ามบรรทัดว่างหรือคอมเมนต์
            machine_code = assemble_instruction(line, labels, address)
            if machine_code is not None:
                # ตรวจสอบว่าเป็นคำสั่ง .fill หรือไม่
                if parts[0] == '.fill' or (len(parts) > 1 and parts[1] == '.fill'):
                    # เขียนค่าโดยตรง (ค่าของ .fill เป็น decimal)
                    outfile.write(f"{machine_code}\n")
                else:
                    # แปลง machine code เป็น integer (ฐานสอง) และเขียนออกมา
                    outfile.write(f"{int(machine_code, 2)}\n")
            address += 1

# ทดสอบการทำงานของ Assembler
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python AssemblyToMachineCode.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    assemble(input_file, output_file)
    print(f"Assembly to Machine Code completed. Output written to {output_file}")
