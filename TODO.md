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
1. Re-evaluate and fix enemy damage scaling
2. Loading the game seems to have worse performance than a new game
   1. _Check if multiple states are being drawn._
3. When you load game the escape button doesn't work
4. You cannot generate large dungeons (15+ Floors)

## Map Rework TODO:
1. We should be moving upwards not downwards
   3. Just invert the Y when drawing
2. Implement a score-like system
3. Decide what to do with victory screen.
   1. Probably change it to a "Score" screen showing the players score after they die