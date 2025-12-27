program fibonacci
    implicit none
    ! Use 64-bit integers for storage
    integer(kind=8), allocatable :: digits_a(:), digits_b(:), temp(:), temp_resize(:)
    integer :: i, j, count, stat_val, n_a, n_b, n_temp, max_digits
    integer(kind=8) :: carry, sum_val, val_temp
    integer(kind=8) :: start_time, end_time, clock_rate
    integer(kind=8), parameter :: BASE = 1000000000_8
    character(len=100) :: count_env

    call get_environment_variable("COUNT", count_env, status=stat_val)
    if (stat_val == 0) then
        read(count_env, *) count
    else
        count = 10
    end if

    max_digits = 1000
    allocate(digits_a(max_digits))
    allocate(digits_b(max_digits))
    allocate(temp(max_digits))
    
    digits_a = 0
    digits_b = 0
    temp = 0       ! Initialize temp to zero
    digits_a(1) = 0
    digits_b(1) = 1
    n_a = 1
    n_b = 1

    call system_clock(start_time, clock_rate)
    do i = 1, count
        if (max(n_a, n_b) + 2 > max_digits) then
             allocate(temp_resize(max_digits * 2))
             temp_resize(1:max_digits) = digits_a
             temp_resize(max_digits+1:) = 0
             call move_alloc(temp_resize, digits_a)

             allocate(temp_resize(max_digits * 2))
             temp_resize(1:max_digits) = digits_b
             temp_resize(max_digits+1:) = 0
             call move_alloc(temp_resize, digits_b)

             allocate(temp_resize(max_digits * 2))
             temp_resize = 0
             call move_alloc(temp_resize, temp)

             max_digits = max_digits * 2
        end if

        ! temp = a
        temp(1:n_a) = digits_a(1:n_a)
        n_temp = n_a
        
        ! a = b
        digits_a(1:n_b) = digits_b(1:n_b)
        n_a = n_b
        
        ! b = b + temp
        carry = 0
        do j = 1, max(n_b, n_temp)
            ! Safe access: treat value as 0 if we are beyond temp's active length
            val_temp = 0
            if (j <= n_temp) val_temp = temp(j)
            
            sum_val = digits_b(j) + val_temp + carry
            digits_b(j) = mod(sum_val, BASE)
            carry = sum_val / BASE
        end do
        n_b = max(n_b, n_temp)
        if (carry > 0) then
            n_b = n_b + 1
            digits_b(n_b) = carry
        end if
    end do
    call system_clock(end_time)

    write(*, '("Result(F_", I0, "): ")', advance='no') count
    if (n_a == 1 .and. digits_a(1) == 0) then
        print '(I0)', 0
    else
        write(*, '(I0)', advance='no') digits_a(n_a)
        do j = n_a - 1, 1, -1
            write(*, '(I9.9)', advance='no') digits_a(j)
        end do
        print *
    end if
    
    print '("Time: ", F0.3, " ms")', real(end_time - start_time) * 1000.0 / real(clock_rate)

    deallocate(digits_a)
    deallocate(digits_b)
    deallocate(temp)
end program fibonacci
