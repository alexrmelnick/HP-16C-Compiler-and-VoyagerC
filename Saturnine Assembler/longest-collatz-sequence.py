def main():
    X = 1000000
    longest_chain_length = 0
    longest_chain_index = 1
    for i in range(1,X):
        temp = Collatz(i)
        if temp > longest_chain_length:
            longest_chain_length = temp
            longest_chain_index = i
    print(longest_chain_index, longest_chain_length)

def Collatz(num):
    length = 1
    while num != 1:
        if num%2 == 0:
            num = num/2
        else:
            num = 3*num+1
            length += 1
    return length

if __name__ == "__main__":
    main()