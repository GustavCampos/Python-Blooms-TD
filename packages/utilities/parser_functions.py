import re as regex
import packages.utilities.way_point as waypoint
from packages.utilities.math_functions import bezier_curve

def get_wave_list_from_file(file_path) -> list[str]:
    lines = open(file_path, "r").readlines()
    
    return_list = []
    
    for line in lines:
        wave_blooms_list = parse_bloom_wave(line)
        
        return_list.append(wave_blooms_list)
        
    return return_list
        

def parse_bloom_wave(wave_line: str) -> list:
    wave_list = []
    
    pattern = r"(?<=wave{)[\w+:\d+:\d+,*]+(?=})"
    
    matched_string = regex.search(pattern, wave_line).group()
    
    blooms_to_make = matched_string.split(',')
    
    for bloom in blooms_to_make:
        values = bloom.split(":")
        
        dict_to_append = {
            "bloom": values[0],
            "quantity": values[1],
            "framerate": values[2],
        }
        
        wave_list.append(dict_to_append)
    
    return wave_list
    
def get_waypoints_list(file_path) -> list[dict]:
    lines = open(file_path, "r").readlines()
    
    pattern = r"(?<=[wrg]p\={)((\d+\.*\d*),?(\d+\.*\d*))(?=})"
    
    wp_list = []
    rp_list = []
    gp_list = []
    return_list = []
    
    for line in lines:
        matched_string = regex.search(pattern, line).group()
        
        if (line.startswith("gp")):
            gp_list.append(int(matched_string))
        else:
            values = matched_string.split(',')
            values = float(values[0]), float(values[-1])
            
            if (line.startswith("wp")):
                wp_list.append(waypoint.WayPoint(values[0], values[-1]))
            elif (line.startswith("rp")):
                rp_list.append(waypoint.ReferenceWayPoint(values[0], values[-1]))
            else:
                raise ValueError("Given string has not 'wp', 'rp' or 'gp' at start")    
                
        
    for index in range(len(wp_list)):
        return_list.append(wp_list[index])
        
        if (index == len(wp_list) - 1):
            break
        
        range_part = (1 / (gp_list[index] + 1))
        range_point = 0
        for _ in range(gp_list[index]):
            range_point += range_part
            
            generated_xy = bezier_curve(
                (wp_list[index].x, wp_list[index].y), 
                (wp_list[index + 1].x, wp_list[index + 1].y), 
                (rp_list[index].x, rp_list[index].y), 
                range_point
            )
            
            return_list.append(waypoint.GeneratedWayPoint(generated_xy[0], generated_xy[-1]))

        
    return return_list