# Manual Test Plan

## Image Upload
- [ ] Load square image – should fit correctly.
- [ ] Load portrait image – should crop to square.
- [ ] Load landscape image – should crop to square.

## Tile Display
- [ ] Check that 15 tiles are visible and correctly spaced.
- [ ] Ensure bottom-right tile is empty.

## Tile Movement
- [ ] Click to move adjacent tile – should slide.
- [ ] Press arrow keys – empty tile should move.
- [ ] Cannot move non-adjacent tiles.

## Shuffling
- [ ] Every shuffle should be solvable.
- [ ] Game should not start in solved state.

## Win Condition
- [ ] Reassemble image to trigger win screen.
- [ ] Counter stops after win.
