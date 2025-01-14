import praw

from newsbot import log


class Reddit:

    def __init__(self, config) -> None:
        self._config = config

    def clean_up_subreddits(self, sub_reddits: str) -> str:
        log.debug('Got subreddits to clean: {0}'.format(sub_reddits))
        return sub_reddits.strip().replace(" ", "").replace(',', '+')
    
    def get_latest_news(self, sub_reddits: str) -> str:
        log.debug('Fetching news from reddit')
        r = praw.Reddit(user_agent=self._config.user_agent,
                        client_id=self._config.client_id,
                        client_secret=self._config.client_secret)
        r.read_only = True
        
        sub_reddits = self.clean_up_subreddits(sub_reddits)
        log.info(f"Fetching subreddits: {sub_reddits}")
        submissions = r.subreddit(sub_reddits).hot(limit=5)
        submission_content = ''
        
        try:
            for post in submissions:
                submission_content += f"{post.title} - {post.url} \n\n"
        except praw.errors.Forbidden:
                log.debug(f"subreddit {sub_reddits} is private".format())
                submission_content = "Sorry couldn't fetch; subreddit is private."
        except praw.errors.InvalidSubreddit:
                log.debug(f"Subreddit {sub_reddits} is invalid or doesn't exist.")
                submission_content = "Sorry couldn't fetch; subreddit doesn't seem to exist."
        return submission_content
