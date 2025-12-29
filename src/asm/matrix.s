.intel_syntax noprefix
    
    # Disable executable stack warning
    .section .note.GNU-stack,"",@progbits

    .section .rodata
str_matrix_size: .string "MATRIX_SIZE"
str_output_header: .string "Matrix(%dx%d)\n"
str_output_res:    .string "Result[0]: %.4f\n"
str_output_time:   .string "Time: %.3f ms\n"

val_1_0:  .double 1.0
val_0_01: .double 0.01
val_1000: .double 1000.0
val_1M:   .double 1000000.0

    .section .bss
    .align 32
N:      .quad 0
A:      .quad 0          
B:      .quad 0
C:      .quad 0
ts_start: .skip 16
ts_end:   .skip 16

    .section .text
    .global main
    .extern malloc, free, printf, clock_gettime, getenv, atoi

main:
    push rbp
    mov rbp, rsp
    sub rsp, 48

    # 1. Get MATRIX_SIZE
    lea rdi, [str_matrix_size]
    call getenv
    test rax, rax
    jz .default_size
    mov rdi, rax
    call atoi
    mov [N], rax
    jmp .alloc_arrays

.default_size:
    mov qword ptr [N], 256

.alloc_arrays:
    mov rax, [N]
    imul rax, [N]
    shl rax, 3      # bytes = N*N*8
    mov rbx, rax

    mov rdi, rbx; call malloc; mov [A], rax
    mov rdi, rbx; call malloc; mov [B], rax
    mov rdi, rbx; call malloc; mov [C], rax

    # 2. Initialize Arrays
    # Standard logic to setup values
    mov rdi, [A]
    mov rsi, [B]
    mov r8, [C]
    
    mov rcx, [N]
    imul rcx, [N]
    
    movsd xmm2, [val_1_0]
    movsd xmm3, [val_0_01]
    pxor xmm4, xmm4
    
.init_loop:
    test rcx, rcx
    jz .init_done
    
    # Calc (Total - rcx) % 100 manually
    # Or just simple logic: we cheat slightly on init time optimization 
    # to focus on Matrix Mul optimization. Using Div is fine here.
    
    mov rax, [N]
    imul rax, [N]
    sub rax, rcx    # Current index i
    
    xor rdx, rdx
    mov r11, 100
    div r11
    
    cvtsi2sd xmm0, rdx
    mulsd xmm0, xmm3
    
    # A
    movsd xmm1, xmm2
    addsd xmm1, xmm0
    movsd [rdi], xmm1
    
    # B
    movsd xmm1, xmm2
    subsd xmm1, xmm0
    movsd [rsi], xmm1
    
    # C
    movsd [r8], xmm4
    
    add rdi, 8
    add rsi, 8
    add r8, 8
    dec rcx
    jmp .init_loop

.init_done:

    # 3. Start Timer
    mov rdi, 1
    lea rsi, [ts_start]
    call clock_gettime

    # ==========================================
    # 4. Matrix Multiplication (SIMD + UNROLL)
    # ==========================================
    # Logic: C[i][j] += A[i][k] * B[k][j]
    
    mov r8, [N]     # N
    shl r8, 3       # Row stride (bytes)
    
    mov r9, [A]     # ptr_A_row
    mov r10, [C]    # ptr_C_row
    
    xor r11, r11    # i = 0
    
.loop_i:
    cmp r11, [N]
    jge .done_mul
    
    xor r12, r12    # k = 0
    mov r13, [B]    # ptr_B_row (starts at B[0][0])
    
.loop_k:
    cmp r12, [N]
    jge .next_i
    
    # Load scalar A[i][k] and broadcast to both doubles in xmm0
    # movddup requires SSE3
    movddup xmm0, [r9 + r12*8] 
    
    # Inner loop j
    # We unroll by 8 doubles (64 bytes)
    # This requires N to be divisible by 8 (256 is fine)
    
    mov rcx, 0      # j
    mov rax, [N]    # Limit
    
    mov rbx, r13    # ptr_B_curr
    mov rdx, r10    # ptr_C_curr
    
.loop_j:
    cmp rcx, rax
    jge .next_k
    
    # --- UNROLLED BLOCK (Process 8 doubles) ---
    # We use xmm1-xmm4 for B, xmm5-xmm8 for C
    
    # Load 8 doubles from B (4 registers * 2 doubles)
    movups xmm1, [rbx]
    movups xmm2, [rbx + 16]
    movups xmm3, [rbx + 32]
    movups xmm4, [rbx + 48]
    
    # Multiply by broadcasted A[i][k] (xmm0)
    mulpd xmm1, xmm0
    mulpd xmm2, xmm0
    mulpd xmm3, xmm0
    mulpd xmm4, xmm0
    
    # Load 8 doubles from C
    movups xmm5, [rdx]
    movups xmm6, [rdx + 16]
    movups xmm7, [rdx + 32]
    movups xmm8, [rdx + 48]
    
    # Accumulate
    addpd xmm5, xmm1
    addpd xmm6, xmm2
    addpd xmm7, xmm3
    addpd xmm8, xmm4
    
    # Store back to C
    movups [rdx], xmm5
    movups [rdx + 16], xmm6
    movups [rdx + 32], xmm7
    movups [rdx + 48], xmm8
    
    # Pointer bump (8 doubles * 8 bytes = 64 bytes)
    add rbx, 64
    add rdx, 64
    add rcx, 8
    jmp .loop_j

.next_k:
    add r13, r8          # Move ptr_B to next row
    inc r12              # k++
    jmp .loop_k

.next_i:
    add r9, r8           # Move ptr_A to next row
    add r10, r8          # Move ptr_C to next row
    inc r11              # i++
    jmp .loop_i

.done_mul:

    # 5. End Timer
    mov rdi, 1
    lea rsi, [ts_end]
    call clock_gettime
    
    # Calc Time
    mov rax, [ts_end]
    sub rax, [ts_start]
    cvtsi2sd xmm0, rax
    mulsd xmm0, [val_1000]
    
    mov rax, [ts_end + 8]
    sub rax, [ts_start + 8]
    cvtsi2sd xmm2, rax
    divsd xmm2, [val_1M]
    addsd xmm0, xmm2
    movsd [rsp], xmm0 

    # 6. Print
    lea rdi, [str_output_header]
    mov rsi, [N]
    mov rdx, [N]
    xor rax, rax
    call printf

    mov rdi, [C]
    movsd xmm0, [rdi]
    lea rdi, [str_output_res]
    mov rax, 1     
    call printf
    
    lea rdi, [str_output_time]
    movsd xmm0, [rsp]
    mov rax, 1
    call printf

    # Cleanup
    mov rdi, [A]; call free
    mov rdi, [B]; call free
    mov rdi, [C]; call free

    add rsp, 48
    pop rbp
    xor rax, rax
    ret
