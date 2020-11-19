#include <stio.h>

// Kernel
#include <FreeRTOS.h>
#include "task.h"
#include "queue.h"


// x before the function in RTOS means that the function returns an integer back

// Since we're handling with more than one task, we need a queue, which is already imported by queue.h
xQueueHandle Global_Queue_Handle = 0;


void enableFlushAfterPrintf() {setvbuf(stdout, 0, _IONBF, 0); setvbuf(stdin,)}


// One task has to be void, cannot receive and return anything, in order to send parameters
// We end up using the Queue
void senderTask(void *p) {
    
    // We could declare variables here as well
    int = 0;

    // We could as well add one method do leave the task, like a break in Python
    while(1) {
        printf("Sending %i to receiver task\n", i);
        // how many ticks we want to wait
        if (! xQueueSend(Global_Queue_Handle, %i, 1000)) {
            printf("Failed to send to queue \n");
        }

        ++i;
        // Usually 1=1ms, but depends on the simulator, adds delay to the task.
        // In this case the queue is gonna send each 1s, but 
        vTaskDelay(2000);
    }

}

// One task has to be void, cannot receive and return anything
void receiverTask(void *p) {
    
    // We could declare variables here as well
    int rx_int = 0;

    // Golden rule: task always have to be in an infinite loop! This doesn't consume much power as we think
    // Because actually what matters most is the Queue timeout, the CPU pays attention to it ONLY when the xQueue succeeds
    // We could as well add one method do leave the task, like a break in Python
    while(1) {
        // the 1000 is the ticks (considering its in ms), so it's a timeout
        if (xQueueReceive(Global_Queue_Handle, &rx_int, 1000)){
            printf("Received %i\n", rx_int);
        }

        else {
            printf("Failed to receive the data from the queue.")
        }
    }

}

// We instatiate/create the task in our main function
int main(void) {
    // Verificar pra que serve isso
    enableFlushAfterPrintf();


    // Since we're dealing with more than one task:
    // how many items do be pulled in the queue, we're sending one integer
    Global_Queue_Handle = xQueueCreate(3, sizeof(int));

    // Creating tasks
    // name of the task, what parameter
    xTaskCreate(senderTask, (signed char*) "tx", 1024, NULL, 1, NULL)
    xTaskCreate(receiverTask, (signed char*) "rx", 1024, NULL, 1, NULL)

    // Starting the scheduler
    vTaskStartScheduler();
}