# %%
# Eithan Schonberg 01/2023


from stringlines_graph import Stringlines
import stringlines_graph


# %%
#
all_stations = stringlines_graph.stops

# %%
# קרית מוצקין תל אביב האוניברסיטה
control_stop = [37360, 37362, 37364, 40640,
                37366, 37368, 37370, 37372,
                37374, 37376, 37378, 37380,
                42507, 37388, 37386, 37392, 41293]

# תל אביב ההגנה - באר שבע מרכז דרך הנגב המזרחי
# זה עדיין מראה את הרכבות שעוברות בנגב המערבי
control_stop = [37312, 37314, 37308, 37316, 42419, 42418, 37336, 37338, 37340, 37334, 37292]

# ירושלים הרצליה
control_stop = [42286, 37306, 37292, 37350, 37358, 37360, 37362]


# # מסילת העמק
# control_stop = [40583]
# stop_ids = [37374, 37376, 37378, 37380, 42507,37388, 40584, 40581, 40582, 40583]
# # in this case is is recomended to use the following call to Stringlines:
# s = Stringlines(control_stop,sp_stop_id=stop_ids,direction=3)

# start_time and end_time are optional
start_time='07:30:00'
end_time='13:00:00'
# in this case is is recomended to use the following call to Stringlines:
s = Stringlines(control_stop,start_time = start_time, end_time = end_time)

# s = Stringlines(control_stop)


# %%

s.show()


# %%
