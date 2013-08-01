genevo
======
Just in case you also found Convey's Game of Life too boring and static. Chaos rulez.
It's like Convey's Game but each cell has a 16 bit genome from which its attributes are derived.
That is, how long does the cell live, how hungry is it (how many other cells can be around it before is starves),
how likely is it to attack/mate with other cells.

It needs python3 and pygame to run.  
Run it with:  
  `git clone https://github.com/ponderstibbons/genevo genevo`  
  `cd genevo`  
  `./bin/genevo`  
  
That should open a window with lots of colorful squares in it.
The default view gives similar (in the genes) cell a similar color. That means cells with a similiar color are 
less likely to attack eachother and more likely to mate with eachother.
You can change the color coding by pressing 1 - 5, where each number has a different color coding:
  1. default as explained above
  2. the more red the cell is the more aggressive it is, if it is black you can poke with a stick and it will still like you
  3. the more blue it is the stronger the cell and is less likely to get killed when attacked or attacking
  4. the greener a cell the longer it has to live, that is black cell probably dies within the next few turns
  5. this is a bit special, the greyshade is again similar for similar cells, where ever a red square pops blinks a cell has been killed in combat and whereever a blue one blinks there was a mutation while mating
  
