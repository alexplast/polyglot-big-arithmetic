program fibonacci_float
    implicit none
    integer :: i, k, count, stat_val
    real(kind=8) :: a, b, temp
    integer(kind=8) :: start_time, end_time, clock_rate
    real(kind=8) :: time_ms
    character(len=100) :: count_env

    call get_environment_variable("COUNT", count_env, status=stat_val)
    if (stat_val == 0) then
        read(count_env, *) count
    else
        count = 1475
    end if

    call system_clock(start_time, clock_rate)
    
    do k = 1, 200000
        a = 0.0_8
        b = 1.0_8
        do i = 1, count
            temp = a
            a = b
            b = temp + b
        end do
    end do
    
    call system_clock(end_time)

    time_ms = real(end_time - start_time, 8) * 1000.0_8 / real(clock_rate, 8)

    print *, "Result: ", a
    print '("Time: ", F0.3, " ms")', time_ms
end program fibonacci_float
