#include <string>
#include <iostream>

using namespace std;

int num = 0;

void f(int l[], int size, int n, string curr) {
    if (n == size) {
       num++;
       cout << curr << endl;
       return;
    }

    string prevcurr = curr;
    for (int i = 0; i < size; ++i) {
        curr += to_string(i+1);
        f(l, size, n+1, curr);
        curr = prevcurr;
    }
}

int main() {
    int list[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    f(list, 9, 0, "");
}
