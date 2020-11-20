# RTOS on Linux
Tested on Ubuntu 18.04. 

POSIX: Portable Operating System Interface for Unix WAS basically a set of measures to ease the pain of development and usage of different flavours of UNIX by having a (mostly) common API and utilities.

## Installation
Follow thoroughly the [*Building the Posix/Linux Simulator Demo*](https://www.freertos.org/FreeRTOS-simulator-for-Linux.html) section, installing the dependencies etc.

I had to downgrade some packages from Ubuntu, but that is quite particular to the flavour you're using.

## Running
Access the ```FreeRTOS/Demo/Posix_GCC/main.c``` file and change **only** line 74 from: 

```C
#define    BLINKY_DEMO       0
#define    FULL_DEMO         1
#define    ECHO_CLIENT_DEMO  2

#define mainSELECTED_APPLICATION FULL_DEMO
```

to

```C
#define mainSELECTED_APPLICATION BLINKY_DEMO
```

And then on the same directory:

``` $ make ```

To run the ```main_blinky.c```:

``` $ ./build/posix_demo ```

