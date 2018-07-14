def get_input():

    while True:
        try:
            n = int(input("Provide a first number between 1 and 10000: "))
            m = int(input("Provide a second number between 1 and 10000, higher than first: "))
        except ValueError:
            print("That is not the integer, try again!")
        if not (n in range(1, 10001) and m in range(1, 10001) and n < m):
            print("Incorrect value, try again!")
        else:
            break
    return n, m


def fizzbuzz(num_range):

    for num in num_range:

        if num % 3 == 0:
            if num % 5 == 0:
                yield "FizzBuzz"
            else:
                yield "Fizz"
        elif num % 5 == 0:
            yield "Buzz"
        else:
            yield num

n, m = get_input()
for i in fizzbuzz(range(n, m+1)):
    print(i)
