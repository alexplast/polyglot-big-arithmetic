program factorial
    implicit none
    integer, allocatable :: digits(:), temp_digits(:)
    integer :: i, j, count, stat_val, n_digits, max_digits
    integer(kind=8) :: carry, current
    integer(kind=8) :: start_time, end_time, clock_rate
    character(len=100) :: count_env

    call get_environment_variable("COUNT", count_env, status=stat_val)
    if (stat_val == 0) then
        read(count_env, *) count
    else
        count = 200
    end if

    max_digits = 10000
    allocate(digits(max_digits))
    digits = 0
    digits(1) = 1
    n_digits = 1

    call system_clock(start_time, clock_rate)
    do i = 2, count
        carry = 0
        do j = 1, n_digits
            current = int(digits(j), 8) * i + carry
            digits(j) = mod(current, 10_8)
            carry = current / 10
        end do
        do while (carry > 0)
            n_digits = n_digits + 1
            if (n_digits > max_digits) then
                ! Double the capacity
                allocate(temp_digits(max_digits * 2))
                temp_digits(1:max_digits) = digits
                temp_digits(max_digits+1:) = 0
                call move_alloc(temp_digits, digits)
                max_digits = max_digits * 2
            end if
            digits(n_digits) = mod(carry, 10_8)
            carry = carry / 10
        end do
    end do
    call system_clock(end_time)

    write(*, '("Result(", I0, "!): ")', advance='no') count
    do j = n_digits, 1, -1
        write(*, '(I1)', advance='no') digits(j)
    end do
    print *
    print '("Time: ", F0.3, " ms")', real(end_time - start_time) * 1000.0 / real(clock_rate)

end program factorial
