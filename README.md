# Elevator Simulator using asyncio

## Requirements

Python 3.5 or above

## Usage

Running command ```python elevator/simulator.py``` will start 
the simulator with default settings. Settings can also be specified 
via command line options, see ```python elevator/simulator.py --help``` 
for details. 

Simulator will print its status on the standard output:

```
Welcome to Elevator Simulator
Floors:		      12
Height:		    2.65
Velocity:	     3.0
Doors delay:     3.0
Elevator controller server is listening on port 4455
2017-12-25 00:36:04.244681: Starting operations
2017-12-25 00:36:04.244732: Waiting on floor: 1. Turn lights OFF
```

From another terminal connect to the elevator controller with ```nc``` 
command like this: ```nc 127.0.0.1 4455``` It is possible to start 
multiple controlling sessions. Elevator controller will display a prompt 
and wait for user input:

```
$ nc 127.0.0.1 4455
Welcome to Elevator Controller
Enter a command ('help' for help): help
Commands are:
	help		prints this help message
	quit		disconnects from the server
	call <n>	simulates pressing the call button on the n-th floor
	go <n>		simulates pressing the n-th floor button in the cabin
Enter a command ('help' for help): 

``` 

Enter a few commands:

```
Welcome to Elevator Controller
Enter a command ('help' for help): call 1
Calling elevator to floor 1
Enter a command ('help' for help): go 5
Cabin button 5 is pressed
Enter a command ('help' for help): go 7    
Cabin button 7 is pressed
Enter a command ('help' for help): call 1
Calling elevator to floor 1
Enter a command ('help' for help): call 3
Calling elevator to floor 3
```

Elevator will respond in real time:

```
Welcome to Elevator Simulator
Floors:		      12
Height:		    2.65
Velocity:	     3.0
Doors delay:     3.0
Elevator controller server is listening on port 4455
2017-12-25 00:36:04.244681: Starting operations
2017-12-25 00:36:04.244732: Waiting on floor: 1. Turn lights OFF
2017-12-25 00:36:21.946042: Called from floor 1
2017-12-25 00:36:21.946177: Wake up. Turn lights ON
2017-12-25 00:36:21.946269: Opening doors
2017-12-25 00:36:23.809979: Cabin button 5 pressed
2017-12-25 00:36:24.947376: Closing doors
2017-12-25 00:36:24.947460: Moving up
2017-12-25 00:36:25.832726: Current floor is 2
2017-12-25 00:36:26.721611: Current floor is 3
2017-12-25 00:36:27.607225: Current floor is 4
2017-12-25 00:36:28.493567: Current floor is 5
2017-12-25 00:36:28.493624: Opening doors
2017-12-25 00:36:30.514166: Cabin button 7 pressed
2017-12-25 00:36:31.499272: Closing doors
2017-12-25 00:36:32.387941: Current floor is 6
2017-12-25 00:36:33.275335: Current floor is 7
2017-12-25 00:36:33.275391: Opening doors
2017-12-25 00:36:36.277074: Closing doors
2017-12-25 00:36:36.277146: Waiting on floor: 7. Turn lights OFF
2017-12-25 00:36:51.123926: Called from floor 1
2017-12-25 00:36:51.124050: Wake up. Turn lights ON
2017-12-25 00:36:51.124095: Moving down
2017-12-25 00:36:52.010974: Current floor is 6
2017-12-25 00:36:52.898232: Current floor is 5
2017-12-25 00:36:53.011718: Called from floor 3
2017-12-25 00:36:53.786204: Current floor is 4
2017-12-25 00:36:54.673947: Current floor is 3
2017-12-25 00:36:54.674002: Opening doors
2017-12-25 00:36:57.675658: Closing doors
2017-12-25 00:36:58.564595: Current floor is 2
2017-12-25 00:36:59.448693: Current floor is 1
2017-12-25 00:36:59.448742: Opening doors
2017-12-25 00:37:02.452141: Closing doors
2017-12-25 00:37:02.452226: Waiting on floor: 1. Turn lights OFF
```

Press Ctrl+C to stop the simulator


## Elevator algorithm

Elevator is a state machine that has two states:
  * `Idle`
  * `Active`
 
Initially elevator is in `Idle` state waiting for `command` event to be notified. 
  
There's a separate coroutine `Elevator.handle_commands` which handles user input 
 (obtained from `controller.command_queue`) and keeps track which buttons are pressed.
 
When user sends a command, `Elevator.handle_commands` will notify `command` event and
 elevator will wake up and enter the `Active` state.
 
 `Active` state has substates: 
    * `Active.moving_up`, 
    * `Active.moving_down`, 
    * `Active.open_doors` 
which are implemented as separate coroutines.

While moving up or down, user can press multiple buttons in the cabin and elevator
 will stop and open the doors once respective floor is reached. 
 
While moving down elevator will also stop and open doors as it reaches the floor 
if a call button is pressed on that floor.
 
Elevator will change moving direction only once it has reached its final destination in 
a particular direction.
 
Once there are no more commands to execute elevator will enter the `Idle` state.
 
 