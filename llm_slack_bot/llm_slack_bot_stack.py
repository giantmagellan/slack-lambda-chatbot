from aws_cdk import (
    aws_lambda as _lambda,
    Duration,
    Stack
)
from constructs import Construct

class LlmSlackBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = _lambda.Function(
            self, 
            id="lambda_function",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="llm_utils.lambda_handler",
            code=_lambda.Code.from_asset("./scripts/"),
            timeout=Duration.seconds(15)
        )
