import pickle
import math

X_OFFSET = 0
Y_OFFSET = 0

# assuming camera is mounted towards the jagged windows, looking towards Room 510N
#(0,0) corresponds to nao (4500,3000) - edge of field closest to door
#(450, 0) corresponds to nao (0, 3000) - edge of field adjacent to door but closer to camera
#(0, 600) corresponds to nao (4500, -3000) - edge of field adjacent to door but closer to offices
#(450, 600) corresponds to (0, -3000) - THE EDGE THAT'S LEFT
def convertNX(x):
    return int((4500 - float(x)) / 10) + X_OFFSET

def convertNY(y):
    return int((3000 - float(y)) / 10) + Y_OFFSET

def convertNHeading(heading):
    return float(heading) * math.pi / 180 + math.pi

def process_line(line, time_difference):
    # nao heading is in degrees
    # nao heading variance is in radians^2
    split_list = line.split('|')
    nao_log = {'Time': int(float(split_list[0]) - time_difference), 'Xpos': convertNX(split_list[2]), 'Xvar': float(split_list[4])/100, \
    'Ypos': convertNY(split_list[6]), 'Yvar': float(split_list[8])/100, \
    'HeadingNao': convertNHeading(split_list[10]), "HNaovar": float(split_list[12]), 'Balls': [], 'LPost': [], 'RPost': [], 'HPost': [], 'APost': [], \
    'HLPost': [], 'HRPost': [], 'ALPost': [], 'ARPost': [], 'NPost': [], 'Centre': [], 'Penalty': []}
    for i in range(13, len(split_list), 2):
        if split_list[i] == "":
            break
        nao_log[split_list[i]].append(split_list[i + 1])
    return nao_log

if __name__ == "__main__":
    #freya time is 72279ms ahead
    #yoda time is 10850ms behind
    nao_lines = [process_line(line.rstrip('\n'), -10850) for line in open('nao_log.txt')]
    # for line in nao_lines:
    #     print line
    pickled_log_file = open('log_file.txt')
    log_file_array = pickle.load(pickled_log_file)
    print log_file_array;
    # for line in log_file_array:
    #     print line

    i = 0
    j = 0

    matched_list = []

    while(1):
        # print "i = " + str(i);
        # print "j = " + str(j);
        eps = 50
        if i >= len(nao_lines) or j >= len(log_file_array):
            break
        nao_time = nao_lines[i]['Time']
        log_time = int(log_file_array[j]['Time'])

        # print "nao_time: " + str(nao_time)
        # print "log_time: " + str(log_time)
        if nao_time < log_time - eps:
            i += 1
        elif nao_time > log_time + eps:
            matched_list.append(dict(log_file_array[j]))
            j += 1
        else:
            matched_dictionary = nao_lines[i].copy()
            for key in log_file_array[j]:
                if key == 'Time':
                    continue
                matched_dictionary[key] = log_file_array[j][key]
            matched_list.append(matched_dictionary)
            i += 1
            j += 1

    matched_log_file = open('matched_log_file.txt', 'w')
    pickle.dump(matched_list, matched_log_file)

    for line in matched_list:
        print line

    matched_percentage = len(matched_list) / float(min(len(nao_lines), len(log_file_array)))
    print "matched_percentage: " + str(matched_percentage * 100)
