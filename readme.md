RogueCaves - readme
===================

Current Milestone: Athletic Alpaca
----------------------------------
Todo
----
* React to things like vomit, etc
* Tint ground where liquid is spilled
* Draw item backgrounds
* If no line of sight, can the player hear an action?
* Multiple ways for dogs to attack
* ALife should figure out when they can't outrun someone

Future Milestone: Boring Badger
-------------------------------
Todo
----
* Extended cave generation (old bridges, rooms, etc).
* Random quests
* Tricky ALife
* Audio
* Accept unfinished A* paths
* ALife should flee at some point during combat
* Need animal class
* Need "tilling" task for farming
* Relationships (would probably get rid of life.owner)
* Relationship flags: Likes pets
* Save var.id

Bugs
----
* ALife still occasionally teleports due to pathing errors.
* ALife continues to calculate paths that broke in the past.
* ALife adds broken paths to cache to prevent freezes.
* ALife sometimes spawns in walls
* Crash on line 179 of pathfinding.py.
* Roomgen can lead to impossible levels.
* Walls should be destroyable, either with a pickaxe or something else.

Current Version: 06.27.2012A
----------------------------
Changed
-------
* Didn't document a lot of the work done in the past few days
* Lakes/ponds
* Naming lakes/ponds
* Bridges to buildings built on water
* levelgen.add_landmark()
* levelgen.is_landmark()
* levelgen.find_landmarks()
* levelgen.flood_fill()

Previous Version: 06.23.2012A
----------------------------
Changed
-------
* Fixed ALife locking up after combat

Previous Version: 06.22.2012A
----------------------------
Changed
-------
* Still working on combat...

Previous Version: 06.21.2012A
----------------------------
Changed
-------
* Pain
* Passing out

Previous Version: 06.20.2012A
----------------------------
Changed
-------
* Limbs track who damaged them last
* More combat changes
* Bleeding out
* Blood splatter

Previous Version: 06.19.2012A
----------------------------
Changed
-------
* Severed limbs, movement penalties
* life.get_max_speed()
* Removing combat from life.py and placing it in combat.py

Previous Version: 06.18.2012A
----------------------------
Changed
-------
* Working on combat
* Less messages during combat
* Dogs now attack
* levelgen.house - House generation
* chests no longer solid
* Fixed iteration over non-sequence bug in life.build_relationship_with()

Previous Version: 06.16.2012A
----------------------------
Changed
-------
* pathfinding.py is now using numpy
* Fixed memory leak in pathfinding.py
* Optimized most functions in levelgen.py
* Fixed farming
* Scrolling
* -font flag
* -small flag
* Sped up levelgen.get_real_estate()

Previous Version: 06.15.2012A
----------------------------
Changed
-------
* Scrolling
* Trees

Previous Version: 06.14.2012A
----------------------------
Changed
-------
* Fixed logo
* Combat overhauled
* Added limbs

Previous Version: 06.13.2012A
----------------------------
Changed
-------
* ALife will fight each other
* life.throw_item()
* life.get_items()
* life.get_items_ext()
* Getting rid of a bunch of helper functions
* levegen.get_all_items_in_building_tagged()
* Blacksmiths now sell what they forge

Previous Version: 06.12.2012A
----------------------------
Changed
-------
* Upgraded libtcod
* Caves work with libtcod
* Added forging task
* life.get_done_forges()
* life.get_open_forges()
* Tilled tiles now refresh
* life.build_history()
* Added more detail to histories
* Announces

Previous Version: 06.11.2012A
----------------------------
Changed
-------
* life.destroy_item()
* life.get_past_event()
* life.announce()
* life.receive_announce()
* life.get_farm_speed()
* Fixed error in farming task that caused ALife to freeze in stores out of the item they need
* Fixed logic in pathfinding.getadj() that caused negative x,y positions to pass the check
* Added Pygame output flag (-pygame)
* Added libtcod output (default)
* Increased level size a bit

Previous Version: 06.10.2012A
----------------------------
Changed
-------
* levelgen.town()
* Buildings are now placed in an orderly fashion
* Bought carrots not longer grow in storage
* functions.get_item_name()
* ALife is more vocal when interacting with items
* Added more phrases

