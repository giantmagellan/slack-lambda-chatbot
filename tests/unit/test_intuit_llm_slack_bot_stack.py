import aws_cdk as core
import aws_cdk.assertions as assertions

from intuit_llm_slack_bot.intuit_llm_slack_bot_stack import IntuitLlmSlackBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in intuit_llm_slack_bot/intuit_llm_slack_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IntuitLlmSlackBotStack(app, "intuit-llm-slack-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
