program factorial_float
    implicit none
    integer :: i, count, stat_val
    ! Selected real kind for at least 33 digits of precision (Quad/128-bit)
    integer, parameter :: qp = selected_real_kind(33, 4931)
    real(kind=qp) :: factorial
    integer(kind=8) :: start_time, end_time, clock_rate
    real(kind=8) :: time_ms
    character(len=100) :: count_env

    call get_environment_variable("COUNT", count_env, status=stat_val)
    if (stat_val == 0) then
        read(count_env, *) count
    else
        count = 170
    end if

    factorial = 1.0_qp

    call system_clock(start_time, clock_rate)
    do i = 1, count
        factorial = factorial * real(i, qp)
    end do
    call system_clock(end_time)

    time_ms = real(end_time - start_time, 8) * 1000.0_8 / real(clock_rate, 8)

    print '("Result(", I0, "!): ", ES24.14)', count, factorial
    ! Force fixed point output for small timings
    print '("Time: ", F0.6, " ms")', time_ms

end program factorial_float