Previous Version: 06.09.2012A
----------------------------
Changed
-------
* Added dislikes
* ALife now drinks
* Bartender now serves drinks
* life.does_like_item()
* life.drink()
* life.fill_container()
* life.buy_item_type_from_alife()
* life.get_nearest_building_of_type()
* Drawing in caves works again
* Fixed saving
* Added logo
* Fixed ALife shopping when shops are closed
* Task weighting

Previous Version: 06.08.2012A
----------------------------
Changed
-------
* FPS increase
* ALife has more elaborate likes/dislikes/traits
* ALife can learn the likes and dislikes of others
* life.can_farm()
* life.get_all_relationships()
* life.get_relationship_with()

Previous Version: 06.07.2012A
----------------------------
Changed
-------
* life.buy_items()
* life.dislikes
* life.likes
* ALife finally buys more seeds
* Additional phrases
* Fixed a few errors in level.py that caused no rooms to be returned
* Fixed saving/loading

Previous Version: 06.06.2012A
----------------------------
Changed
-------
* Added phrases.txt
* Added names_male_dogs.txt
* Added names_female_dogs.txt
* functions.get_dog_name_by_gender()
* functions.generate_human()
* functions.get_phrase()
* functions.get_number_of_alife_with_gender()
* life.say_phrase()
* human.get_top_love_interests() is now life.get_top_love_interests()
* All event functions were moved to life
* human.think()
* human.think_finalize()
* ALife no longer wakes up and goes back to bed immediately
* ALife no longer stands around after giving an item to someone

Previous Version: 06.05.2012A
----------------------------
Changed
-------
* ALife now name their homes
* Shop owners now get tired and go home
* life.on_wake()
* life.on_sleep()
* life.is_in_bed()
* life.get_open_beds()
* life.get_top_love_interests()
* life.give_item_to()
* life.build_relationship_with()
* life.go_to_and_claim_building()

Previous Version: 06.04.2012A
----------------------------
Changed
-------
* Traders looking for a shop to claim no longer add and remove the task until they succeed
* life.on_enemy/friendly_spotted() now accept an argument (who)
* Moved life.on_enemy/friendly_spotted() call into initial ALife scoring
* Fixed multiple shop owners trying to inhabit the same shop
* life.sell_items()

Previous Version: 06.03.2012A
----------------------------
Changed
-------
* Added dog
* ALife now find and claim buildings on their own
* Restructured the way buildings are handled
* levelgen.get_open_space_around()
* levelgen.get_open_buildings_with_items()
* levelgen.get_open_buildings_of_type()
* levelgen.get_all_buildings_of_type()
* life.get_open_stoves()
* life.get_done_stoves()
* life.get_nearest_store()
* life.follow_person()

Previous Version: 06.02.2012A
----------------------------
Changed
-------
* ALife weighs decisions based on need
* Added additional tasks for ALife to perform during downtime
* Fixed error in life.get_event()
* Potential doors no longer ask for real estate
* life.get_all_items_of_type() now accepts lists
* life.claim_building()
* life.get_claimed()
* life.get_all_growing_crops()
* life.get_all_grown_crops()

Previous Version: 06.01.2012A
----------------------------
Changed
-------
* ALife no longer buys items remotely
* ALife can cook

Previous Version: 05.31.2012A
----------------------------
Changed
-------
* Fixed levelgen.get_real_estate() returning duplicate entries
* Added stove
* Added cooking
* life.flag_item()
* life.cook()

Previous Version: 05.30.2012A
----------------------------
Changed
-------
* Saving/loading
* Level no longer ticks every second, but instead every 20 frames

Previous Version: 05.29.2012A
----------------------------
Changed
-------
* life.go_to_building_and_buy()
* life.go_to_building_and_sell()
* life.get_owned_land()
* life.claim_real_estate()
* Fixed life.get_money()
* Farmers now buy seed when they run out

Previous Version: 05.28.2012A
----------------------------
Changed
-------
* levelgen.claim_real_estate() no longer the worst function I have ever written
* Pressing 'c' now shows real_estate on the map

Previous Version: 05.27.2012A
----------------------------
Changed
-------
* Fixed error in life.pick_up_item_at() that caused ALife to not remove item from chest
* Real estate
* Farmers attempt to plant closer to their homes

Previous Version: 05.26.2012A
----------------------------
Changed
-------
* Server should now be able to tick at specified TPS: var.server_tick_rate
* 'data' directory created. Stores save files and name files
* Saving
* Most major functions now use logging.debug()
* Fixed some code that casued life.path_dest to be reset
* Menus now draw on their own surface
* Added headless (server) mode. Run with -server

