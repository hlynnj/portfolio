import re
def increment_time(filepath, dt):
    with open(filepath) as f:
        lines = [line.rstrip() for line in f]

    new_lines = []
    for line in lines:
        time, lane, instrument = re.split(';', line)
        new_time = float(time) + dt
        new_lines.append(str(new_time)+';'+lane+';'+instrument+'\n')
    
    return new_lines

new_lines = increment_time('./data/audio/Waltz/Waltz_map.txt', 1.8)
print(new_lines)

with open('./data/audio/Waltz/Waltz_map_new.txt', 'w') as f:
    for line in new_lines:
        f.write(line)