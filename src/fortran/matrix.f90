program matrix_mult
    implicit none
    integer :: n, i, j, k, stat_val
    real(kind=8), allocatable :: a(:), b(:), c(:)
    real(kind=8) :: r
    integer(kind=8) :: start_time, end_time, clock_rate
    character(len=100) :: n_env

    call get_environment_variable("MATRIX_SIZE", n_env, status=stat_val)
    if (stat_val == 0) then
        read(n_env, *) n
    else
        n = 256
    end if

    allocate(a(n*n))
    allocate(b(n*n))
    allocate(c(n*n))
    c = 0.0d0

    do i = 1, n*n
        a(i) = 1.0d0 + dble(mod(i-1, 100)) * 0.01d0
        b(i) = 1.0d0 - dble(mod(i-1, 100)) * 0.01d0
    end do

    call system_clock(start_time, clock_rate)

    ! Naive implementation to test raw loops, not BLAS
    ! Note: Fortran is Column-Major, but we used 1D logic similar to C
    do i = 1, n
        do k = 1, n
             r = a((i-1)*n + k)
             do j = 1, n
                 c((i-1)*n + j) = c((i-1)*n + j) + r * b((k-1)*n + j)
             end do
        end do
    end do

    call system_clock(end_time)

    print '("Matrix(", I0, "x", I0, ")")', n, n
    print '("Result[0]: ", F0.4)', c(1)
    print '("Time: ", F0.3, " ms")', real(end_time - start_time) * 1000.0 / real(clock_rate)
end program matrix_mult
