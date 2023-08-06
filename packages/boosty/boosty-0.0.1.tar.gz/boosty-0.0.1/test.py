import asyncio

from boosty.api.api import API
from boosty.types import Post
from boosty.utils.logging import logger


def validator(obj: list[Post]):
    for post in obj:
        print("", end="")
        if len(post.comments.data) != 0:
            print("", end="")
            for comment in post.comments.data:
                if comment.replyCount != 0:
                    # print(post.id)
                    print(comment.replyCount)
                    print(comment.replies.data[0])
                # for comment_data in comment.data:
                #     if comment_data.type != "text":
                #         print(comment_data)


async def poll_posts(name):
    api = API()
    response = await api.get_post("ikakprosto", post_id="dfd9446c-fe6d-4c97-9b24-59f68b865e56", reply_limit=10, comments_limit=100)
    print(validator([response]))
    print(response.title)
    response = await api.get_posts(name, limit=10, comments_limit=10)
    resp_reversed = response.data[::-1]
    logger.info(len(resp_reversed))
    validator(resp_reversed)
    response = await api.get_post_comments(name, post_id=resp_reversed[0].id)
    logger.info(response)
    return resp_reversed


if __name__ == '__main__':
    logger.info(asyncio.run(poll_posts("ikakprosto")))
