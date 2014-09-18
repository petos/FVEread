/*
 *  FVEsetContactor.c
 *       gcc -lwiringPi -o FVEsetContactor FVEsetContactor.c
 */

//~ #include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int PINTOSET;

/*
 * Call PINPORTMAP with PORT=n
 * when PORT should is expected to be 4, then PIN is on PINPORTMAP[4]
 * on PIN 4 there is DHT11 temperature sensor connected. 
*/
int PINPORTMAP[8] = {15,18,19,22,21,24,23,26};

int main( void )
{
    //~ if ( wiringPiSetup() == -1 )
        //~ exit( 1 );
    for (int i=0; i<10; i++) {
        printf("%d\n", PINPORTMAP[i]);
    }
    return(0);
}
