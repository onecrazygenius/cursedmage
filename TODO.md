# For Final
1. ~~Implement Bosses~~
   1. Add boss sprite
   2. Add boss door sprite
   3. Better Place Boss Room (Probably blocked by dungeon paths)
   4. [Optional] - Add more bosses, maybe even for different difficulties
2. Implement card upgrade after boss
3. Implement Shield Cards
4. Implement new card effects
5. Random dungeon paths
6. See hand & deck from combat screen
7. Tutorial
8. Animation
9. Re-implement automated testing


# Bugs
1. When you load a game and are on the room select screen. If you don't click on a door the game crashes
   1. This **DOES NOT** happen when you make a new game
2. When there are 2 enemies, if the left most enemy is dead, the top text will still says "X's Turn" where X is the leftmost enemy
3. AI Logic breaks when they have a heal card. It displayes the 'Out of Mana' popup and gets stuck in an infinite loop
   1. _James suspects this is something to do with how the card is played rather than the logic itself_
4. After completing a room and going back to the room select screen. If you quit and load the room you just completed needs finishing again
   1. _The fix for this is almost definitely just changing the save order_

