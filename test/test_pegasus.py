"""
    If:
        ModuleNotFoundError: No module named 'gql.transport.aiohttp'
    Solution:
        pip uninstall gql
        pip install --pre gql[all]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import BartForConditionalGeneration, BartTokenizer

from server_com import ServerCom


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


async def query_data(url, gql_query):
    transport = AIOHTTPTransport(url=url)

    async with Client(
        transport=transport, fetch_schema_from_transport=True,
    ) as session:

        # Execute single query
        query = gql(gql_query)
        result = await session.execute(query)

        return result


if __name__ == "__main__":
    server_com = ServerCom()

    # Use your own query instead
    gql_query = """
        query getArticles {
            Article(order_by: {timestamp: asc}, where: {timestamp: {_gte: "2020-02-01T00:00:00", _lte: "2020-03-01T00:00:00"}}) {
                timestamp
                journal
                id
                headline
                content
            }
        }
    """
    result = asyncio.run(query_data(server_com.url, gql_query))
    news = result['Article'][0]

    # Put your news here
    content = news['content']  # a string of news
    headline = news['headline']  # a string of news' headline

    # Model
    # multi-news(long), newsroom(medium), wikihow (short), cnn_dailymail
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-cnn_dailymail")  
    model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail").to(DEVICE)

    batch = tokenizer.prepare_seq2seq_batch([content, result['Article'][1]['content']], truncation=True, padding='longest', return_tensors="pt").to(DEVICE)
    summary = model.generate(**batch)
    summary = tokenizer.batch_decode(summary, skip_special_tokens=True)

    print(headline)
    print("=============================")
    print(content)
    print("=============================")
    print(summary)