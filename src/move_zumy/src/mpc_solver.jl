#!/usr/bin/env julia

using RobotOS

@rosimport move_zumy.srv: MPCSolver

rostypegen()
using move_zumy.srv

using JuMP
using Ipopt


function mpc_cb(req::MPCSolverRequest)
# function mpc_cb(x0, y0, theta0, x_ref, y_ref, theta_ref)

    println("Starting MPC Solver!!!")

    N = 8;

    delta_t = 0.10;

    mpc = Model(solver=IpoptSolver(print_level=0));

    x_rate = 5;
    y_rate = 5;
    theta_rate = 5;


    # State variables
    @defVar(mpc, x[1:N])
    @defVar(mpc, y[1:N])
    @defVar(mpc, theta[1:N])

    # Control variables
    @defVar(mpc, v_tr[1:N-1])
    @defVar(mpc, v_rt[1:N-1])


    for i = 1:N-1
        @addNLConstraint(mpc, x[i+1] == x[i] + v_tr[i]*cos(theta[i])*delta_t)
        @addNLConstraint(mpc, y[i+1] == y[i] + v_tr[i]*sin(theta[i])*delta_t)
        @addNLConstraint(mpc, theta[i+1] == theta[i] + v_rt[i]*delta_t)
    end


    for i = 1:N-2
        @addNLConstraint(mpc, -x_rate <= x[i+1] - x[i] <= x_rate)
        @addNLConstraint(mpc, -x_rate <= x[i+1] - x[i] <= x_rate)

        @addNLConstraint(mpc, -y_rate <= y[i+1] - y[i] <= y_rate)
        @addNLConstraint(mpc, -y_rate <= y[i+1] - y[i] <= y_rate)

        @addNLConstraint(mpc, -theta_rate <= theta[i+1] - theta[i] <= theta_rate)
        @addNLConstraint(mpc, -theta_rate <= theta[i+1] - theta[i] <= theta_rate)
    end

    x0 = req.x0;
    y0 = req.y0;
    theta0 = req.theta0;

    x_ref = req.goal_x;
    y_ref = req.goal_y;
    theta_ref = req.goal_theta;


    @addNLConstraint(mpc, x[1] == x0)
    @addNLConstraint(mpc, y[1] == y0)
    @addNLConstraint(mpc, theta[1] == theta0)


    @setNLObjective(mpc, Min, sum{(x[i]-x_ref)^2 + (y[i] - y_ref)^2 + (theta[i] - theta_ref)^2, i=1:N-2}
                    + sum{v_tr[i]^2 + v_rt[i]^2, i=1:N-1})

    status = solve(mpc)

    v_tr_vals = getValue(v_tr[1:N-1])
    v_rt_vals = getValue(v_rt[1:N-1])

    # return v_tr_vals[1], v_rt_vals[1];

    resp = MPCSolverResponse();

    resp.v_tr = v_tr_vals[1];
    resp.v_rt = v_rt_vals[1];

    return resp;
end

init_node("mpc_solver")
# const srvcall = ServiceProxy("callme", Empty)
srvlisten = Service("mpc_solver", MPCSolver, mpc_cb)
println("Created MPC Solver!!!")
spin()
