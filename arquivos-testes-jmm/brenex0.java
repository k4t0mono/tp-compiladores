
public abstract class Aluno { // idEscopo 1
    private int a;
    public void foo() { // idEscopo = 2
        int a = 0;
        if(a > 0) { // idEscopo = 3
            int x = 1;
        }
        if(a <= 0) { // idEscopo = 4
            int x = 2 - 4;
            boolean c = a > 23 * 7;
            if(c) {
                int x = 10;
                x = 11;
            }
        }
    }

    public void foo2() { // idEscopo = 5
        a = 0;
        if(2 <= 0) { // idEscopo = 6
            a = 2;
        }
        if(2 > 0) { // idEscopo = 7

        }
    }
    
    public static void main() { // idEscopo = 8
        int x = 3 * 4 +  5 * 7 + 3 ;
        // x = 5;
        // int a = x + 3;
    }
}