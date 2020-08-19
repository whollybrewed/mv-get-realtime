import numpy as np
fr_now = 2
total_sad = 0

stat = []
with open('stat_intra.txt', 'w') as file_out:
    for line in open("delta_intra.txt", "r"):
        mv = line.split()
        fr = int(mv[0])
        if fr_now != fr:
            arr = np.array(stat) 
            line =  "fr=" + str(fr_now) + \
                    " mv=" + str(arr.size) + \
                    " mean=" + str(int(np.mean(arr))) + \
                    " med=" + str(int(np.median(arr))) + \
                    " 1q=" + str(int(np.percentile(arr, 25))) + \
                    " 3q=" + str(int(np.percentile(arr, 75))) + "\n"
            file_out.write(line)
            fr_now = fr
            stat[:] = []
            print('READING...' + str(fr_now), end="\r", flush=True)
        sad = int(mv[8])
        stat.append(sad)
    arr = np.array(stat)
    line =  "fr=" + str(fr_now) + \
            " mv=" + str(arr.size) + \
            " mean=" + str(int(np.mean(arr))) + \
            " med=" + str(int(np.median(arr))) + \
            " 1q=" + str(int(np.percentile(arr, 25))) + \
            " 3q=" + str(int(np.percentile(arr, 75))) + "\n"
    file_out.write(line)
    file_out.close()
