with open('delta.txt', 'r') as f_all_inter:
    with open('delta_intra.txt', 'r') as f_intra:
        force_convert = set(f_all_inter).difference(f_intra)
force_convert.discard('\n')
force_list = list(force_convert)

force_list.sort(key=lambda a_line: int(a_line.split()[0]))


with open('delta_inter.txt', 'w') as file_out:
    for line in force_list:
        file_out.write(line)