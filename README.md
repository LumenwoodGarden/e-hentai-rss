# e-hentai-rss

A rss generator for tags/artists/anything you can search on e-hentai inspired by [mangadex-rss](https://github.com/marceloslacerda/mangadex-rss).

# Installtion

Clone this repository.
```bash
git clone https://github.com/LumenwoodGarden/e-hentai-rss
cd e-hentai-rss
```

Install the requirements.

```bash
pip3 install -r requirements.txt
```


Add a feed to `feeds.txt`. The format for this is:

```feed-name;your-query;path/to/configurations;path/for/the/output/file.xml```

`feed-name` is the name of the feed that will be displayed by your feed reader and will be used as argmuent when calling `main.py`.

`your-query` is what you would write in the e-hentai search bar to arrive at the feed you want to generate a rss file for.

`path/to/configurations` is the path to your configurations text file for this feed if you have one. (can be left empty, defaults to configs.txt).

`path/for/the/output/file` is self-explanatory. (can be left empty, output will be `feed-name`.xml in the project folder)

All argmuents are seperated by `;` and can't include `;`


Run to generate a feed
```bash
python3 main.py feed-name
```

---

# Configurations

Set the values in `configs.txt` to 1 or 0 for the different categories you want to include or exclude from your query.
MINRATING` sets the lowest possible rating entry can have and goes from 0 to 5.

If you want different configurations for some feeds, create a new file, keep the order of the values and specify the path to your file as the third arguments in `feeds.txt` for this feed.

# Using the generated file

Just point your feed reader to the local file. I personally use [thunderbird](https://blog.thunderbird.net/2022/05/thunderbird-rss-feeds-guide-favorite-content-to-the-inbox/), you can just put `file://` + `path/for/the/output/file.xml` as the feed url.

For more information, refer to [mangadex-rss](https://github.com/marceloslacerda/mangadex-rss#how-do-i-use-the-generated-file)

# Updating the generated file

To update your feed you have to generate a new file by running the program again.
This can be done using a cron job for more info refer to [mangadex-rss](https://github.com/marceloslacerda/mangadex-rss#how-do-i-keep-updating-the-generated-rss) again, however consider checking out the limitations listed below before you try that.

# Limitations

Unlike mangadex-rss, e-hentai-rss doesn't use the [e-hentai api](https://ehwiki.org/wiki/API) as this only allows you to look up metadata for galleries and images. So e-hentai-rss request the html file for your query instead and extracts all relevant infos from there, this comes with a few limitations unfortunately.

* understandably e-hentai takes countermeasures against excessive requests and can temporarily ban your ip address (1hr -> 24hrs -> maybe more, didn't get that far)
    * if you want to use a cron job and/or update multiple feeds, try not to overwhelm e-hentai
* the http request doesn't include your credentials or preferences, filtering categories and languages has to done via the configurations or query
* if the page you want to generate a feed for can't be specified with the given tools, it probably isn't possible
* the search result page only includes 25 entries, if more than 25 entries were added since the last update, the oldest ones will be skipped

# Final notes

If you run into any issues, consider opening an issue.
