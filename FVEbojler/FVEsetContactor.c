/*
 *  FVEsetContactor.c
 *       gcc -lwiringPi -o FVEsetContactor FVEsetContactor.c
 */

#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct params
{
	int port;
    char* operation;
    int pinstatus;
	int state;        /**< Stavovy kod programu, odpovida vyctu tstates. */
} TParams;

TParams processParams(int argc, char **argv);


int PINTOSET;

/*
 * Call PINPORTMAP with PORT=n
 * when PORT should is expected to be 4, then PIN is on PINPORTMAP[4]
 * on PIN 4 there is DHT11 temperature sensor connected. 
*/
int PINPORTMAP[8] = {15,18,19,22,21,24,23,26};

int main( int argc, char *argv[] )
{
    
    
    TParams params = processParams(argc,argv);
    
    if ( params.state != EXIT_SUCCESS ){
        exit(EXIT_FAILURE);
    }
    if ( wiringPiSetup() == -1 )
        exit( 1 );
    fprintf(stdout,"PORT: %d\n", params.port);
    fprintf(stdout,"PIN: %d\n", PINPORTMAP[params.port]);
    fprintf(stdout,"OPER: %s\n", params.operation);
    fprintf(stdout,"PINSTATUS: %d\n", params.pinstatus);
    
    
    pinMode(PINPORTMAP[params.port], OUTPUT);
    digitalWrite(PINPORTMAP[params.port], params.pinstatus);
    
    return(0);
}


TParams processParams(int argc, char **argv){
    
    TParams result = {        // inicializace struktury
		.port = 0,
		.operation = "off",
        .pinstatus = LOW,
		.state = EXIT_SUCCESS,
	};
    
    if (argc == 2 && strcmp (argv[1],"-h") == 0) 
    {
        printf("%s","print_help\n");
        exit(0);
    }
    else if (argc == 2 && strcmp (argv[1],"--help") == 0) 
    {
        printf("%s","print_help\n");
        exit(0);
    }
    else if (argc >= 4)
    {
       fprintf(stderr, "Error, only 2 params are allowed!\n"); 
       result.state = EXIT_FAILURE;
    }
    else if ( argc == 3 )
    {
        if((result.operation = (char*) malloc(strlen(argv[2])*sizeof(char))) == NULL)
		{
			exit(1);
		}
        
        result.port = *argv[1] - 48;
        strcpy(result.operation, argv[2]);
        if ( strcmp("off",result.operation) == 0 )result.pinstatus = LOW ;
        else if ( strcmp("on",result.operation) == 0 ) result.pinstatus = HIGH ;
        else {
            result.state = EXIT_FAILURE;
            fprintf(stderr,"Wrong action passed\n");
            return result;
        }
        
        result.state = EXIT_SUCCESS;
    }
    else {
        result.state = EXIT_FAILURE;
        fprintf(stderr, "None or only one parametr passed!\n"); 
    }
    
    return result;
}

