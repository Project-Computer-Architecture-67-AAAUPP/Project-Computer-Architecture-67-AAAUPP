def decimal_to_binary(decimal_file, binary_file):
    with open(decimal_file, 'r') as f_in, open(binary_file, 'w') as f_out:
        for line in f_in:
            # Convert decimal to integer, handling negative numbers
            decimal = int(line.strip())
            
            # Convert to 32-bit binary, handling negative numbers
            if decimal < 0:
                binary = format(decimal & 0xFFFFFFFF, '032b')
            else:
                binary = format(decimal, '032b')
            
            # Divide into 8-bit chunks (LSB is already at the rightmost position)
            chunks = [binary[i:i+8] for i in range(0, 32, 8)]
            
            # Join chunks with spaces, add the decimal as a comment, and write to output file
            f_out.write(f"{' '.join(chunks)} # {decimal}\n")

if __name__ == "__main__":
    input_file = "teacher.mc"
    output_file = "teacher_binary.txt"
    decimal_to_binary(input_file, output_file)
    print(f"Conversion complete. Binary output saved to {output_file}")