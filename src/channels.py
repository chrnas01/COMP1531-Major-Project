data = {
    # 'channels': [
    #     {
    #             'channel_name': name
    #             'channel_id': channel_id
    #             'privacy_status': is_public 

    #             'owner_members': [
    #                 1,
    #             ],
    #             'all_members': [
    #                 1,
    #             ],
    #     },
    #     {
    #             'channel_name': name
    #             'channel_id': channel_id
    #             'privacy_status': is_public 

    #             'owner_members': [
    #                 1,
    #             ],
    #             'all_members': [
    #                 1,
    #             ],
    #     },
    # ],
}




def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    return {
        'channel_id': 1,
    }
