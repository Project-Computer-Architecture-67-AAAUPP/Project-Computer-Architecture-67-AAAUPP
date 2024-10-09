# Combination(n, r)
            lw      0       1       n           # โหลดค่า n จาก memory ลงใน reg1
            lw      0       2       r           # โหลดค่า r จาก memory ลงใน reg2
            lw      0       3       neg1        # โหลดค่า -1 ลงใน reg3
            lw      0       4       one         # โหลดค่า 1 ลงใน reg4
            lw      0       5       stackPtr    # โหลดค่า stack pointer ลงใน reg5

            beq     2       0       base_case   # ถ้า r == 0 ให้กระโดดไป base case
            beq     1       2       base_case   # ถ้า n == r ให้กระโดดไป base case

            add     1       3       6           # n-1 (reg1 + reg3 -> reg6)
            add     2       3       7           # r-1 (reg2 + reg3 -> reg7)
            
            sw      5       1       stack       # เก็บ n ลง stack
            add     5       4       5           # เพิ่ม stack pointer
            sw      5       2       stack       # เก็บ r ลง stack
            add     5       4       5           # เพิ่ม stack pointer
            
            jalr    4       6                   # recursive call combination(n-1, r)
            
            add     5       3       5           # ลด stack pointer (reg5 = reg5 + reg3)
            lw      1       5       stack       # ดึงค่า r กลับจาก stack
            add     5       3       5           # ลด stack pointer (reg5 = reg5 + reg3)
            lw      2       5       stack       # ดึงค่า n กลับจาก stack

            jalr    4       7                   # recursive call combination(n-1, r-1)

            add     3       4       4           # นำค่าทั้งสองมาบวกกัน

            halt                                # จบการทำงาน

base_case   lw      0       3       one         # ถ้าเป็น base case ให้ return 1
            halt                                # จบการทำงาน

            n       .fill   7                           # ค่า n
            r       .fill   3                           # ค่า r
            zero    .fill   0                           # กำหนดค่า 0
            one     .fill   1                           # กำหนดค่า 1
            neg1    .fill   -1                          # กำหนดค่า -1
            stackPtr .fill   stack                      # กำหนดค่า stack pointer
            stack   .fill   0                           # Stack สำหรับเก็บค่าระหว่างการเรียก
