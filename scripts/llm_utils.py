import os
import json
import urllib3
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from helper import generate_prompt

MODEL_ID = os.environ["AWS_BEDROCK_INFERENCE_PROFILE_ARN"]


def get_llm_client():
    botocore_config: Config = Config(
        connect_timeout=15, 
        read_timeout=60, 
        retries={'max_attempts': 3}
        )
    return boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.environ["AWS_BEDROCK_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_BEDROCK_SECRET_ACCESS_KEY"],
        config=botocore_config
    )


def get_llm_response(prompt: str, model_id: str=MODEL_ID) -> str:
    """
    Make request to LLM and generate a response.
    :param prompt: str, instruction text.
    :param model_id: str, model id/name
    :return: str, generate LLM response
    """
    client = get_llm_client()

    # Format the request payload using the model's native structure.
    native_request = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.9,
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(
            modelId=MODEL_ID, 
            body=request
            )
        # Decode the response body.
        model_response = json.loads(response["body"].read())
        # Extract and print the response text.
        response_text = model_response["generation"]
        return response_text

    except (ClientError, Exception) as e:
        print(f"Can't invoke '{model_id}'. Reason: {e}")


def lambda_handler(event, context):
    # Generate llm response
    prompt = generate_prompt()
    response_llm = get_llm_response(prompt=prompt)

    # Send llm response to slack
    http = urllib3.PoolManager()
    slack_webhook_url = os.environ["SLACK_WEBHOOK"]
    headers = {'Content-Type': 'application/json'}
    slack_message = json.dumps({'text': response_llm}).encode('utf-8')
    req = http.request(
        'POST',
        slack_webhook_url,
        body=slack_message,
        headers=headers
    )

    return {
        'statusCode': 200,
    }