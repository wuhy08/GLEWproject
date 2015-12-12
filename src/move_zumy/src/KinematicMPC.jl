using Ipopt
using JuMP


# Internal MPC solver model optimized for speed with JuMP.
type InternalMPCModel
    n_horizon
    td
    ts
    lr
    model
    a
    b
    x
    y
    psi
    v
    linear_constraints
    nl_p
    x_ref
    y_ref
    psi_ref
    v_ref
    a_change_min
    a_change_max
    b_change_min
    b_change_max
    a_min
    a_max
    b_min
    b_max
end

solver = IpoptSolver(print_level=0)


function generate_initial_model(n, td, ts, lr)
    b_min        = -deg2rad(37)
    b_max        = -b_min
    a_min        = -1.5
    a_max        = 1
    a_change_min = -3
    a_change_max = 1.5
    b_change_min = -deg2rad(10)
    b_change_max = -b_change_min

    model = Model(solver=solver)
    @defVar(model, x[1:n])
    @defVar(model, y[1:n])
    @defVar(model, psi[1:n])
    @defVar(model, v[1:n])
    @defVar(model, b_min <= b[1:n] <= b_max)
    @defVar(model, a_min <= a[1:n] <= a_max)

    a_curr   = 0.0
    b_curr   = 0.0
    x_curr   = 0.0
    y_curr   = 0.0
    psi_curr = 0.0
    v_curr   = 0.0

    # Initial condition constraints
    @addConstraint(model, a_min_con, (a[1] >= a_change_min*ts + a_curr))
    @addConstraint(model, a_max_con, (a[1] <= a_change_max*ts + a_curr))
    @addConstraint(model, b_min_con, (b[1] >= b_change_min*ts + b_curr))
    @addConstraint(model, b_max_con, (b[1] <= b_change_max*ts + b_curr))

    linear_constraints = [a_min_con, a_max_con, b_min_con, b_max_con]

    # nonlinear constraints pointers
    nl_p = [x_curr, y_curr, psi_curr, v_curr]

    @addNLConstraint(model, x[1]   == nl_p[1] + nl_p[4]*cos(nl_p[3] + b[1])*td)
    @addNLConstraint(model, y[1]   == nl_p[2] + nl_p[4]*sin(nl_p[3] + b[1])*td)
    @addNLConstraint(model, psi[1] == nl_p[3] + (nl_p[4]/lr)*sin(b[1])*td)
    @addNLConstraint(model, v[1]   == nl_p[4] + a[1]*td)

    # Rest of constraints
    for i = 1:n-1
        @addConstraint(model, a_change_min <= (a[i+1] - a[i])/td <= a_change_max)
        @addConstraint(model, b_change_min <= (b[i+1] - b[i])/td <= b_change_max)
    end

    for i = 1:n-1
        @addNLConstraint(model, x[i+1]   == x[i] + v[i]*cos(psi[i] + b[i+1])*td)
        @addNLConstraint(model, y[i+1]   == y[i] + v[i]*sin(psi[i] + b[i+1])*td)
        @addNLConstraint(model, psi[i+1] == psi[i] + (v[i]/lr)*sin(b[i+1])*td)
        @addNLConstraint(model, v[i+1]   == v[i] + a[i+1]*td)
    end


    x_ref, y_ref, psi_ref, v_ref = zeros(n), zeros(n), zeros(n), zeros(n)

    # Q matrix
    q1 = 10 # w_x
    q2 = 10 # w_y
    q3 = 1  # w_psi
    q4 = 0  # w_v

    # R matrix
    r1 = 100  # w_beta
    r2 = 50   # w_a

    # R_ matrix
    r1_ = 1000 # w_beta_rate
    r2_ = 10   # w_a_rate

    # Note: We have to do setNLObjective() until https://github.com/JuliaOpt/JuMP.jl/issues/472 is resolved
    # Since we are doing setNLObjective, we should change the reference and not reset the objective!
    @setNLObjective(model, Min,
                    sum{q1*(x[i]-x_ref[i])^2 + q2*(y[i] - y_ref[i])^2
                    + q3*(psi[i] - psi_ref[i])^2 + q4*(v[i] - v_ref[i])^2,
                    i=1:n}
                    + sum{r1*(b[i]^2) + r2*(a[i])^2, i=1:n}
                    + sum{r1_*(b[i+1]-b[i])^2 + r2_*(b[i+1] - b[i])^2, i=1:n-1})

    solve(model)
    return InternalMPCModel(n, td, ts, lr, model, a, b, x, y, psi, v,
                            linear_constraints, nl_p, x_ref, y_ref, psi_ref, v_ref,
                            a_change_min, a_change_max, b_change_min, b_change_max,
                            a_min, a_max, b_min, b_max)
end


function fast_mpc_controller!(x_curr, y_curr, psi_curr, v_curr, a_curr, b_curr,
                              x_ref, y_ref, psi_ref, v_ref, mpc_model::InternalMPCModel)

    # Initial condition constraints
    chgConstrRHS(mpc_model.linear_constraints[1], mpc_model.a_change_min*ts + a_curr)
    chgConstrRHS(mpc_model.linear_constraints[2], mpc_model.a_change_max*ts + a_curr)
    chgConstrRHS(mpc_model.linear_constraints[3], mpc_model.b_change_min*ts + b_curr)
    chgConstrRHS(mpc_model.linear_constraints[4], mpc_model.b_change_max*ts + b_curr)

    mpc_model.nl_p[1] = x_curr
    mpc_model.nl_p[2] = y_curr
    mpc_model.nl_p[3] = psi_curr
    mpc_model.nl_p[4] = v_curr

    for i = 1:mpc_model.n_horizon
        mpc_model.x_ref[i]   = x_ref[i]
        mpc_model.y_ref[i]   = y_ref[i]
        mpc_model.psi_ref[i] = psi_ref[i]
        mpc_model.v_ref[i]   = v_ref[i]
    end

    solve(mpc_model.model)
    return getValue(mpc_model.a), getValue(mpc_model.b)
end
