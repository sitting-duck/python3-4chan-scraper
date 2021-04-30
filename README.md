Original found here: https://github.com/graysonpike/python-4chan-scraper
My code is more recent, but has less features. I had to modify the code a little from grayson original implementation. Maybe 4chan code has changed on the site or something. /shrug

# 4chan Image Scraper
An image scraper written in Python.
Run in Jenkins to scrape every night at midnight.
Grabs associated text in the posts too. 
Can be interesting to run on pol to see what is going on in reaction to public events, or just create datasets of images. 
I like to use the YOLO neural net classifier to then sort these images according to subject.

### Usage (Linux, OSX):

** I have not tested this on OSX
- Use python3
- Make sure to install dependencies (BeautifulSoup4):
  - `sudo pip3 install -r requirements.txt`
- For entire boards: `python3 scraper.py board <board letter> <output directory>`
  - eg. `python3 scraper.py board g output`
- For single threads: `python3 scraper.py thread <thread url> <output directory>`
  - eg. `python3 scraper.py thread http://boards.4chan.org/g/thread/49098915 output`
- Remember, the directory must exist to put files in it!

NOTE: If you experience an error installing Pillow with pip3, try installing the `libjpeg8-dev` package.

### Output Directory Formatting Examples:

- Relative Paths:
  - `output`
  - `output/`
- Absolute Paths:
  - `/Users/me/Pictures/4chan`

### Jenkins:
Ive included a JenkinsFIle for use with a declarative pipeline. 
If you don't have it installed you may have to install the CRON plugin. 
CRON is what allows the Jenkins to get a signal to run your script. 
