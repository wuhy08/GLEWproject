# using Base.Collections

# using DataStructures
using GeometricalPredicates
using AutoHashEquals

using Base.Collections


# Plant

function bicycle_plant(td, x0, y0, psi0, v0, n, b, a, lr)
    x, y, psi, v = zeros(n), zeros(n), zeros(n), zeros(n)

    x[1]   = x0   + v0*cos(psi0 + b[1])*td
    y[1]   = y0   + v0*sin(psi0 + b[1])*td
    psi[1] = psi0 + (v0/lr)*sin(b[1])*td
    v[1]   = v0   + a[1]*td

    for i = 1:n-1
        x[i+1]   = x[i]   + v[i]*cos(psi[i] + b[i+1])*td
        y[i+1]   = y[i]   + v[i]*sin(psi[i] + b[i+1])*td
        psi[i+1] = psi[i] + (v[i]/lr)*sin(b[i+1])*td
        v[i+1]   = v[i]   + a[i+1]*td
    end

    return x, y, psi, v
end


# A* Planner

immutable PlainPoint
    x::Int64
    y::Int64
end


function ==(p1::PlainPoint, p2::PlainPoint)
    return p1.x == p2.x && p1.y == p2.y
end


function Base.hash(p1::PlainPoint)
    h = Base.hash(p1.x)
    return Base.hash(p1.y, h)
end


immutable Node
    parent
    action
    state
    step_cost::Float64
    cumulative_cost::Float64
end


immutable Obstacle
    start_x
    end_x
    start_y
    end_y
end


immutable Edge
    start_node::Node
    end_node::Node
end


function get_actions(node::Node)
    if node != nothing && node.action != nothing
        if node.parent != nothing
            return push!(get_actions(node.parent), node.action)
        else
            return PlainPoint[node.action]
        end
    else
        return PlainPoint[]
    end
end


function is_legal(width, height, obstacles::Vector{Obstacle}, point::PlainPoint)
    # TODO: Remove this safety distance.

    # safety spacing
    spacing = 4
    if point.x < 1 || point.x >= width
        return false
    end

    if point.y < 1 || point.y >= height
        return false
    end

    for obstacle in obstacles
        if ((point.x >= obstacle.start_x - spacing && point.x <= obstacle.end_x + spacing)
            && (point.y >= obstacle.start_y - spacing && point.y <= obstacle.end_y + spacing))
            return false
        end
    end

    return true
end


function add_successor_if_possible!(width::Int64, height::Int64,
                                    successor_states::Vector{PlainPoint},
                                    actions::Vector{PlainPoint},
                                    costs::Vector{Float64},
                                    obstacles::Vector{Obstacle},
                                    point::PlainPoint, step_cost::Float64)
    if is_legal(width, height, obstacles, point)
        push!(successor_states, point)
        push!(actions, point)
        push!(costs, step_cost)
    end
end


# Returns the surrounding possible 8 squares
function point_successor(obstacles::Vector{Obstacle}, width, height, current_point::PlainPoint)
    successor_states = PlainPoint[]
#     actions = String[]
    actions = PlainPoint[]
    costs = Float64[]

    add_succ = (p, step_cost) -> add_successor_if_possible!(width, height,
                                                            successor_states, actions,
                                                            costs, obstacles,
                                                            p, step_cost)

    # Up, Down, Left, Right
    add_succ(PlainPoint(current_point.x, current_point.y - 1), 1.0)
    add_succ(PlainPoint(current_point.x - 1, current_point.y), 1.0)
    add_succ(PlainPoint(current_point.x + 1, current_point.y), 1.0)
    add_succ(PlainPoint(current_point.x, current_point.y + 1), 1.0)

    # Four corners
    add_succ(PlainPoint(current_point.x - 1, current_point.y + 1), 1.25)
    add_succ(PlainPoint(current_point.x + 1, current_point.y + 1), 1.25)
    add_succ(PlainPoint(current_point.x - 1, current_point.y - 1), 1.25)
    add_succ(PlainPoint(current_point.x + 1, current_point.y - 1), 1.25)

    return successor_states, actions, costs
end


function simple_node_eval(goal_point::PlainPoint, node::Node)
    return node.cumulative_cost + sqrt((node.state.x - goal_point.x)^2 + (node.state.y - goal_point.y)^2)
end


function construct_node(parent, action, state, step_cost)
    if parent != nothing
        return Node(parent, action, state, step_cost, step_cost + parent.cumulative_cost)
    else
        return Node(parent, action, state, step_cost, step_cost)
    end
end


# TODO: Make fringe universal instead of PriorityQueue
function universal_search(goal_f, successor_f, eval_f, start_node,
                          fringe, closed)
    println("SDFSDFSDFSD");
    enqueue!(fringe, start_node, eval_f(start_node))

    while !isempty(fringe)
        node = dequeue!(fringe)

        current_state = node.state

        if goal_f(current_state)
            return get_actions(node)
        end

        if !(current_state in closed)
            push!(closed, current_state)

            ss, as, cs = successor_f(current_state)

#             println(ss)

            for (successor_state, action, step_cost) in zip(ss, as, cs)
                new_node = construct_node(node, action, successor_state, step_cost)
                enqueue!(fringe, new_node, eval_f(new_node))
            end
        end
    end

    return []
end



# function pp_to_points!(mm, pps)
#     for pp in pps
#         mm[pp.x, pp.y] = 1
#     end
# end

function goal_function(point)
    function f(p)
        # check to see if the last location is the same
        return p.x == point.x && p.y == point.y
    end
    return f
end


# Convert the discrete points into the middle of the squares
function convert_to_continuous(square_dimension, points::Vector{PlainPoint})
    f = p -> (p.x*square_dimension + square_dimension/2.0,
              p.y*square_dimension + square_dimension/2.0)
    return map(f, points)
end
