from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path
import os
from easy_selenium.logger import logger
try:
    from .base import Base
except ImportError:
    from base import Base


class Publish(Base):
    """
    Post articles, texts, and images in your LinkedIn account.

    Args:
        url (str): The page's url (default = 'https://www.linkedin.com/feed')
        short_sleep_range (tuple[float, float]): time.sleep(short range) (default = (0.5, 0.9))
        long_sleep_range (tuple[float, float]): time.sleep(long range) (default = (1.5, 4.9))
    """
    def post(self, driver: WebDriver, content: str) -> bool:
        """
        Publish a post.

        Args:
            driver (WebDriver): A Chrome webdriver.
            content (str): The text you'll post

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        if self.url not in driver.current_url:
            driver.get(self.url)
        try:
            wait = WebDriverWait(driver, 5)
            action = ActionChains(driver)
            self.short_nap()
            start_post_button = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, (
                        "//div[contains(@class, 'hare-box-feed-entry')]"
                        "/div/button[contains(@class, 'share-box-feed-entry')]"
                    )
                ))
            )
            action.move_to_element(start_post_button).click().perform()
            self.short_nap()
            text_editor = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, "//div[contains(@class, 'ql-editor ql-blank')]"
                ))
            )
            text_editor.clear()
            action.move_to_element(text_editor).click().perform()
            self.short_nap()
            text_editor.send_keys(content)
            self.short_nap()
            submit_button = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, (
                        "//div[contains(@class, 'share-box')]/"
                        "button[contains(@id, 'ember') and contains(@class, 'share-action')]"
                    )
                ))
            )
            action.move_to_element(submit_button).click().perform()
            self.short_nap()
        except Exception as error:
            logger.error(f"Post.post: \t{str(error)}")
            return False
        else:
            logger.success(f"{content} has been posted.")
            return True

    def image(self, driver: WebDriver, image: Path, content: str = None) -> bool:
        """
        Publish an image + text.

        Args:
            driver (WebDriver): A Chrome webdriver.
            image: (Path): The absolute path of the image.
            content (str): The text you'll post.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        if not os.path.isfile(image):
            logger.warning(f"The given path {image} doesn't exist!")
            return False
        if self.url not in driver.current_url:
            driver.get(self.url)
        try:
            wait = WebDriverWait(driver, 5)
            action = ActionChains(driver)
            self.short_nap()
            add_a_photo = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Add a photo']"
                ))
            )
            action.move_to_element(add_a_photo).click().perform()
            self.short_nap()
            add_photo = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, "//input[contains(@id,'image-sharing-detour-container')]"
                ))
            )
            add_photo.send_keys(image)
            self.short_nap()
            submit_button = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, (
                        "//div[contains(@class, 'share-box-footer')]/button"
                    )
                ))
            )[1]
            action.move_to_element(submit_button).click().perform()
            if content:
                self.short_nap()
                text_editor = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH, "//div[contains(@class, 'ql-editor ql-blank')]"
                    ))
                )
                text_editor.clear()
                action.move_to_element(text_editor).click().perform()
                self.short_nap()
                text_editor.send_keys(content)
                self.short_nap()
                submit_button = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH, (
                            "//div[contains(@class, 'share-box')]/"
                            "button[contains(@id, 'ember') and contains(@class, 'share-action')]"
                        )
                    ))
                )
                action.move_to_element(submit_button).click().perform()
                self.short_nap()
        except Exception as error:
            logger.error(f"Post.image: \t{str(error)}")
            return False
        else:
            logger.success(f"{content} has been posted.")
            return True
