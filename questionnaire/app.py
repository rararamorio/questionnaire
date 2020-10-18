import json
import boto3


def answer(params):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="https://dynamodb.ap-northeast-1.amazonaws.com")
    table = dynamodb.Table('questionnaire')

    item = {}
    try:
        response = table.get_item(Key={'name': params['name']})

        print(response)
        item = response['Item'] if ('Item' in response) else {}
    except Exception as e:
        print('get item')
        print(e)

    if item != None and len(item) > 0:
        print('marge')
        params['infra_skill'] = params['infra_skill'] + item['infra_skill']
        params['poll_count'] = params['poll_count'] + item['poll_count']
        params['pg_skill'] = params['pg_skill'] + item['pg_skill']
        params['op_skill'] = params['op_skill'] + item['op_skill']
        params['comm_skill'] = params['comm_skill'] + item['comm_skill']
        params['strength'] = params['strength'] + item['strength']
        params['management'] = params['management'] + item['management']
        params['kindness'] = params['kindness'] + item['kindness']

    return table.put_item(Item=params)

# 受け取ったパラメータを元に


def lambda_handler(event, context):
    print('event')
    # print(event)
    name = event['queryStringParameters']['name']
    # インフラスキル
    infra_skill = int(event['queryStringParameters']['infra_skill'])
    # プログラミングスキル
    pg_skill = int(event['queryStringParameters']['pg_skill'])
    # 運用スキル
    op_skill = int(event['queryStringParameters']['op_skill'])
    # コミュニケーション力
    communication_skill = int(event['queryStringParameters']['comm_skill'])
    # 体力
    strength = int(event['queryStringParameters']['strength'])
    # マネジメント力
    management = int(event['queryStringParameters']['management'])
    # やさしさ
    kindness = int(event['queryStringParameters']['kindness'])

    params = {
        'name': name,
        'poll_count': 1,
        'infra_skill': infra_skill,
        'pg_skill': pg_skill,
        'op_skill': op_skill,
        'comm_skill': communication_skill,
        'strength': strength,
        'management': management,
        'kindness': kindness
    }

    res = answer(params)

    return {
        "statusCode": res['ResponseMetadata']['HTTPStatusCode'],
        "body": json.dumps({
            "message": "complete"
        }),
    }
