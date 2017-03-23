# html scraper tests

If you need to re-download the html files but they are blocked, you can route it through open knesset server (assuming you have ssh access)

```
ssh oknesset-db1 curl 'http://www.knesset.gov.il/plenum/heb/display_full.asp' > knesset_data/html_scrapers/tests/plenum_display_full.asp
```
