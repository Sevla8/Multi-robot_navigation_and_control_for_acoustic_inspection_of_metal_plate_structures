#!/usr/bin/env bash

source ./params.sh

cd /home/chroma/Documents/bugwright2-ws/bugwright_ws/
source devel/setup.bash

m="${MISSION[1]}"

for w in "${WORLD[@]}"
do
	for d in "${DISTANCE[@]}"
	do
		for s in "${STRIDE[@]}"
		do
			if [ -d "/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/$m-$w-$d-$s/" ]
			then
				echo "Already done."
			else
				mkdir /home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/$m-$w-$d-$s/

				crawler_1_x=-3.0
				crawler_1_y=-3.0
				crawler_2_x=''
				crawler_2_y=-3.0
				case $d in
					6.0)
						crawler_2_x=3.0
						;;
					3.0)
						crawler_2_x=0.0
						;;
					2.0)
						crawler_2_x=-1.0
						;;
					1.0)
						crawler_2_x=-2.0
						;;
				esac

				roslaunch my_sim crawler_ugw_with_uwb_simulation_spawn.launch \
					grid_width:=$GRID_WIDTH \
					grid_height:=$GRID_HEIGHT \
					grid_resolution:=$GRID_RESOLUTION \
					crawler_1_starting_position_x:=$crawler_1_x \
					crawler_1_starting_position_y:=$crawler_1_y \
					crawler_2_starting_position_x:=$crawler_2_x \
					crawler_2_starting_position_y:=$crawler_2_y \
					world:=$w \
					headless:=true \
					gui:=false \
					paused:=false \
					> /home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/$m-$w-$d-$s/crawler_ugw_with_uwb_simulation_spawn.out 2>&1 &

				gz_PID=$!

				sleep 20

				roslaunch my_sim crawler_navigation_nospawn.launch \
					grid_width:=$GRID_WIDTH \
					grid_height:=$GRID_HEIGHT \
					grid_resolution:=$GRID_RESOLUTION \
					mission_name:=$m \
					crawlers_distance:=$d \
					stride_size:=$s \
					headless:=true \
					gui:=false \
					paused:=false \
					> /home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/$m-$w-$d-$s/crawler_navigation_nospawn.out 2>&1

				rosservice call /save_occgrid

				mv /home/chroma/Downloads/occupancy_grid.png /home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/$m-$w-$d-$s/occupancy_grid.png

				pkill -P $$

				sleep 20
			fi
		done
	done
done