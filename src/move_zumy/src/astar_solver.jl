#!/usr/bin/env julia

using RobotOS
using Base.Collections
# using DataStructures

@rosimport geometry_msgs.msg.Pose2D
@rosimport move_zumy.srv: AStarSolver

rostypegen()

using move_zumy.srv
using geometry_msgs.msg

include("./GraphPlanner.jl")
include("./Utilities.jl")


second = xs -> xs[2];

square_dimension = 3.0; # Discretization amount
num_tiles = 4;
tile_size = 30; # 30cm square tiles
width = Integer(round((num_tiles*tile_size) / square_dimension)); # Number of squares
height = Integer(round((num_tiles*tile_size) / square_dimension)); # Number of squares

println("width: $(width)");
println("height: $(height)");

# height = 120;

zumy_width = 4;
zumy_height = 4;

td = 4.0;
n_horizon = 350;
v_desired = 2.0;

normalized_to_cm = 120;

function astar_cb(req::AStarSolverRequest)

    println("SDFDSFSDGSDGSFGFGFGDFGDFGDFGDFGDFGDFGFDGFDGFDGDFGDFGDFGFDGDFGDFGDFGDFGFDGDF");

    println("Starting A* Solver!!!!")
    println("start x: $(req.zumy_start.x), start y: $(req.zumy_start.y), start theta: $(req.zumy_start.theta)")
    println("goal x: $(req.zumy_goal.x), goal y: $(req.zumy_goal.y), goal theta: $(req.zumy_goal.theta)")

    println(req.zumy_pos)

    start_point = PlainPoint(Integer(round((req.zumy_start.x*normalized_to_cm)/square_dimension)), Integer(round((req.zumy_start.y*normalized_to_cm)/square_dimension)));
    goal_point = PlainPoint(Integer(round((req.zumy_goal.x*normalized_to_cm)/square_dimension)), Integer(round((req.zumy_goal.y*normalized_to_cm)/square_dimension)));

    obstacles = Obstacle[]

    # for (zumy, i) in zip(req.zumy_pos, range(1, length(req.zumy_pos)))

    for zumy in req.zumy_pos
        println(zumy);
        start_x = (zumy.x*normalized_to_cm)/square_dimension - zumy_width/2;
        start_y = (zumy.y*normalized_to_cm)/square_dimension - zumy_width/2;
        end_x = (zumy.x*normalized_to_cm)/square_dimension + zumy_width/2;
        end_y = (zumy.y*normalized_to_cm)/square_dimension + zumy_width/2;
        ob = Obstacle(Integer(round(start_x)), Integer(round(end_x)), Integer(round(start_y)), Integer(round(end_y)));

        push!(obstacles, ob)
    end

    println("start_point: $(start_point), goal_point: $(goal_point), obstacles: $(obstacles)");

    node_eval = node -> simple_node_eval(goal_point, node);
    empty_q = PriorityQueue();
    start_node = construct_node(nothing, nothing, start_point, 0);

    successor_f = s -> point_successor(obstacles, width, height, s);

    res = universal_search(goal_function(goal_point), successor_f, node_eval, start_node, empty_q, Set{PlainPoint}());

    println(res);

    if length(res) > 0
        res_cont = convert_to_continuous(square_dimension, res);
        x_p, y_p = path_d2c(map(second, res_cont), map(first, res_cont), v_desired, n_horizon, 
                            td, start_point.y*square_dimension + square_dimension/2, 
                            start_point.x*square_dimension + square_dimension/2); # Need to flip x and y!
        println("res_cont length: $(length(res_cont))");
        # println(x_p);
        # println(y_p);

        path = Pose2D[];

        # println(Pose2D(3.0, 4.0, 0.0));
        
        for (x, y) in zip(x_p, y_p)
            push!(path, Pose2D(y/(num_tiles*tile_size), x/(num_tiles*tile_size), 0.0)); # Flip x and y!
        end

        response = AStarSolverResponse();
        response.path = path;

        # println(path);

        return response;

        # println(Pose2D(x_p[1], y_p[1], 0.0));

        # return Pose2D(x_p[1], y_p[1], 0.0);
    end

    println("FAILEDDDD\n\n");

    return req.zumy_start;
end

init_node("astar_solver")
srvlisten = Service("astar_solver", AStarSolver, astar_cb)
println("Created A* Solver!!!!")
spin()
