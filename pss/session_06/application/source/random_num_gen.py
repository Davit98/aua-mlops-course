import argparse
import numpy as np


def generate_random_number(a=1, b=10):
    return np.random.randint(low=a, high=b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random number generator",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--a", required=False, type=int,
                        help="The left endpoint of the interval.")
    parser.add_argument("--b", required=False, type=int,
                        help="The right endpoint of the interval.")
    
    args = parser.parse_args()
    
    a, b = args.a, args.b
    randint = generate_random_number(a, b)
    print(f"My random number is: {randint}")
     