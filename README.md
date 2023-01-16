# stringlines
making stringline plots

this is a very crude way to plot stringlines

enjoy!

        control_stop : list
            list of stations by which the stop_times is filtered by
        sp_stop_id : list, optional
            list of stations to display (default is sp_stop_id = control_stop)

            !!! important !!!
            the station ids must be in order of arrival
        weekday : str, optional
            what weekday to show
        direction : int, optional
            0 is northbound trains only, 1 is southbound trains only, 3 is both directions (default is 0)
        start_time : str, optional
            start time of graph in the format 'HH:MM:SS'
        end_time : str, optional
            end time of graph in the format 'HH:MM:SS'
        title : str, optional
            title of the graph (default is first and last stations)
