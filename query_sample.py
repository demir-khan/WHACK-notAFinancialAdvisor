from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# backend functions that both take in a string parameter (the crypto name token)
from sentiment import sentiment
from technical import technical


class TokenNameRequest(Model):
    token: str

class TokenNameResponse(Model):
    sentimentanalysis: str
    technicalanalysis : str


agent = Agent(
    name="cryptoname",
    seed="cryptoname agent for whack",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

fund_agent_if_low(agent.wallet.address())

"""async def function_name(token):
    return sentiments

async def function_name(token):
    return sentiments"""

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")


@agent.on_query(model=TokenNameRequest, replies={TokenNameResponse})
async def query_handler(ctx: Context, sender: str, _query: TokenNameRequest):
    ctx.logger.info(f"Query received: {_query.token}")
    try:
        # do something here
        technical_ans = technical(_query.token)
        sentiment_ans = sentiment(_query.token)
        print(technical_ans, sentiment_ans)
        await ctx.send(sender, TokenNameResponse(sentimentanalysis=str(sentiment_ans), technicalanalysis=str(technical_ans)))
    except Exception:
        print("error")
        #await ctx.send(sender, TokeNameResponse(sentimentanalysis="fail", technicalanalysis="fail"))


if __name__ == "__main__":
    agent.run()