
/* Standard includes. */
#include <stdio.h>
#include <conio.h>

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "timers.h"
#include "semphr.h"

/* Priorities at which the tasks are created. tskIDLE_PRIORITY is 0? */
#define mainQUEUE_RECEIVE_TASK_PRIORITY		( tskIDLE_PRIORITY + 2 )
#define	mainQUEUE_SEND_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 )

/* The rate at which data is sent to the queue.  The times are converted from
milliseconds to ticks using the pdMS_TO_TICKS() macro. */
#define mainTASK_SEND_FREQUENCY_MS			pdMS_TO_TICKS( 200UL )
#define mainTIMER_SEND_FREQUENCY_MS			pdMS_TO_TICKS( 2000UL )

/* The number of items the queue can hold at once. */
#define mainQUEUE_LENGTH					( 2 )

/* The values sent to the queue receive task from the queue send task and the
queue send software timer respectively. */
#define mainVALUE_SENT_FROM_TASK			( 100UL )
#define mainVALUE_SENT_FROM_TIMER			( 200UL )

// Tasks
static void receiverTask( void *pvParameters );
static void senderTask( void *pvParameters );

/* The queue used by both tasks. */
//static QueueHandle_t xQueue = NULL;
xQueueHandle GlobalQueueHandle = 0;


// Remembering the tasks should not return or accept any parameters, everything is done through the Queue!
static void senderTask( void *pvParameters )
{
	/*
	const uint32_t ulValueToSend = mainVALUE_SENT_FROM_TASK;*/


	int key = 0;
	int count = 0;

	// A principio run pode sair
	int run = 0;
	/* Prevent the compiler warning about the unused parameter. */
	( void ) pvParameters;/

	for( ;; )
	{
		// Enters the loop when any key from the keyboard is pressed
		if (!_kbhit())
		{
			// Retrieving WHICH key was pressed, getch() returns an int
			key = _getch();

			// 97 is "a", which is our input pin
			if (key == 97)
			{
				// 
				run = !run;
				/* Reset the software timer. */
				//xTimerReset(xTimer, portMAX_DELAY);
			}

			// 115 is "s", only when the key is pressed AND the run port is 1 that we output the commutating state to the exit pin
			// Commutation in this case is done by doing ++count
			else if ((key == 115) && (run == 1))
			{
				count = mainVALUE_SENT_FROM_TASK
				//count = count + 1;
			}
		}	
			
		/* Send to the queue - causing the queue receive task to unblock and
		write to the console.  0 is used as the block time so the send operation
		will not block - it shouldn't need to block as the queue should always
		have at least one space at this point in the code. */
		// In the end count is being send to the taskReceiver in order to be decreased there and therefore commutating the output pin
		xQueueSend( GlobalQueueHandle, &count, 0U );
	}
}

static void receiverTask( void *pvParameters )
{
	int rx_int;
	int i;

	/* Prevent the compiler warning about the unused parameter. */
	( void ) pvParameters;

	for(;;)
	{
		
		/* The last parameter is how many ticks we want to wait.  It will not use any CPU time while it is in the
		Blocked state. */
		xQueueReceive( xQueue, &rx_int, portMAX_DELAY );
		
		for (i= rx_int; i >= 0; i = i - 1)
		{
			printf("%i \n", i);
			vTaskDelay(200);
		}
		
		printf("%i \n", rx_int);
	}
}


// main_blinky
void main( void )
{

	/* Create the queue. */
	GlobalQueueHandle = xQueueCreate(mainQUEUE_LENGTH, sizeof(int) );

	if (GlobalQueueHandle != NULL)
	{
		/* Start the two tasks as described in the comments at the top of this
		file. */
		xTaskCreate( receiverTask, "Rx", configMINIMAL_STACK_SIZE, NULL, mainQUEUE_RECEIVE_TASK_PRIORITY, NULL );							

		xTaskCreate( senderTask, "TX", configMINIMAL_STACK_SIZE, NULL, mainQUEUE_SEND_TASK_PRIORITY, NULL );

		/* Start the tasks and timer running. */
		vTaskStartScheduler();
	}

	/* If all is well, the scheduler will now be running, and the following
	line will never be reached.  If the following line does execute, then
	there was insufficient FreeRTOS heap memory available for the idle and/or
	timer tasks	to be created.  See the memory management section on the
	FreeRTOS web site for more details. */
	for( ;; );
}



