import aws_cdk as core
import aws_cdk.assertions as assertions

from llm_slack_bot.llm_slack_bot_stack import LlmSlackBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in intuit_llm_slack_bot/intuit_llm_slack_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LlmSlackBotStack(app, "llm-slack-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
