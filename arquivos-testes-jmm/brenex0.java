
public abstract class Aluno { // idEscopo 1
    public void foo() { // idEscopo = 2
        int a = 0;
        if( a > 0) { // idEscopo = 3
            int x = 1;
        }
        if(a <= 0) { // idEscopo = 4
            int x = 2;
        }
    }

    public void foo2() { // idEscopo = 5
        if(2 <= 0) { // idEscopo = 6
            a = 2;
        }
        if( 2 > 0) { // idEscopo = 7
            int x = 1;
        }
    }
    
    public static void main() { // idEscopo = 8
        // int x = 3 * 4 +  5 * 7 + 3 ;
        int x = 5;
        int a = x + 3;
    }
}