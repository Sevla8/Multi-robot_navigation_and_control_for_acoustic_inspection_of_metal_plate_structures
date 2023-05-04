# Simulation

## Launch

```bash
source devel/setup.bash
roslaunch chroma_gazebo_interfaces crawler_navigation.launch
rostopic echo /crawler_0/uwb
rosservice call /crawler_0_uwb_antenna_link/get_token "previous_token_users:
- ''"
```