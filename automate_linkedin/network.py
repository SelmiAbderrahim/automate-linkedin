from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from easy_selenium.logger import logger
try:
    from .base import Base
except ImportError:
    from base import Base


class Follow(Base):
    """
    Follow people on my network.
    """
    def __init__(self):
        super(Follow, self).__init__()
        self.max_user_to_follow: str = 8
        self.url = "https://www.linkedin.com/mynetwork"

    def start(self, driver: WebDriver):
        wait = WebDriverWait(driver, 5)
        action = ActionChains(driver)
        timeout_exception_counter = 0
        followed_users_counter = 0
        if self.url not in driver.current_url:
            driver.get(self.url)
        while True:
            if followed_users_counter >= self.max_user_to_follow:
                logger.success(f"-- {self.max_user_to_follow} users has been followed.")
                break
            if timeout_exception_counter >= 10:
                logger.warning("Timeout exceed: Check your internet speed!")
                break
            follow_buttons = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, (
                        "//button[contains(@aria-label, 'Follow') "
                        "and not(contains(@aria-label, 'Unfollow'))]"
                    )
                ))
            )
            for follow_button in follow_buttons:
                if followed_users_counter >= self.max_user_to_follow:
                    break
                followed_user = " ".join(follow_button.get_attribute("aria-label").split(" ")[1:])
                follow_button = follow_button.find_element(
                    by=By.XPATH,
                    value=(
                        ".//span[text()='Follow']"
                    )
                )
                try:
                    action.move_to_element(follow_button).click().perform()
                    self.short_nap()
                    try:
                        skip_button = wait.until(
                            EC.presence_of_all_elements_located((
                                By.XPATH, (
                                    "//div[contains(@class, 'artdeco-modal') "
                                    "and contains(@class, 'actionbar')]/"
                                    "button[contains(@class, 'artdeco-button')]"
                                )
                            ))
                        )[0]
                    except TimeoutException:
                        pass
                    else:
                        action.move_to_element(skip_button).click().perform()
                    logger.success(f"You followed {followed_user}.")
                    followed_users_counter += 1
                    self.short_nap()
                except TimeoutException:
                    logger.warning("No one to follow 😔")
                    timeout_exception_counter += 1
                self.long_nap()
            self.long_nap()


class Connect(Base):
    """
    Invite people from my network to connect with me.
    """
    def __init__(self):
        self.max_user_to_connect: str = 8
        super(Connect, self).__init__()
        self.url = "https://www.linkedin.com/mynetwork"

    def start(self, driver: WebDriver):
        wait = WebDriverWait(driver, 5)
        action = ActionChains(driver)
        timeout_exception_counter = 0
        invited_users_counter = 0
        if self.url not in driver.current_url:
            driver.get(self.url)
        while True:
            if invited_users_counter >= self.max_user_to_connect:
                logger.success(f"-- {self.max_user_to_connect} users has been invited.")
                break
            if timeout_exception_counter >= 10:
                logger.warning("Timeout exceed: Check your internet speed!")
                break
            invited_users = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, (
                        "//button[contains(@aria-label, 'Invite')]"
                    )
                ))
            )
            for invited_user in invited_users:
                self.short_nap()
                if invited_users_counter >= self.max_user_to_connect:
                    break
                try:
                    invite_button = invited_user.find_element(
                        by=By.XPATH,
                        value=(
                            ".//span[text()='Connect']"
                        )
                    )
                    self.short_nap()
                    action.move_to_element(invite_button).click().perform()
                    invited_user = " ".join(invited_user.get_attribute("aria-label").split(" ")[1:-2])
                    logger.success(f"You invited {invited_user}.")
                    invited_users_counter += 1
                    self.short_nap()
                except TimeoutException:
                    logger.warning("No one to connect with 😔")
                    timeout_exception_counter += 1
                self.long_nap()
            self.long_nap()
