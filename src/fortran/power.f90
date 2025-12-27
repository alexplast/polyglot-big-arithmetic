program power_calc
    implicit none
    integer(kind=8), allocatable :: base_digits(:), result_digits(:)
    integer :: base_val, exp_val, stat_val, n_base, n_result
    integer(kind=8) :: start_time, end_time, clock_rate
    integer(kind=8), parameter :: BASE_CONST = 1000000000_8
    character(len=100) :: base_env, exp_env

    call get_environment_variable("BASE", base_env, status=stat_val)
    if (stat_val == 0) then
        read(base_env, *) base_val
    else
        base_val = 2
    end if

    call get_environment_variable("EXP", exp_env, status=stat_val)
    if (stat_val == 0) then
        read(exp_env, *) exp_val
    else
        exp_val = 1000
    end if

    allocate(result_digits(100000))
    result_digits = 0
    result_digits(1) = 1
    n_result = 1

    allocate(base_digits(100000))
    base_digits = 0
    call int_to_digits(base_val, base_digits, n_base)

    call system_clock(start_time, clock_rate)
    call binary_exp(base_digits, n_base, exp_val, result_digits, n_result)
    call system_clock(end_time)

    write(*, '("Result(", I0, "^", I0, "): ")', advance='no') base_val, exp_val
    call print_bigint(result_digits, n_result)
    print '("Time: ", F0.3, " ms")', real(end_time - start_time) * 1000.0 / real(clock_rate)

contains

    subroutine int_to_digits(n, digits, n_digits)
        integer, intent(in) :: n
        integer(kind=8), intent(inout) :: digits(:)
        integer, intent(out) :: n_digits
        integer(kind=8) :: temp_n

        temp_n = int(n, 8)
        n_digits = 0
        if (temp_n == 0) then
            n_digits = 1
            digits(1) = 0
            return
        end if
        
        do while (temp_n > 0)
            n_digits = n_digits + 1
            digits(n_digits) = mod(temp_n, BASE_CONST)
            temp_n = temp_n / BASE_CONST
        end do
    end subroutine

    subroutine bigint_multiply(a, n_a, b, n_b, c, n_c)
        integer(kind=8), intent(in) :: a(:), b(:)
        integer, intent(in) :: n_a, n_b
        integer(kind=8), intent(inout) :: c(:)
        integer, intent(out) :: n_c
        integer(kind=8) :: carry, current
        integer :: i, j, max_len

        max_len = n_a + n_b
        ! Reset target area manually instead of whole array for speed
        c(1:max_len+1) = 0

        do i = 1, n_a
            carry = 0
            do j = 1, n_b
                current = c(i + j - 1) + a(i) * b(j) + carry
                c(i + j - 1) = mod(current, BASE_CONST)
                carry = current / BASE_CONST
            end do
            j = n_b + 1
            do while (carry > 0)
                current = c(i + j - 1) + carry
                c(i + j - 1) = mod(current, BASE_CONST)
                carry = current / BASE_CONST
                j = j + 1
            end do
        end do

        n_c = max_len
        do while (n_c > 1 .and. c(n_c) == 0)
            n_c = n_c - 1
        end do
    end subroutine

    subroutine binary_exp(base, n_base, exp, result, n_result)
        integer(kind=8), intent(inout) :: base(:), result(:)
        integer, intent(inout) :: n_base, n_result
        integer, intent(in) :: exp
        integer :: e
        integer(kind=8), allocatable :: temp_result(:), temp_base(:)
        integer :: n_temp_res, n_temp_base

        allocate(temp_result(200000))
        allocate(temp_base(200000))

        e = exp
        do while (e > 0)
            if (mod(e, 2) == 1) then
                call bigint_multiply(result, n_result, base, n_base, temp_result, n_temp_res)
                n_result = n_temp_res
                result(1:n_result) = temp_result(1:n_result)
            end if
            call bigint_multiply(base, n_base, base, n_base, temp_base, n_temp_base)
            n_base = n_temp_base
            base(1:n_base) = temp_base(1:n_base)
            e = e / 2
        end do

        deallocate(temp_result)
        deallocate(temp_base)
    end subroutine

    subroutine print_bigint(digits, n_digits)
        integer(kind=8), intent(in) :: digits(:)
        integer, intent(in) :: n_digits
        integer :: j
        
        write(*, '(I0)', advance='no') digits(n_digits)
        do j = n_digits - 1, 1, -1
            write(*, '(I9.9)', advance='no') digits(j)
        end do
        print *
    end subroutine

end program power_calc
