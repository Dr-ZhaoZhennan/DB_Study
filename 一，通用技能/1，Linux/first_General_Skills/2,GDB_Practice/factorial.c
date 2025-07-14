#include <stdio.h>

// 这是一个计算阶乘的函数
long long factorial(int n) {
    long long result = 1;
    for (int i = 0; i <= n; i++) { // 故意引入的 Bug：循环条件是 <= n
        result *= i;
    }
    return result;
}

int main() {
    int num;
    printf("请输入一个正整数来计算它的阶乘: ");
    scanf("%d", &num);

    if (num < 0) {
        printf("阶乘不支持负数。\n");
    } else {
        long long res = factorial(num);
        printf("%d 的阶乘是 %lld\n", num, res);
    }

    return 0;
}
