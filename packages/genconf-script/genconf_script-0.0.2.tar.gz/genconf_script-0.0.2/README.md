# genconf_script

### Description
This is a simple Python package created as a proof-of-concept and side project to demonstrate web scraping and simple package creation skills. The subject matter for this package was chosen primarily for its familiarity to the package's creator.

The package allows the user to interact with footnotes from talks given at the General Conference of the Church of Jesus Christ of Latter-day Saints, a semi-annual event at which the church's leaders speak. Using the package, the user can identify talks that reference a given verse from the Book of Mormon, one of the books of scripture utilized by members of the aforementioned church. 

#### Installation

`pip install genconf_script`

#### Example Usage

`import pandas as pd`
`from genconf_script import get_conf_urls, scrape_talk_footnotes as scrape, check_verse`

Obtain the URLs in question.

`urls = get_conf_urls([2021,2022])`

Scrape footnote references from all of the talks in question.

`combined_df = pd.concat([scrape_talk_footnotes(url) for url in conf_urls])`

Identify which talks (if any) contain the verse(s) in question.

`final_talks = check_verse('Alma', 36, 17, combined_df)`