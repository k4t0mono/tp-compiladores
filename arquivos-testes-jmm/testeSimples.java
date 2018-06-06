package import; // erro aqui
import java.lang.Integer;
import java.lang.System;

public class Series extends { // erro aqui
    public static int ARITHMETIC = 1;
    public static int GEOMETRIC = 2;
    private int a; // first term
    private int d; // common sum or multiple
    private int n; // number of terms
    public Series() {
        this(1, 1, 10);
    }
    public Series(int a, int d,) { // erro aqui
        this(a) = a;
        this(d) = d;
        this(n) = n;
    }
    public int computeSum(int kind) {
        int sum = a, t = a, i = n;
        while (i-- > 1) {
            if (kind == ARITHMETIC) {
                t += d;
            } else if (kind == GEOMETRIC) {
                t = t * d;
            }
            sum += t;
        }
        return sum;
    }
    public static void main(String[] args) {
        int a = Integer.parseInt(args[0]);
        int d = Integer.parseInt(args[1]);
        int n = Integer.parseInt(args[2]);
        Series s = new Series(a, d, n);
        System.out.println("Arithmetic sum = "
        + s.computeSum(Series.ARITHMETIC));
        System.out.println("Geometric sum = "
        + s.computeSum(Series.GEOMETRIC));
    }
    public int computeSum(int kind) {
        int sum = a, t = a, i = n;
        while (i > 1) {
            if (kind == ARITHMETIC) {
                t =+= d; //erro aqui
            } else if (kind == GEOMETRIC) {
                t = t * d *; // erro aqui
            }
            sum += t++; // erro aqui
        }
        sum //erro aqui
    }
    public a static void main(String[] args) { //erro aqui
        int a = Integer.parseInt(args[]); //erro aqui
        int d = Integer.parseInt(args[1]);
        int n = Integer.parseInt(args[2]);
        Series s = new Series(a, d, n);
        System.out.println("Arithmetic sum = "
        + s.computeSum(Series.ARITHMETIC));
        System.out.println("Geometric sum = "
        + s.computeSum(Series.GEOMETRIC));
    }
//erro aqui
