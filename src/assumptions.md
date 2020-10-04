Assumptions:

Authentication:

-   Email
    -   Will only consist of 1 dot before the @ sign
    -   Can have capital letters before the @ as well as after
-   Token
    -   For iteration 1, token will be an email string
-   Names
    -   Length of characters are inclusive within the bounds (as specifically stated in future additions)
    -   handle_str is the concatenation of the firstname and lastname, but to be made unqiue, it will be allocated a id number added as a suffix within the 20 character limit
    -   The names are only alphabetical characters
-   u_id
    -   Begins on u_id 1 (assumed from starter code provided)
    -   u_id 1 is the flockr owner (global owner)
    -   u_id 1 is the only flockr owner (global owner)
-   handle
    -   Concatenation is cut to 20 characters, but changing it to make it unique is not capped at 20 characters
    -   The password is not the user's first and last name concatenated in all lowercase

Channel:

-   You can remove your own ownership if you are the last channel owner
-   Channels can have no channel owners
-   Channels can have no members
-   channel_addowner will raise an input error if u_id is invalid
-   channel_removeowner will raise an input error if u_id is invalid
-   Flockr owner needs to be in the channel before they can add or remove owners in the channel
-   Start index for channel_messages cannot be negative
