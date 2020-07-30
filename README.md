# Insta Unfollower Beak

Its a simple Selemium script for unfollow accounts you are following but hes doesn't follow you. We using Firefox Webdriver for run it.

    IMPORTANT: We are not responsible for misuse. We set up to do only 15 unfollow every 15 minutes to prevent your account from being blocked to unfollow.

## Installation

### Docker(Not Working)
Already not working, need to apply configurations for firefox to run in container:

```
docker build -t eduardobarbiero/insta-unfollower-beak .
docker run -v $(pwd)/cache:/usr/src/insta-unfollower-beak/cache --env INSTAGRAM_USERNAME=username --env INSTAGRAM_PASSWORD=password eduardobarbiero/insta-unfollower-beak:latest
```

### Local Machine
Needs Python3, Pip3 and Firefox installed.

Run:
```
pip3 install --no-cache-dir -r requirements.txt
```

After run:
```
INSTAGRAM_USERNAME=username INSTAGRAM_PASSWORD=password HEADLESS=False python3 unfollower-beak.py
```


## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/[USERNAME]/instagram-unfollower-beak. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [code of conduct](https://github.com/[USERNAME]/instagram-unfollower-beak/blob/master/CODE_OF_CONDUCT.md).


## License

The package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in the Insta Unfollower Beak project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/[USERNAME]/instagram-unfollower-beak/blob/master/CODE_OF_CONDUCT.md).