if __name__ == '__main__':
    s = 'babe'
    for i in range(1 << len(s)):
        print(''.join([
            s[x].upper() if (1 << x & i) else s[x]
            for x in range(len(s))
        ]))

