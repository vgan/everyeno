everyeno
========
everyeno is a bot designed to run on a schedule and tweet/ tumbl details of master releases for brian eno in chronological order. </br>
you can see results here:</br>
<ul>
   <li>http://twitter.com/everyeno</li>
   <li> http://everyeno.tumblr.com</li>
</ul>
i thought this would be a fun way to learn to use the discogs API and visualize how much interesting work brian eno has been involved with over the years as an artist and producer. </br>
<b>Operation:</b> </br>
<ul>
    <li>on 1st run, it downloads info for every master release brian eno is credited on via the discogs api and creates a local file called releases.csv (note: after first run manually check and sort the data in the csv to your liking before running again.)</li>
    <li>on subsequent runs it steps through each release and tweets/ tumbls each one, keeping track via a second local file  tweeted.txt</li>
</ul>

<b>APIs/ Wrappers:</b> </br>
  - Discogs https://github.com/discogs/discogs_client
  - Twitter (tweepy) https://github.com/tweepy/tweepy
  - Tumblr (pytumblr) https://github.com/tumblr/pytumblr
  - Google Custom Search Engine (cse) https://developers.google.com/custom-search/json-api/v1/reference/cse/list
</br>

<b>Scheduling via Cron:</b> </br>
        @hourly your-username python /path-to-your-script/everyeno.py >> /path-to-your-script/everyeno.log 2>&1

