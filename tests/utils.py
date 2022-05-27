
def has_refresh_token(resp):
    assert b'refresh_token' in resp.data
        
def has_pwd_length_error(resp):
    assert b'password must be at least 12 characters' in resp.data

def has_pwd_form_error(resp):
    assert b'password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character' in resp.data

def has_invalid_chars_error(resp):
    assert b'Invalid characters' in resp.data
    
def has_invalid_firstname_error(resp):
    has_invalid_chars_error(resp)
    
    assert b'firstname' in resp.data 
    
def has_invalid_lastname_error(resp):
    has_invalid_chars_error(resp) 
    
    assert b'lastname' in resp.data

def has_invalid_email_error(resp):
    assert b'Not a valid email address' in resp.data
    
def has_username_form_error(resp):
    assert b'username must contain uppercase letters, lowercase letters, numbers and underscores only' in resp.data

def has_username_length_error(resp):
    assert b'username must be at least 5 characters long and at most 30 characters' in resp.data

def has_used_username_error(resp):
    assert b'Username already in use' in resp.data

def has_used_email_error(resp):
    assert b'Email already in use' in resp.data

def has_user_deleted_error(resp):
    assert b'user has been deleted' in resp.data
    
def has_incorrect_user_cred_error(resp):
    assert b'Incorrect username or email and password' in resp.data
    
def has_logout_success(resp):
    assert b'logged out successfully' in resp.data
    
def has_invalid_token_error(resp):
    assert b'Token' in resp.data and b'is invalid' in resp.data or b'Missing JWT' in resp.data
    
def has_expired_token_error(resp):
    assert b'Token is expired' in resp.data
    
def has_post_created(name, resp):
    assert b' '.join([name,b'created successfully']) in resp.data
    
def has_post_updated(name, resp):
    assert b' '.join([name, b'updated successfully']) in resp.data
    
def has_too_short_error(resp):
    assert b'Shorter than minimum length' in resp.data
    
def has_too_long_error(resp):
    assert b'Longer than maximum length' in resp.data
    
def has_too_short_error(resp):
    assert b'Shorter than minimum length' in resp.data
    
def has_length_range_error(resp):
    assert b'Length must be between' in resp.data
    
def has_disallowed_post_type_error(name, resp):
    assert b' '.join([b'This user is not allowed to make',name, b'posts']) in resp.data
    
def has_min_value_error(resp):
    assert b'Must be greater than or equal to' in resp.data
    
def has_max_value_error(resp):
    assert b'Must be less than or equal to' in resp.data
    
def has_value_range_error(resp):
    assert b'Must be greater than or equal to' in resp.data
    assert b'and less than or equal to' in resp.data
    
def has_date_range_error(resp):
    assert b'The end date cannot be earlier than the start date' in resp.data
    
def has_invalid_date_error(resp):
    assert b'Not a valid datetime' in resp.data
    
def has_manager_post_error(resp):
    assert b'Gas station managers can only make posts for gas stations they manage' in resp.data
    
def has_invalid_num_error(resp):
    assert b'Not a valid number' in resp.data
    
def has_duplicate_gas_type_error(resp):
    assert b'Only one price per gas type allowed per post' in resp.data
    
def has_404_error(resp):
    assert b'does not exist' in resp.data
    
def has_vote_success(resp):
    assert b'vote toggled successfully' in resp.data
    
def has_vote_disallowed_error(resp):
    assert b'user is not allowed to vote on posts' in resp.data
    
def has_no_self_vote_error(resp):
    assert b'Users cannot vote on their own posts' in resp.data
    
def has_not_votable_error(resp):
    assert b'post is not votable' in resp.data
    
def has_deleted_post_error(resp):
    assert b'specified post has been deleted' in resp.data
    
