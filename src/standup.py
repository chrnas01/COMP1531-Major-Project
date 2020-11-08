'''
This File will hold the standup functions. 
'''

'''
For a given channel, start the standup period whereby for the next "length" seconds if someone calls "standup_send" with a message, 
it is buffered during the X second window then at the end of the X second window a message will be added to the message queue in the 
channel from the user who started the standup. X is an integer that denotes the number of seconds that the standup occurs for
'''
def standup_start(token, channel_id, length):

    return {
        'time_finish': 
    }



'''
For a given channel, return whether a standup is active in it, and what time the standup finishes. If no standup is active, then time_finish returns None
'''
def standup_active(token, channel_id):
    return {
        'is_active': 
        'time_finish':
    }


'''
Sending a message to get buffered in the standup queue, assuming a standup is currently active
'''
def standup_send(token, channel_id, message): 
    return {}