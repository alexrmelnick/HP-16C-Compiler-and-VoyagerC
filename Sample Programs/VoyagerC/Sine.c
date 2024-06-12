// Manual calculation of sine wave values for hand compiling into keypress commands
// sin(x) = x^1/1! - x^3/3! + x^5/5! - x^7/7! + x^9/9! - x^11/11! + ...
// Term:    1       2        3        4         5        6
// n-th term = ((-1)^n) * (x^(2n+1)) / ((2n+1)!)
#include <stdio.h>

int factorial(int n) {
    int result = 1;
    for(int i = n; i > 0; i--) {
        result *= i;
    }

    return result;
}

float exp(float base, int power) {
    float result = 1;
    for(int i = power; i > 0; i--) {
        result *= base;
    }

    return result;
}

// Angle in radians
int main() {
    float angle = 1.8; // in Radians
    int terms = 5;

    float result = 0;

    for(int i = 0; i < terms; i++) {
        // n-th term = ((-1)^n) * (x^(2n+1)) / ((2n+1)!)
        result += (exp(-1,i)) * (exp(angle, (2*i+1))) / factorial((2*i+1));
    }

    printf("%f\n",result); // Print the result

    return 0;
}