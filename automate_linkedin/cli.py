import click
import sys
from decouple import config
from easy_selenium.logger import logger
from easy_selenium.authentication.login.linkedin import Login
from easy_selenium.driver.chrome.driver import Driver
from easy_selenium.common.funcs import driver_safe_quit
try:
    from interactions import Posts
    from publish import Publish
    from network import (
        Follow, Connect
    )
except ModuleNotFoundError:
    from .interactions import Posts
    from .publish import Publish
    from .network import (
        Follow, Connect
    )


@click.command()
@click.option(
        "--username", "-u", type=str, help="Your LinkedIn email address.",
        required=True
    )
@click.option(
        "--password", "-p", help="Your LinkedIn email password.",
        required=True
    )
@click.option(
        "--env", help="Get username & password as environment variables.",
        is_flag=True, default=False
    )
@click.option(
        "--headless", "-h", help="Hide the browser's window.",
        is_flag=True, default=False
    )
@click.option(
        "--post-interaction", "-posts", help="Interact with LinkedIn feed/groups posts.",
        is_flag=True, default=False
    )
@click.option(
        "--post-number-likes", "-p-likes", type=int, help="Number of post likes.",
        default=5, show_default=True
    )
@click.option(
        "--like-post-comments", "-comments", help="Like posts comments.",
        is_flag=True, default=False
    )
@click.option(
        "--comment-number-likes", "-c-likes", type=int, help="Number of likes for each post's comments.",
        default=1, show_default=True
    )
@click.option(
        "--auto-comment", help="Comment with positive examples.",
        is_flag=True, default=False
    )
@click.option(
        "--publish", help="Post images or texts.",
        is_flag=True, default=False
    )
@click.option(
        "--text", "-text", type=str, help="The text you'll publish.",
    )
@click.option(
        "--image-path", "-img", type=str, help="The image absolute path.",
    )
@click.option(
        "--follow-network", help="Follow people in my network.",
        is_flag=True, default=False
    )
@click.option(
        "--connect-network", help="Connect people in my network.",
        is_flag=True, default=False
    )
def main(
        username, password, env, headless, post_interaction,
        post_number_likes, comment_number_likes, auto_comment,
        like_post_comments, text, image_path, publish, follow_network,
        connect_network):
    if env:
        username = config(username, None)
        password = config(password, None)
    if not username or not password:
        logger.critical("Can't get username or password!")
        return None
    try:
        driver = Driver()
        chrome = driver.create(headless=headless)
        login = Login(username, password)
        authenticated = login.start(chrome)
        if authenticated:
            if post_interaction:
                post = Posts()
                post.auto_comment = auto_comment
                post.like_post_comments = like_post_comments
                post.number_of_posts_to_like = post_number_likes
                post.number_of_post_comments_to_like = comment_number_likes
                post.start(chrome)
            if publish:
                publish = Publish()
                if text and image_path:
                    publish.image(chrome, image_path, text)
                elif text:
                    publish.post(chrome, text)
            if follow_network:
                follow = Follow()
                follow.start(chrome)
            if connect_network:
                connect = Connect()
                connect.start(chrome)
    except Exception as error:
        logger.critical(sys.exc_info()[0])
        logger.critical(str(error))
        driver_safe_quit(chrome)
    except KeyboardInterrupt:
        sys.exit()
    driver_safe_quit(chrome)


if __name__ == "__main__":
    main()
