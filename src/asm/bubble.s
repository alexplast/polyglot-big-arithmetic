    .intel_syntax noprefix

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
    push rbp
    mov rbp, rsp
    sub rsp, 48

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
    movsd [rsp], xmm0

    # 6. Print
    lea rdi, [str_output_head]
    mov rsi, [N]
    xor rax, rax
    call printf
    
    mov rcx, 0
    mov rbx, [arr]
    mov r12, 5
    cmp r12, [N]
    cmovg r12, [N]
.p_loop1:
    cmp rcx, r12
    jge .p_mid
    movsd xmm0, [rbx + rcx*8]
    lea rdi, [str_val_fmt]
    mov rax, 1
    push rcx
    push rbx
    push r12
    call printf
    pop r12
    pop rbx
    pop rcx
    inc rcx
    jmp .p_loop1
.p_mid:
    lea rdi, [str_dots]
    xor rax, rax
    call printf
    mov r12, [N]
    cmp r12, 5
    jle .p_end
    mov rcx, [N]
    sub rcx, 5
    mov rbx, [arr]
.p_loop2:
    cmp rcx, [N]
    jge .p_end
    movsd xmm0, [rbx + rcx*8]
    lea rdi, [str_val_fmt]
    mov rax, 1
    push rcx
    push rbx
    call printf
    pop rbx
    pop rcx
    inc rcx
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
    add rsp, 48
    pop rbp
    xor rax, rax
    ret
