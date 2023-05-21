import re as regex
from packages.utilities.way_point import WayPoint
from math import sqrt

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
    
    pattern = r"(?<=[wr]p\={)((\d+\.*\d*),(\d+\.*\d*))(?=})"
    
    wp_list = []
    rp_list = []
    return_list = []
    
    for line in lines:
        matched_string = regex.search(pattern, line).group()
        values = matched_string.split(",")
        values = [float(values[0]),float(values[-1])] 
        
                
        if (line.startswith("wp")):
            wp_list.append(WayPoint(values[0], values[-1]))
        elif (line.startswith("rp")):
            rp_list.append(WayPoint(values[0], values[-1], True))
        else:
            raise ValueError("Given string has not 'wp' or 'rp' at start")
    
    for index in range(len(rp_list)):
        ip = wp_list[index]
        fp = wp_list[index + 1]
        rp = rp_list[index]
        
        length_fp_ip = sqrt(((fp.x - ip.x)**2) + ((fp.y - ip.y)**2))
        length_rp_ip = sqrt(((rp.x - ip.x)**2) + ((rp.y - ip.y)**2))
        length_rp_fp = sqrt(((rp.x - fp.x)**2) + ((rp.y - fp.y)**2))
        
        length = length_fp_ip - (length_rp_fp + length_rp_ip) / 2
        
        return_list.append({
            "ip": ip,
            "fp": fp,
            "rp": rp,
            "vm": length
        })
        
    return return_list