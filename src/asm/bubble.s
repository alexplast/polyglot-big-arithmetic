    .intel_syntax noprefix

    # Disable executable stack warning
    .section .note.GNU-stack,"",@progbits

    # Note: GNU-stack and Linux-specific sections will fail on macOS.
    # This source is kept for Linux/Docker runs.

    .section .rodata
str_sort_size:   .string "SORT_SIZE"
str_data_file:   .string "data.bin"
str_mode_rb:     .string "rb"
str_err_open:    .string "Error: data.bin not found\n"
str_output_head: .string "Sort(%d): "
str_val_fmt:     .string "%.4f "
str_dots:        .string "... "
str_newline:     .string "\n"
str_time:        .string "Time: %.3f ms\n"

val_1000:    .double 1000.0
val_1M:      .double 1000000.0

    .section .bss
    .align 32
N:      .quad 0
arr:    .quad 0
fp:     .quad 0
ts_start: .skip 16
ts_end:   .skip 16

    .section .text
    .global main
    .extern malloc, free, printf, clock_gettime, getenv, atoi, fopen, fread, fclose, puts, exit

main:
    # --- PROLOGUE & ABI COMPLIANCE ---
    # Stack checking: Entry RSP ends in 0x8 (return address pushed)
    push rbp        # RSP -> 0x0
    mov rbp, rsp
    
    # Save Callee-Saved Registers
    push rbx        # RSP -> 0x8
    push r12        # RSP -> 0x0
    push r13        # RSP -> 0x8  <-- New: Use R13 for loop counter
    
    # Align Stack to 16 bytes
    # Current RSP ends in 0x8. We need to subtract 8 to get to 0x0.
    sub rsp, 8      # RSP -> 0x0 (ALIGNED). We use this 8 bytes for double storage.

    # 1. Env SORT_SIZE
    lea rdi, [str_sort_size]
    call getenv
    test rax, rax
    jz .default_n
    mov rdi, rax
    call atoi
    mov [N], rax
    jmp .alloc
.default_n:
    mov qword ptr [N], 10000

.alloc:
    mov rdi, [N]
    shl rdi, 3
    call malloc
    mov [arr], rax

    # 2. Read data.bin
    lea rdi, [str_data_file]
    lea rsi, [str_mode_rb]
    call fopen
    test rax, rax
    jz .open_error
    mov [fp], rax

    mov rdi, [arr]
    mov rsi, 8
    mov rdx, [N]
    mov rcx, [fp]
    call fread
    
    mov rdi, [fp]
    call fclose
    jmp .start_bench

.open_error:
    lea rdi, [str_err_open]
    call puts
    mov rdi, 1
    call exit

.start_bench:
    # 3. Start Timer
    mov rdi, 1
    lea rsi, [ts_start]
    call clock_gettime

    # 4. Bubble Sort
    mov r10, [arr]
    mov r8, 0
    mov r11, [N]
    dec r11

.outer_loop:
    cmp r8, r11
    jge .sort_done
    mov r9, 0
    mov r12, [N]
    sub r12, r8
    dec r12
.inner_loop:
    cmp r9, r12
    jge .next_outer
    movsd xmm0, [r10 + r9*8]
    movsd xmm1, [r10 + r9*8 + 8]
    comisd xmm0, xmm1
    jbe .no_swap
    movsd [r10 + r9*8], xmm1
    movsd [r10 + r9*8 + 8], xmm0
.no_swap:
    inc r9
    jmp .inner_loop
.next_outer:
    inc r8
    jmp .outer_loop

.sort_done:
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
    movsd [rsp], xmm0  # Store time in stack scratch space

    # 6. Print
    lea rdi, [str_output_head]
    mov rsi, [N]
    xor rax, rax
    call printf
    
    # Use R13 as loop counter instead of RCX (RCX is volatile)
    mov r13, 0
    mov rbx, [arr]
    mov r12, 5
    cmp r12, [N]
    cmovg r12, [N]
.p_loop1:
    cmp r13, r12
    jge .p_mid
    movsd xmm0, [rbx + r13*8]
    lea rdi, [str_val_fmt]
    mov rax, 1
    # Stack is already aligned (rsp ends in 0). No pushes needed.
    call printf
    inc r13
    jmp .p_loop1
.p_mid:
    lea rdi, [str_dots]
    xor rax, rax
    call printf
    mov r12, [N]
    cmp r12, 5
    jle .p_end
    mov r13, [N]
    sub r13, 5
    mov rbx, [arr]
.p_loop2:
    cmp r13, [N]
    jge .p_end
    movsd xmm0, [rbx + r13*8]
    lea rdi, [str_val_fmt]
    mov rax, 1
    call printf
    inc r13
    jmp .p_loop2
.p_end:
    lea rdi, [str_newline]
    xor rax, rax
    call printf
    lea rdi, [str_time]
    movsd xmm0, [rsp]
    mov rax, 1
    call printf

    mov rdi, [arr]
    call free
    
    # --- EPILOGUE ---
    add rsp, 8
    pop r13
    pop r12
    pop rbx
    pop rbp
    xor rax, rax
    ret
