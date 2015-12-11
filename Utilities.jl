using Base.Collections


# Interpolate / Upsample from A* discrete path to MPC continuous path
function path_d2c(xs, ys, v_desired, n_horizon, td, current_x, current_y)
    distance_goal = v_desired * td * n_horizon
    # Find the points that we will cover in the path to match v_desired
    distance_elapsed = 0.0

#     current_x = xs[1]
#     current_y = ys[1]

    end_index = 1
    # first figure out how many of the A* steps are needed
    # Jason - why wouldn't the number of steps always be equal to the length of xs? doesn't A* stop at the goal?
    for i = 1:length(xs)
        x = xs[i]
        y = ys[i]
        dist = sqrt((current_x - x)^2.0 + (current_y - y)^2.0)
        distance_elapsed += dist
        if distance_elapsed > distance_goal
            end_index = i
            break
        end
        end_index = i
    end
#     println("end_index: ", end_index)
    xs_interpolated = Float64[]
    ys_interpolated = Float64[]

    # interpolate the current_x, current_y to the first A* point
    num_steps = (sqrt((xs[1] - current_x)^2.0 + (ys[1] - current_y)^2.0)/v_desired) / td
    x_slope = (xs[1] - current_x)/(num_steps)
    y_slope = (ys[1] - current_y)/(num_steps)

    for j = 1:round(num_steps)-1
        x_next = current_x + x_slope*j
        y_next = current_y + y_slope*j
        push!(xs_interpolated, x_next)
        push!(ys_interpolated, y_next)
    end

    # Then continue the rest of the interpolation
    for i = 1:end_index
        push!(xs_interpolated, xs[i])
        push!(ys_interpolated, ys[i])
        if i != end_index
            num_steps = (sqrt((xs[i+1] - xs[i])^2.0 + (ys[i+1] - ys[i])^2.0)/v_desired) / td
            x_slope = (xs[i+1] - xs[i])/(num_steps)
            y_slope = (ys[i+1] - ys[i])/(num_steps)

            for j = 1:round(num_steps)-1
                x_next = xs[i] + x_slope*j
                y_next = ys[i] + y_slope*j
                push!(xs_interpolated, x_next)
                push!(ys_interpolated, y_next)
            end
        end
    end

    # If we have fewer than n_horizon points, smear the last point, means we are at the goal, I (Kiet) think???
    if length(xs_interpolated) < n_horizon + 1
        n = (n_horizon + 1) - length(xs_interpolated)
        xs = xs_interpolated
        ys = ys_interpolated
        append!(xs, ones(n) * xs_interpolated[end])
        append!(ys, ones(n) * ys_interpolated[end])
    else
        xs = xs_interpolated[1:n_horizon+1]
        ys = ys_interpolated[1:n_horizon+1]
    end


    psi = [atan2(y_i_next - y_i, x_i_next - x_i) for (x_i_next, x_i, y_i_next, y_i) in zip(xs[2:end], xs,
                                                                                           ys[2:end], ys)]
    v   = [v_desired for i=1:length(xs)]
    return xs[1:end-1], ys[1:end-1], psi, v[1:end-1]
end
