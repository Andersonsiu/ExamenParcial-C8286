#EJERCICIO 1

1. python3 multi.py -n 1 -L a:30:200 
- La tarea tarda 30s en completarse, se divide en 3 partes 0-9 , 10-19 , 20-29


2. python3 multi.py -r 1 -L a:30:200 -M 300 -c 
- El trabajo finaliza en 30s con dos CPUS en este caso, CPU0 utiliza 100 y CPU1 uiliza 0 en ambos se calienta 0.00


3. python3 multi.py -r 1 -T a:30:200 -M 300 -c
- Al ejecutar con -T el tiempo de finalizacion es 100s, en donde se divide en 10 partes, 
la segunda columan disminuye del 39-30 , 69-60, 39-30, 19-10, 49-40, 19-10 hasta asi llegar al ultimo 9-0


4. python3 multi.py -r 1 -C a:30:200 -M 300 -c
- En este caso se divide en 10 partes donde en la primera parte del 0-9 se encuentra el w en el numero "9" y mientras va avanzando va aumentando las w que quiere decir que se esta calentando poco a poco.

