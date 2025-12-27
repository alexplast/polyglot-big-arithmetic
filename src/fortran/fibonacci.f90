program fibonacci
    implicit none
    integer, allocatable :: digits_a(:), digits_b(:), temp(:), temp_resize(:)
    integer :: i, j, count, stat_val, n_a, n_b, n_temp, max_digits
    integer :: carry, sum_val
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
    digits_a(1) = 0
    digits_b(1) = 1
    n_a = 1
    n_b = 1

    do i = 1, count
        if (max(n_a, n_b) + 1 > max_digits) then
             allocate(temp_resize(max_digits * 2))
             temp_resize = 0
             ! resize all? Just digits_a, digits_b, temp
             ! For brevity, let's just make it huge enough for common counts
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
            sum_val = digits_b(j) + temp(j) + carry
            digits_b(j) = mod(sum_val, 10)
            carry = sum_val / 10
        end do
        n_b = max(n_b, n_temp)
        if (carry > 0) then
            n_b = n_b + 1
            digits_b(n_b) = carry
        end if
    end do

    write(*, '("Result(F_", I0, "): ")', advance='no') count
    do j = n_a, 1, -1
        write(*, '(I1)', advance='no') digits_a(j)
    end do
    print *

    deallocate(digits_a)
    deallocate(digits_b)
    deallocate(temp)
end program fibonacci
