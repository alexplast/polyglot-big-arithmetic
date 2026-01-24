program bubble_sort
    implicit none
    integer :: n, i, j, stat_val
    real(kind=8), allocatable :: arr(:)
    real(kind=8) :: temp
    integer(kind=8) :: start_time, end_time, clock_rate
    character(len=100) :: n_env
    logical :: file_exists

    call get_environment_variable("SORT_SIZE", n_env, status=stat_val)
    if (stat_val == 0) then
        read(n_env, *) n
    else
        n = 10000
    end if

    allocate(arr(n))
    
    inquire(file="data.bin", exist=file_exists)
    if (.not. file_exists) then
        print *, "Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first."
        stop
    end if

    ! Read binary file using stream access (Fortran 2003+)
    open(10, file='data.bin', access='stream', status='old', form='unformatted')
    read(10) arr
    close(10)

    call system_clock(start_time, clock_rate)
    
    do i = 1, n - 1
        do j = 1, n - i
            if (arr(j) > arr(j+1)) then
                temp = arr(j)
                arr(j) = arr(j+1)
                arr(j+1) = temp
            end if
        end do
    end do

    call system_clock(end_time)

    write(*, '("Sort(", I0, "): ")', advance='no') n
    do i = 1, 5
        write(*, '(F0.4, " ")', advance='no') arr(i)
    end do
    write(*, '("... ")', advance='no')
    do i = n-4, n
        write(*, '(F0.4, " ")', advance='no') arr(i)
    end do
    print *
    
    print '("Time: ", F0.3, " ms")', real(end_time - start_time) * 1000.0 / real(clock_rate)
end program bubble_sort
