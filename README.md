# Asynchronous Point Of Sale System Project<br> (revising stage)
In this python project I was given the *inventory* module (containing the *Inventory* class) and simple version of the *main* module. The *Inventory* class contains several asynchronous methods, so the *asyncio* module is needed. In those methods, an ```async.sleep()``` instruction has been included deliberately to slow down their execution and use asynchronous programming.
<br>

My program works well, just perhaps not fast enough because I don't know where to insert ```task = async.create_task()```  and ```await task``` statements, since the original async methods are embedded deep into the final functions (most of them in the *operations* module). Any tips concerning this regard will be greatly appreciated. Please comment! :blush:
