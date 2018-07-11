public abstract class Aluno {
    private int a;
    private boolean b;
    public void foo() {
        b = a + 2;              //ERRO
        b = a > 'c';            //ERRO
        b = a;                  //ERRO
        char c = 2;             //ERRO
        a = 'c';                //ERRO
        if (a == true) {        //ERRO
            int var = 4;
            if ('c' && 'b') {   //ERRO
                b = a <= c;     //ERRO
            }
        }
        var = 5;                //ERRO

        r = 0;                  //ERRO
        int r;
    }
}