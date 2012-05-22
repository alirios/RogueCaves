RogueCaves - readme
===================

Current milestone: Athletic Alpaca
----------------------------------
Todo
----
* Extended cave generation (old bridges, rooms, etc).
* Accept unfinished A* paths.
* Audio.
* Let game run headless.
* Only let ALife clip if the two have active paths.
* Combine generate_room() and generate_cave_rooms()
* Add XP for weapons
* ALife should flee at some point during combat.
* Random quests
* Tricky ALife
* Helper functions to automatically sort incoming item lists
* Helper functions to create menus without altering the variables directly

Bugs
----
* ALife still occasionally teleports due to pathing errors.
* ALife continues to calculate paths that broke in the past.
* ALife adds broken paths to cache to prevent freezes.
* ALife sometimes spawns in walls
* Crash on line 179 of pathfinding.py.
* Roomgen can lead to impossible levels.
* Walls should be destroyable, either with a pickaxe or something else.
* Shop owner occasionally stops saying goodbye when you walk out the door. Requires restart.

Current Version: 05.21.2012A
----------------------------
Added
-----
* Added wheat
* life.add_item() and life.add_item() now set 'pos' key
* levelgen.add_item() no longer returns a pointer to the original item
* Levels now have a tick function that is called every second
* Crops can have different images for each stage of growth

Previous Version: 05.20.2012A
----------------------------
Added
-----
* Moved all event code for run_shop into the function of the same name
* Purchasing items no longer leaves a duplicate in the shop
* Shop owner now stores traded items in chests
* LevelGen: Walkers no longer travel to the edge of the map
* Fixed error in go_to() that caused it to never return if the destination had been reached
* Life: get_all_items_tagged()
* Life: put_all_items_tagged()
* Life: go_to_and_do()
* Life: run_shop()

Previous Version: 05.18.2012A
----------------------------
Added
-----
* ALife can claim buildings
* Messages when entering/leaving buildings
* Icons now listed next to items in inventory
* Extended menu system
* New item: Bronze
* Buying items now works

Previous Version: 05.17.2012A
----------------------------
Added
-----
* Items spawned in chests are no longer duplicated and placed outside of the chest
* Starting to add docstrings
* Life: in_building()
* Level: get_room_items()
* Menu system

Previous Version: 05.16.2012A
----------------------------
Added
-----
* Added 'delay' flag to tasks so ALife will rest between iterations
* PygCurse now checks to see if the tile being drawn was drawn in a previous frame
* Items are now automatically put into storage by levelgen
* Fixed crash that involved buildings being built too close together, blocking doors
* Crazy Miner should no longer get thirsty/hungry and raid the surface for food
* Doors no longer built on cornerstones
* ALife can remove items from storage
* ALife finds the closest object first when searching for something
* Pickaxes speed up mining

Previous Version: 05.15.2012A
----------------------------
Added
-----
* Removed stairs going upwards in the forest.
* Blood now fades even when outside of the player's view.
* Fixed crash relating to removal of the forest's "entrances" variable.

Previous Version: 05.03.2012A
----------------------------
Added
-----
* Timing is much more accurate now.
* "Sticky" movement fixed.
* max_fps is now set to 20 by default.

Previous Version: 04.24.2012A
----------------------------
Added
-----
* No longer checking large amounts rooms during generate_cave_rooms()
* Added "sharp" flag to weapons.

Previous Version: 04.23.2012A
----------------------------
Added
-----
* Fixed some dialog errors.
* Blood.
* Forgot to update readme with new changes.

Previous Version: 04.22.2012A
----------------------------
Added
-----
* ALife forgets about enemies after they're killed.
* Fixed some repeating dialog.
* ALife now takes into consideration a target's weapon.
* Weapons now have ranks and statuses.
* Game now goes into turn-based mode when danger arises.
* Fixed issue with idle ALife automatically traveling to the surface for food.

Previous Version: 04.21.2012A
----------------------------
Added
-----
* Added weapons.
* Added Crazy Miner.
* No longer real-time (for now).
* Fixed bug that prevented ALife from following targets between z-levels.

Previous Version: 04.12.2012A
----------------------------
Added
-----
* Fixed possible bug relating to A* cache returning paths for wrong z-level.
* Started room generation for caves.

Previous Version: 04.11.2012A
----------------------------
Added
-----
* Optimized draw_screen() for caves.
* ALife clips through fellow workers.
* Fixed additional pathing issues.
* Teleporting due to pathing conflicts fixed.

Previous Version: 04.09.2012A
----------------------------
Added
-----
* Fixed crash relating to old item system.
* A* cache.

Current Version: 04.08.2012A
--------------------------
Added
-----
* ALife can path a bit better. No longer teleports (as much.)
* Optimized A*.
* Composed some music.
* Items are now dropped properly.
* Items can be stored.
* Gold and coal are now items.

Previous Version: 04.07.2012A
--------------------------
Added
-----
* ALife understands difference between solid and blocking objects when pathing.
* ALife can mine.
* ALife counts attacking as an event, doing away with the need for interrupts.
* A* tries to understand solid items.

Previous Version: 04.06.2012A
---------------------------
Added
-----
* Working buildings
* Items overhauled to allow extensive customization
* ALife follows events, has basic wants/needs.
* Dirt now counted as an item and is rendered as such

