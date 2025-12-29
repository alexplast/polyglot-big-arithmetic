program power_float
    implicit none
    integer :: exp_val, stat_val
    ! Reverted to standard 64-bit float
    real(kind=8) :: base_val, result
    integer(kind=8) :: start_time, end_time, clock_rate
    real(kind=8) :: time_ms
    character(len=100) :: base_env, exp_env

    call get_environment_variable("BASE", base_env, status=stat_val)
    if (stat_val == 0) then
        read(base_env, *) base_val
    else
        base_val = 2.0_8
    end if

    call get_environment_variable("EXP", exp_env, status=stat_val)
    if (stat_val == 0) then
        read(exp_env, *) exp_val
    else
        exp_val = 1023
    end if

    call system_clock(start_time, clock_rate)
    result = base_val ** exp_val
    call system_clock(end_time)

    time_ms = real(end_time - start_time, 8) * 1000.0_8 / real(clock_rate, 8)

    print '("Result(", F0.2, "^", I0, "): ", ES20.10)', base_val, exp_val, result
    print '("Time: ", F0.6, " ms")', time_ms

end program power_float
