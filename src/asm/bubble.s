    .intel_syntax noprefix
    .section .note.GNU-stack,"",@progbits

    .section .rodata
str_sort_size:   .string "SORT_SIZE"
str_output_head: .string "Sort(%d): "
str_val_fmt:     .string "%.4f "
str_dots:        .string "... "
str_newline:     .string "\n"
str_time:        .string "Time: %.3f ms\n"

val_LCG_mul: .quad 1664525
val_LCG_add: .quad 1013904223
val_LCG_mod: .double 4294967296.0
val_1000:    .double 1000.0
val_1M:      .double 1000000.0

    .section .bss
    .align 32
N:      .quad 0
arr:    .quad 0
ts_start: .skip 16
ts_end:   .skip 16

    .section .text
    .global main
    .extern malloc, free, printf, clock_gettime, getenv, atoi

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
    shl rdi, 3      # N * 8 bytes
    call malloc
    mov [arr], rax

    # 2. LCG Generation
    # seed (rax) = 42
    # ptr (rdi) = arr
    # i (rcx) = 0 to N
    
    mov rdi, [arr]
    mov rcx, 0
    mov rax, 42     # seed
    mov r8, [val_LCG_mul]
    mov r9, [val_LCG_add]
    movsd xmm1, [val_LCG_mod]

.gen_loop:
    cmp rcx, [N]
    jge .gen_done
    
    # seed = seed * mul + add
    imul eax, r8d   # eax * mul
    add eax, r9d    # + add
    
    # Convert unsigned int to double
    mov ebx, eax    # zero extend to rbx
    cvtsi2sd xmm0, rbx
    divsd xmm0, xmm1 # / 2^32
    
    movsd [rdi + rcx*8], xmm0
    
    inc rcx
    jmp .gen_loop

.gen_done:

    # 3. Start Timer
    mov rdi, 1
    lea rsi, [ts_start]
    call clock_gettime

    # 4. Bubble Sort
    # i in r8, j in r9
    # limit_i = N - 1
    # limit_j = N - i - 1
    # ptr = [arr]
    
    mov r10, [arr]  # Base pointer
    
    mov r8, 0       # i = 0
    mov r11, [N]
    dec r11         # N - 1

.outer_loop:
    cmp r8, r11
    jge .sort_done
    
    mov r9, 0       # j = 0
    mov r12, [N]
    sub r12, r8     # N - i
    dec r12         # N - i - 1
    
.inner_loop:
    cmp r9, r12
    jge .next_outer
    
    # Compare arr[j] and arr[j+1]
    # Address: r10 + j*8
    movsd xmm0, [r10 + r9*8]     # arr[j]
    movsd xmm1, [r10 + r9*8 + 8] # arr[j+1]
    
    comisd xmm0, xmm1
    jbe .no_swap    # if arr[j] <= arr[j+1] skip
    
    # Swap
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
    movsd [rsp], xmm0   # save time

    # 6. Print
    lea rdi, [str_output_head]
    mov rsi, [N]
    xor rax, rax
    call printf
    
    # First 5
    mov rcx, 0
    mov rbx, [arr]
.p_loop1:
    cmp rcx, 5
    jge .p_mid
    movsd xmm0, [rbx + rcx*8]
    lea rdi, [str_val_fmt]
    mov rax, 1
    push rcx # save registers used by loop
    push rbx
    call printf
    pop rbx
    pop rcx
    inc rcx
    jmp .p_loop1

.p_mid:
    lea rdi, [str_dots]
    xor rax, rax
    call printf
    
    # Last 5 (N-5 to N)
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
