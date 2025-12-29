program factorial_float
    implicit none
    integer :: i, count, stat_val
    ! Reverted to standard 64-bit float (double precision) for fair comparison
    real(kind=8) :: factorial
    integer(kind=8) :: start_time, end_time, clock_rate
    real(kind=8) :: time_ms
    character(len=100) :: count_env

    call get_environment_variable("COUNT", count_env, status=stat_val)
    if (stat_val == 0) then
        read(count_env, *) count
    else
        count = 170
    end if

    factorial = 1.0_8

    call system_clock(start_time, clock_rate)
    do i = 1, count
        factorial = factorial * real(i, 8)
    end do
    call system_clock(end_time)

    time_ms = real(end_time - start_time, 8) * 1000.0_8 / real(clock_rate, 8)

    print '("Result(", I0, "!): ", ES20.10)', count, factorial
    print '("Time: ", F0.6, " ms")', time_ms

end program factorial_float
