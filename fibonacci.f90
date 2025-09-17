program fibonacci
    implicit none
    integer :: i, n
    integer(kind=8) :: a, b, temp
    character(len=10) :: count_str

    call get_environment_variable("COUNT", count_str)
    if (len_trim(count_str) > 0) then
        read(count_str, *) n
    else
        n = 10
    end if

    print *, "Fibonacci Sequence (first ", n, " numbers):"

    a = 0
    b = 1
    do i = 1, n
        write(*, '(I0, A)', advance='no') a, ' '
        temp = a
        a = b
        b = temp + b
    end do
    print *
    
end program fibonacci
