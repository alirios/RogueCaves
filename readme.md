RogueCaves - readme
===================

Current milestone: Athletic Alpaca
----------------------------------
Todo
----
* Extended cave generation (old bridges, rooms, etc).
* Accept unfinished A* paths.
* Audio.
* Optimize the update() function in Pygcurse.
* Let game run headless.
* Only let ALife clip if the two have active paths.
* Combine generate_room() and generate_cave_rooms()

Bugs
----
* ALife still occasionally teleports due to pathing errors.
* ALife continues to calculate paths that broke in the past.
* ALife adds broken paths to cache to prevent freezes.
* Crash on line 179 of pathfinding.py.

Current Version: 04.22.2012A
----------------------------
Added
-----
* ALife forgets about enemies after they're killed.
* Fixed some repeating dialog.
* ALife now takes into consideration a target's weapon.

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

