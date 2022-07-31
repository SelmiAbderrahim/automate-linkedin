from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException
)
import sys
from easy_selenium.common.funcs import scroll_to
from easy_selenium.logger import logger
try:
    from .constants import (POSITIVE_WORDS)
    from .base import Base
except ImportError:
    from constants import (POSITIVE_WORDS)
    from base import Base


class Posts(Base):
    """
    Interact with the LinkedIn posts.

    Params:
        number_of_posts_to_like (int): Number of posts to like (default = 5).
        number_of_post_comments_to_like (int): Number of comments to like for each post (default = 2).
        like_post_comments (bool): Start liking comments (default = False).
        auto_comment (bool): Post a positive comment for random posts (default = False).
        url (str): The page's url (default = 'https://www.linkedin.com/feed')
        short_sleep_range (tuple[float, float]): time.sleep(short range) (default = (0.5, 0.9))
        long_sleep_range (tuple[float, float]): time.sleep(long range) (default = (1.5, 4.9))

    Returns:
        None
    """
    def __init__(self):
        super().__init__()
        self._like_posts: bool = True
        self._number_of_posts_to_like: int = 5
        self._like_post_comments: bool = False
        self._number_of_post_comments_to_like: int = 2
        self._auto_comment: bool = False

    @property
    def like_posts(self) -> bool:
        return self._like_posts

    @like_posts.setter
    def like_posts(self, like: bool) -> None:
        self._like_posts = like

    @property
    def number_of_posts_to_like(self) -> int:
        return self._number_of_posts_to_like

    @number_of_posts_to_like.setter
    def number_of_posts_to_like(self, number: int) -> None:
        self._number_of_posts_to_like = number

    @property
    def like_post_comments(self) -> bool:
        return self._like_post_comments

    @like_post_comments.setter
    def like_post_comments(self, like: bool) -> None:
        self._like_post_comments = like

    @property
    def number_of_post_comments_to_like(self) -> int:
        return self._number_of_post_comments_to_like

    @number_of_post_comments_to_like.setter
    def number_of_post_comments_to_like(self, number: int) -> None:
        self._number_of_post_comments_to_like = number

    @property
    def auto_comment(self) -> int:
        return self._auto_comment

    @auto_comment.setter
    def auto_comment(self, number: int) -> None:
        self._auto_comment = number

    def start(self, driver: WebDriver) -> None:
        wait = WebDriverWait(driver, 10)
        action = ActionChains(driver)
        timeout_error_counter = 0
        posts_to_like_counter = 0
        if self.url not in driver.current_url:
            driver.get(self.url)
        while True:
            self.short_nap()
            if timeout_error_counter > 20:
                logger.warning("TimeOutException: exceed limit --> check your internet speed!")
                break
            if posts_to_like_counter >= self.number_of_posts_to_like:
                logger.info(f"{self.number_of_posts_to_like} posts has been liked!")
                break
            try:
                # ----------------------------------[1] GET POSTS
                feeds = wait.until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, (
                            "//div["
                            "contains(@id, 'ember') and contains(@class, 'feed-shared-update-v2')"
                            "]/div"
                        )
                    ))
                )
            except TimeoutException:
                pass
            else:
                # ----------------------------------[2] LOOP OVER POSTS
                for feed in feeds:
                    if posts_to_like_counter >= self.number_of_posts_to_like:
                        break
                    try:
                        self.long_nap()
                        feed_author = feed.find_element(
                            by=By.XPATH,
                            value=(
                                ".//span[contains(@class, 'feed-shared-actor') "
                                "and contains(@class, 'title')]/span/span"
                            )
                        ).text
                        # ----------------------------------[3] LIKE THE POST
                        try:
                            like_button = feed.find_element(
                                by=By.XPATH,
                                value=(
                                    ".//span[contains(@class, 'feed-shared-social-action-bar') "
                                    "and not (contains(@class, 'comments-comment-social-bar'))]"
                                    "/button[contains(@aria-label, 'Like') "
                                    "and contains(@aria-label, 'post') and "
                                    "contains(@aria-pressed, 'false')]"
                                )
                            )
                        except TimeoutException:
                            driver.execute_script("window.scrollTo(0, 600);")
                        else:
                            # scroll_to(driver, like_button)
                            self.short_nap()
                            action.move_to_element(like_button).click().perform()
                            logger.success(f"You liked {feed_author}s post.")
                            self.short_nap()
                            posts_to_like_counter += 1
                        # ----------------------------------[4] GET THE COMMENTS CONTAINER
                        try:
                            comments_container = feed.find_element(
                                    by=By.XPATH,
                                    value=".//div[contains(@class, 'comments-comments-list')]"
                                )
                            comments = comments_container.find_elements(
                                    by=By.XPATH,
                                    value=".//article[contains(@class, 'comments-comment-item')]"
                                )
                        except TimeoutException:
                            pass
                        else:
                            # ----------------------------------[5] LIKE THE COMMENTS
                            if self.like_post_comments:
                                for comment in comments[:self.number_of_post_comments_to_like]:
                                    try:
                                        comment_like_button = comment.find_element(
                                            by=By.XPATH,
                                            value=(
                                                ".//button[contains(@aria-label, 'Like') "
                                                "and contains(@aria-label, 'post') and "
                                                "contains(@aria-pressed, 'false')]"
                                            )
                                        )
                                    except TimeoutException:
                                        pass
                                    else:
                                        self.short_nap()
                                        comment_author = " ".join(comment_like_button.get_attribute(
                                            "aria-label"
                                        ).split(" ")[1:-1])
                                        self.short_nap()
                                        action.move_to_element(comment_like_button).click().perform()
                                        logger.success(f"You liked {comment_author} comment.")
                                        self.short_nap()
                            # ----------------------------------[6] AUTO COMMENTING
                            if self._auto_comment:
                                a_postive_comment = None
                                for comment in comments:
                                    comment_content = comment.find_element(
                                        by=By.XPATH,
                                        value=".//span[contains(@class, 'feed-shared-main-content')]"
                                    ).text
                                    if any(
                                            [
                                                word.lower() in comment_content.lower() and len(comment_content.split(" ")) < 3 \
                                                for word in POSITIVE_WORDS
                                            ]):
                                        a_postive_comment = comment_content
                                        break
                                    self.short_nap()
                                if a_postive_comment:
                                    try:
                                        comment_area = comments_container.find_element(
                                            by=By.XPATH,
                                            value="//div[@class='ql-editor ql-blank']"
                                        )
                                    except TimeoutException:
                                        logger.error(f"no comment area for {comment_content}!")
                                    else:
                                        scroll_to(driver, comment_area)
                                        self.short_nap()
                                        comment_area.clear()
                                        comment_area.send_keys(a_postive_comment)
                                        self.short_nap()
                                        try:
                                            comment_submit_button = comments_container.find_element(
                                                by=By.XPATH,
                                                value="//button[contains(@aria-label, 'Post comment on')]"
                                            )
                                        except TimeoutException:
                                            logger.critical(f"no comment button for {comment_content}!")
                                        else:
                                            action.move_to_element(comment_submit_button).click().perform()
                                            logger.success(f"You commented on {feed_author} post's with {a_postive_comment}.")
                                            self.long_nap()
                    except (TimeoutException, NoSuchElementException):
                        pass
                    except KeyboardInterrupt:
                        sys.exit()
