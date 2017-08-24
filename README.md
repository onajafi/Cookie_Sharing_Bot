# Cookie Sharing Bot
This is a project that I made just for having fun 
and learning to work with [Telegrams Bot](https://core.telegram.org/bots) API.

If you have a telegram application you 
can try this script by searching [@ShareTheCookieBot](http://t.me/ShareTheCookieBot)
## About
This script is written in Python and it is powered 
by the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library to sink with telegrams servers.

The script was tested on Ubuntu and Ubuntu server 16.04 LTS operating systems.
##Use for developers
This script has a lot of examples for developers 
(specially telegram bot designers) to use in there one code
in this script you can find python examples about how to work with:
* [Inline commands](https://core.telegram.org/bots/inline)
and results
* SQlite databases
* [Reply markup](https://core.telegram.org/bots/api/#replykeyboardmarkup)
 keys
* etc
## Getting Started
In continue you will see how to run this script on your own Ubuntu system (not sure if it works on other operating systems)
### Requirements
* Python 2.7.12 or higher
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Python library for Telegram Bot APIs
* [emoji](https://github.com/carpedm20/emoji) - Python library for displaying emoticons
* [sqlite3](https://sqlite.org/cli.html) - For storing information received by users
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) - For cloning the source code or for future developing helps from you :D
### Running the script
After installing the libraries it's time to run the script:

First you have to choose a directory to clone 
(or download) the source code, open a terminal and run:
```
cd <DIRECTORY PATH>
git clone https://github.com/onajafi/Cookie_Sharing_Bot.git
```
We have the source, now run:
```
python PFile.py
```
If you want to run it on the background, for example on a server or something you can simply add a '&' at the end:
```
python PFile.py &
```
and to kill the background process you have to run:
```
pkill -f PFile.py
```
## License
This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details