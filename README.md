## LinkedIn Python Bot

I built this project because I'm super lazy to check my LinkedIn account. <br>So by using this bot, I'll increase my profile views, interactions, followers, and connections.<br>
And since I love sharing my stuff with others, I created this package. 
So if you enjoy it, start it on [GitHub](https://github.com/SelmiAbderrahim/automate-linkedin).

<br>

[![](https://i.ibb.co/R9J5nGm/imageedit-6-6834400292.jpg)](https://www.youtube.com/channel/UCmrvAIpkl1L8WlalusTRlnw)

<br><br>

   
- [Features](#features)
- [Installation](#installation)
- [Usage options](#usage-options)
    - [2.1. Create driver](#21-create-driver)
    - [2.2. Login](#22-login)
- [1. Posts Interactions](#1-posts-interactions)
  - [CLI](#cli)
  - [API](#api)
- [2. publishing](#2-publishing)
  - [CLI](#cli-1)
  - [API](#api-1)
- [3. Network](#3-network)
  - [3.1. Follow people](#31-follow-people)
    - [CLI](#cli-2)
    - [API](#api-2)
  - [3.2. Connect with people](#32-connect-with-people)
    - [CLI](#cli-3)
    - [API](#api-3)
- [4. Environment variables](#4-environment-variables)
- [5. Run it on a server](#5-run-it-on-a-server)


<br><hr><br>

# Features

- Interact with LinkedIn posts.
  - Like
  - Comment
- Auto post/image publishing
   
# Installation

```
pip install automate-linkedin
```

or

```
pip install git+https://github.com/SelmiAbderrahim/automate-linkedin
```

# Usage options

1. CLI 

You can use these features throught the command line interface (CLI), which is quite useful to run it on a server. 

```
$ autoln OPTIONS
```

**options:**

- **username**: Your LinkedIn email address (required).
- **password**: Your LinkedIn email password (required).
- **env**: Get username & password as environment variables. **(optional)**.
- **headless**: Hide the browser's window. **(optional)**.

2. API

You can use the same features on your own project (code) throught the API.

 ```
 from automate_linkedin.interactions import Posts
 class Interaction(Posts):
     pass
 ```


For the LinkedIn authentication, I'm using the [easy_selenium](https://pypi.org/projects/easy-py-selenium) to create a Chrome driver and login to LinkedIn accounts.

### 2.1. Create driver

```
from easy_selenium.driver.chrome.driver import Driver
driver = Driver()
chrome = driver.create(headless=headless)
```

### 2.2. Login 

```
from easy_selenium.authentication.login.linkedin import Login
login = Login(username, password)
authenticated = login.start(chrome)
```


<br><hr><br>




# 1. Posts Interactions

## CLI

Interact with the LinkedIn 'home page' or 'groups' posts.

**Options**
- **post-interaction**: Interact with your LinkedIn posts. (required).

  > ```autoln --username plain_text_email --password plain_text_password --post-interaction```

- **post-number-likes**: Number of post likes  [default: 5] (required).

  > ```autoln --username plain_text_email --password plain_text_password --post-interaction --post-number-likes 10```

- **env**: Get username & password as environment variables. **(optional)**.

  > ```autoln --env --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction```

- **headless**: Hide the browser's window. **(optional)**.

  > ```autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction```

- **comment-number-likes**: The number of likes of comments. **(optional)**.

- **like-post-comments**: Like comments of each posts. **(optional)**.

  > ```autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction --like-post-comments --comment-number-likes 2```

- **auto-comment**: Comment with positive examples. **(optional)**.

  > ```autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction --auto-comment```

💡 **Example:** If I want to run a headless browser to like 20 posts and comment on any of these posts if possible.

```
autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction --auto-comment --post-number-likes 25
```

 ## API

After creating a Chrome driver and making sure you're authenticated, as shown above, you can use this function to interact with posts on your LinkedIn pages and groups.

```
from interactions import Posts

posts = Posts()
posts.start(chrome)
```

**Attributes:**

```
>> print(Posts.__doc__)

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
```

<br><hr><br>

# 2. publishing

## CLI

This will allow you to publish a post with an image or text on your LinkedIn profile.


**options:**

- **--publish**: Enable the publishing option **(required)**.
- **--text**: The text content of the post **(optional)**.
- **--image-path**: The absolute path of the image **(optional)**.

💡 **Example:** If I want to publish a post with my image and greeting message.

```
autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --publish --text "Hi people!" --image-path C:\\images\me.png
```

## API

**Post text only**

```
from automate_linkedin.publish import Publish
p = Publish()
p.post(chrome, content="greeting!")
```

**Post text and image**

```
from automate_linkedin.publish import Publish
p = Publish()
p.image(chrome, r"C:\Users\selmi\Pictures\BloggersHood1.png", content="zfzazafazf")
```

<br><hr><br>
# 3. Network

Manage your network.

## 3.1. Follow people

You can follow up to 16 people each time.

### CLI

```
autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --follow-network
```

### API 

```
from automate_linkedin.networkk import Follow
follow = Follow()
follow.start(driver)
```

<br>

## 3.2. Connect with people

You can send invites up to 16 people each time.

### CLI

```
autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --connect-network
```

### API 

```
from automate_linkedin.networkk import Connect
connect = Connect()
connect.start(driver)
```

<br><br><br>

# 4. Environment variables

There many reasons for using environment variables in your projects, including:
- Easy configuration
- Better security
- Fewer production mistakes

So in your working directory, create a new file `.env` and place the secrets you'll use with this package.

**Exmaple**

```
LINKEDIN_EMAIL_ADDRESS=example@email.com
LINKEDIN_PASSWORD=password
```

Then you gonna use it throught the cli:

```
autoln --env --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD
```

# 5. Run it on a server

I have tested the below code on my Ubuntu server, if something went wrong, please open a new issue.

- The first thing you have to do is installing Chrome

```
sudo apt-get update
sudo apt-get install google-chrome-stable
google-chrome --version
```

- Login to your server

```
ssh user@ip
```

- Create a virtualenv

**Linux/Mac**

```
python -m pip install virtualenv
python -m virtualenv env
source env/bin/activate
```

**Windows**

```
py -m pip install virtualenv
py -m virtualenv env
env\Scripts\activate
```

- Install `automate-linkedin`

```
pip install automate-linkedin
```

- Create a new `bash` file with the content below

Let's assume this is my working directory

```
selmi@7BNVUM:/selmi$ pwd
/home/selmi/automate-linkedin
```

Then we create a new file `like.sh` in that working directory.

```
#!/usr/bin/env bash
SHELL=/bin/bash
DISPLAY=:0
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /home/selmi/automate-linkedin
autoln --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --post-interaction --like-post-comments --comment-number-likes 2 --post-number-likes 10 --auto-comment
```

Then for the permissions:

```
sudo chmod +x /home/selmi/automate-linkedin/likes.sh
```

- Environment variables [see this](#4-environment-variables)

- Crontab

and finally, we automate the process using crontab.

```
crontab -e
```

To run that bash file every 5 hours, add this line:

```
0 */5 * * * ./home/selmi/automate-linkedin/likes.sh
```

Then save it.

That's it.