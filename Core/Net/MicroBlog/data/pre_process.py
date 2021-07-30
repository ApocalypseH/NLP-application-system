file_path = input()
with open(file_path, 'r', encoding = 'utf-8') as f:
    count = 0
    for line in f.readlines():
        count += 1
        line_list = line.strip().split('\t')
        if len(line_list) != 2:
            print('error!')
            print('line:' + str(count))
print('success!')