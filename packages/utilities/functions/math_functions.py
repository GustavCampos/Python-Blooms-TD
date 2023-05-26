def bezier_curve(
    initial_point: tuple, 
    final_point: tuple, 
    curvature_point: tuple, 
    function_range: float
):
    x_axis = initial_point[0] * (1 - function_range)**2 + 2 * (1 - function_range) * function_range * curvature_point[0] + final_point[0] * function_range**2
    
    y_axis = initial_point[1] * (1 - function_range)**2 + 2 * (1 - function_range) * function_range * curvature_point[1] + final_point[1] * function_range ** 2   
    
    
    return x_axis, y_axis