Previous Version: 05.25.2012A
----------------------------
Changed
-------
* Fixed drawing in caves
* Fixed level not clearing brightness settings
* Added ID system for future use

Previous Version: 05.24.2012A
----------------------------
Changed
-------
* Drawing is a lot faster

Current Version: 05.23.2012A
----------------------------
Changed
-------
* Added `ignore_storage` flag to level.get_all_items_tagged(), should probably be put everywhere else
* Farmers now sell their crops
* Farmers store some food for themselves
* level: get_all_items_in_building_of_type()
* life: put_item_of_type()
* life.go_to_and_do() now supports most two-argument functions

Previous Version: 05.22.2012A
----------------------------
Changed
-------
* Fixed menu title rendering too far above the menu items
* Disabled thirst, which caused the ALife to become unresponsive
* Added farming task for ALife
* Farmers now pickup their crops
* Added level.get_all_items_tagged()

Previous Version: 05.21.2012A
----------------------------
Changed
-------
* Added wheat
* life.add_item() and life.add_item() now set 'pos' key
* levelgen.add_item() no longer returns a pointer to the original item
* Levels now have a tick function that is called every second
* Crops can have different images for each stage of growth

Previous Version: 05.20.2012A
----------------------------
Changed
-------
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
Changed
-------
* ALife can claim buildings
* Messages when entering/leaving buildings
* Icons now listed next to items in inventory
* Extended menu system
* New item: Bronze
* Buying items now works

Previous Version: 05.17.2012A
----------------------------
Changed
-------
* Items spawned in chests are no longer duplicated and placed outside of the chest
* Starting to add docstrings
* Life: in_building()
* Level: get_room_items()
* Menu system

Previous Version: 05.16.2012A
----------------------------
Changed
-------
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
Changed
-------
* Removed stairs going upwards in the forest.
* Blood now fades even when outside of the player's view.
* Fixed crash relating to removal of the forest's "entrances" variable.

Previous Version: 05.03.2012A
----------------------------
Changed
-------
* Timing is much more accurate now.
* "Sticky" movement fixed.
* max_fps is now set to 20 by default.

Previous Version: 04.24.2012A
----------------------------
Changed
-------
* No longer checking large amounts rooms during generate_cave_rooms()
* Added "sharp" flag to weapons.

Previous Version: 04.23.2012A
----------------------------
Changed
-------
* Fixed some dialog errors.
* Blood.
* Forgot to update readme with new changes.

Previous Version: 04.22.2012A
----------------------------
Changed
-------
* ALife forgets about enemies after they're killed.
* Fixed some repeating dialog.
* ALife now takes into consideration a target's weapon.
* Weapons now have ranks and statuses.
* Game now goes into turn-based mode when danger arises.
* Fixed issue with idle ALife automatically traveling to the surface for food.

Previous Version: 04.21.2012A
----------------------------
Changed
-------
* Added weapons.
* Added Crazy Miner.
* No longer real-time (for now).
* Fixed bug that prevented ALife from following targets between z-levels.

Previous Version: 04.12.2012A
----------------------------
Changed
-------
* Fixed possible bug relating to A* cache returning paths for wrong z-level.
* Started room generation for caves.

Previous Version: 04.11.2012A
----------------------------
Changed
-------
* Optimized draw_screen() for caves.
* ALife clips through fellow workers.
* Fixed additional pathing issues.
* Teleporting due to pathing conflicts fixed.

Previous Version: 04.09.2012A
----------------------------
Changed
-------
* Fixed crash relating to old item system.
* A* cache.

Current Version: 04.08.2012A
--------------------------
Changed
-------
* ALife can path a bit better. No longer teleports (as much.)
* Optimized A*.
* Composed some music.
* Items are now dropped properly.
* Items can be stored.
* Gold and coal are now items.

Previous Version: 04.07.2012A
--------------------------
Changed
-------
* ALife understands difference between solid and blocking objects when pathing.
* ALife can mine.
* ALife counts attacking as an event, doing away with the need for interrupts.
* A* tries to understand solid items.

Previous Version: 04.06.2012A
---------------------------
Changed
-------
* Working buildings
* Items overhauled to allow extensive customization
* ALife follows events, has basic wants/needs.
* Dirt now counted as an item and is rendered as such

