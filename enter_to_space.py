if __name__ == '__main__':
    file = open('poj.txt', 'r')
    args = ' '.join([line.strip('\n') for line in file])
    print args