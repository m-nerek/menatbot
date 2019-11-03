import re

async def get_frames(self, msg, user, *args, **kwargs):
    '''
    Main method thats called for the frame data function.
    Currently works only for SFV data thanks to Pauls nicely
    formatted data <3.
    '''
    # Check if they want verbose output.
    verbose = False
    info_result = re.search(self.info_regex, msg)
    if info_result:
        verbose = True
        msg = re.sub(self.info_regex, '', msg).strip()
    result = re.search(self.regex, msg)

    if not result:
        return ("You've passed me an incorrect format %s. "
                "The correct format is !frames character_name "
                "[vt1/vt2] move_name") % user

    char_name = result.group(1)
    move_name = result.group(3)
    if result.group(2):
        # If either of the vtriggers matched, then we will
        # pass the number of the matched one.
        vtrigger = result.group(2)[-1]
    else:
        vtrigger = False

    frame_data = await self.get_data(**kwargs)
    if not frame_data:
        return 'Got an error when trying to get frame data :(.'

    matched_value = self.match_move(char_name, move_name,
                                    vtrigger, frame_data)
    if not matched_value:
        return ("Don't waste my time %s. %s with %s is not a valid "
                "character/move combination for SFV.") % (user,
                                                          char_name,
                                                          move_name)
    else:
        char, move, data = matched_value
        text_output = self.format_output(
            char, move, vtrigger, data, frame_data, move_name
        )
        if verbose and 'char_stat' not in data:
            embed_output = self.format_embeded_message(
                char, move, vtrigger, data
            )
            return self.add_custom_fields(data, text_output, embed_output)
        else:
            return text_output



@memoize(60 * 60 * 24 * 7)
async def get_data(self, **kwargs):
    '''
    Simple helper function that hits the frame data dump
    endpoint and returns the contents in json format.
    '''
    resp = await get_request(self.url)
    if resp:
        frame_data = json.loads(resp)
        self.add_reverse_mapping(frame_data)
        return frame_data
    else:
        return False