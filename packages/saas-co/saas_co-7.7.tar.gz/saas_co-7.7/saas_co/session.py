import boto3

#####################

def session_from_credentials(creds, region):
    try:
        return boto3.session.Session(
            region_name=region,
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"]
        )
    except:
        return None

#####################

def assume_role(**params):
    region = params.get('region', 'us-east-1')
    access_key_id = params.get('access_key_id')
    secret_access_key = params.get('secret_access_key') 
 
    account_id = params.get('accountId')
    role_name = params.get('roleName')
    session_name = params.get('sessionName','tmp')
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'

    try:
        if access_key_id:
            sts = boto3.client('sts', 
                               region_name=region,
                               aws_access_key_id=access_key_id,                
                               aws_secret_access_key=secret_access_key)
        else:
            sts = boto3.client('sts')
        assumed_role = sts.assume_role(RoleArn=role_arn, 
                                       RoleSessionName=session_name)
        credentials = assumed_role.get('Credentials')
    except Exception as e:
        print(account_id, 'Assume error')
        credentials = None

    return session_from_credentials(credentials, region)

############################################

def get_account_regions(accounts):
    account_regions = list(set([(a['account_id'], a['region']) for a in accounts]))
    return [{'account_id':a[0], 'region':a[1]} for a in account_regions]
    
#####################

def get_session(a, **args):
    reg = a.get('region')
    aid = a.get('account_id')
    sessions = args.get('sessions')
    if not sessions: 
        for ar in args.get('account_regions'): sessions.update({ar['account_id']:{}})
    s = sessions.get(aid,{}).get(reg,None)
    if not s: 
        # Create a new session object and cache it in the sessions dictionary
        s = assume_role(access_key_id = args.get('key'), 
                        secret_access_key = args.get('secret'),
                        roleName = args.get('role'),
                        accountId = aid, region=reg)
        sessions[aid][reg] = s
    return s
        
#####################

def get_sessions(accounts, **kargs):
    account_regions = get_account_regions(accounts)
    kargs.update({'account_regions': account_regions, 'sessions': {}})
    for a in accounts:
        account_id = a['account_id']
        region = a['region']
        # Check if the account/region pair has already been processed
        if (account_id, region) in kargs['sessions']:
            continue
        # Call get_session() and add the resulting session to the sessions dictionary
        session = get_session(a, **kargs)
        kargs['sessions'][(account_id, region)] = session
    return kargs['sessions']



    #########################################

    import boto3
from saas_co import session as cos

def get_main_sts_client(secret_id, access_key_id, secret_access_key, region = 'us-east-1'):
    sm_client = boto3.client('secretsmanager')
    secretString = eval(sm_client.get_secret_value(SecretId=secret_id)['SecretString'])
    access_key_id = secretString[access_key_id]; 
    secret_access_key = secretString[secret_access_key]
    
    return boto3.client(
        'sts', 
        region_name=region,
        aws_access_key_id=access_key_id,                
        aws_secret_access_key=secret_access_key)

def get_main_session(sts_client, account, role, region, session_name):
    creds = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account}:role/{role}',
        RoleSessionName=session_name).get('Credentials')
    return cos.session_from_credentials(creds, region)
    
def get_session_with_external_id(sts_client, account, role, region, session_name, external_id):
    creds = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account}:role/{role}',
        RoleSessionName=session_name, ExternalId=external_id).get('Credentials')
    return cos.session_from_credentials(creds, region)
    
def get_main_power_session(secret_id, access_key_id, secret_access_key, account, region, role, session_name):
    sts_client = get_main_sts_client(secret_id, access_key_id, secret_access_key, region)
    return get_main_session(sts_client, account, role, region, session_name)

##########################

def get_sts_client_from_session(s, account, role, region):
    creds = s.get_credentials().get_frozen_credentials()
    return boto3.client('sts',
        aws_access_key_id=creds.access_key,
        aws_secret_access_key=creds.secret_key,
        aws_session_token=creds.token,
        region_name=region)

def get_session_from_session(s, account, role, region):
    sts_client = get_sts_client_from_session(s, account, role, region)
    session_name = s.client('sts').get_caller_identity()['Arn'].split('/')[-1].split(':')[0]    
    return get_main_session(sts_client, account, role, region, session_name)

def get_session_from_session_with_accounts(s, account, role, region, accounts):
    external_id = get_external_id_from_account(accounts, account)
    sts_client = get_sts_client_from_session(s, account, role, region)
    session_name = s.client('sts').get_caller_identity()['Arn'].split('/')[-1].split(':')[0]
    return get_session_with_external_id(sts_client, account, role, region, session_name, external_id)

def get_main_finder_session(s, account, region, role):
    try:     return get_session_from_session(s, account, role, region)
    except:  return None
    
def get_customer_session(s, accounts, account, region, role):
    try:    return get_session_from_session_with_accounts(s, account, role, region, accounts)
    except Exception as e:
        print(e)
        return None
    
##########################################################################
##########################################################################

def get_tid_by_account(accounts, account):
    filtered = accounts[accounts['account'].astype(str).apply(lambda x: str(account) in x)]
    return None if filtered.empty else filtered.iloc[0]['tid']

########################

def get_external_id_from_account(main_session, accounts, account):
    tenant_id = get_tid_by_account(accounts, account)
    try:
        response = main_session.client('secretsmanager').get_secret_value(SecretId=tenant_id)
        return response.get('SecretString',response.get('SecretBinary'))
    except Exception as e:
        print(e)
        return None

##########################################################################
##########################################################################




