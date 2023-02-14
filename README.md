# Stringlines

Making stringline plots from Israel Railways GTFS data.


## Getting started

This code can be used with general GTFS files but it is recommended to use the `gtfs_rail_18-01-2023` folder for ease of computation and a few fixed issues.

Set the date. If you are using the `gtfs_rail_18-01-2023` folder, only january 2023 is supported.

Set `STOPS_TO_FILTER_BY` `STOPS_TO_DISPLAY` `STOPSֹֹ_TO_REMOVE_BY` using `rail_branches.py` as a reference or try the given examples.
`STOPS_TO_DISPLAY` need to be set in order from north to south. 

Set `direction` 0 for northbound 1 for southbound anything else for both. Some examples have this set already.

Every train that doesn't end in one of the stations on the graph has it's end station stated at the of the line. You can change `textRotation` so that it doesn't disrupt the other lines on the graph.

## Background

Usually when using GTFS data you choose routes using the `routes.txt` file but in the data for Israel Railways is a bit different than buses.
I filtered the data using stations instead of routes because it is more intuitive when looking at trains.
