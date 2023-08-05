# __init__.py
__version__ = "0.0.2"

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

############
#### Constants
############

# The consistent root of the talk URLs
gen_conf_url_root1 = 'https://www.churchofjesuschrist.org/study/general-conference/'

# Dict for converting URL abbreviations to their respective full names
ref_dict = {
    '1-ne':'1 Nephi',
    '2-ne':'2 Nephi',
    'jacob':'Jacob',
    'enos':'Enos',
    'jarom':'Jarom',
    'omni':'Omni',
    'w-of-m':'Words of Mormon',
    'mosiah':'Mosiah',
    'alma':'Alma',
    'hel':'Helaman',
    '3-ne':'3 Nephi',
    '4-ne':'4 Nephi',
    'morm':'Mormon',
    'ether':'Ether',
    'moro':'Moroni'
    }


############
#### Functions
############

# 
def expand_hyphen_ref(x):
    '''Expands hyphenated ranges of verses to full lists (e.g. verses 3-7 becoms 3,4,5,6,7)
    
    Arguments:
        x(str): string containing a digit, a hyphen, and another digit (ex. "3-7")
    
    Returns:
        all_verses(list): a list of all of the numbers from the expanded list.
    '''
    first_digit = int(x.split('-')[0])
    last_digit = int(x.split('-')[1])
    all_verses = list(range(first_digit, last_digit + 1))
    return all_verses

def get_conf_urls(years):
    '''Generates the URLs for general conferences from the years specified,
    to be used in further scraping.
    
    Arguments:
        years(int or list of int): the year(s) from which to scrape talk footnotes.
    
    Returns:
        urls(list): a list of URLs for scraping.
    '''

    if isinstance(years, list):
        urls = []
        for year in years:
            url_april = gen_conf_url_root1 + str(year) + '/04' 
            url_oct = gen_conf_url_root1 + str(year) + '/10'
            urls.append(url_april)
            urls.append(url_oct)
    else:
        url_april = gen_conf_url_root1 + str(years) + '/04' 
        url_oct = gen_conf_url_root1 + str(years) + '/10' 
        urls = [url_april, url_oct]
    return urls

def get_book_verse(x):
    ''' Identifies the book, chapter, and verse of a scripture reference from its
    churchofjesuschrist.org URL format.
    
    Arguments: 
        x(str): the URL of a scripture
    
    Returns:
        book, chapter, verse (tuple): A tuple containing the book, chapter, and verse ints.
    '''
    first_split = x.split('bofm/')[1]
    book = ref_dict[first_split.split('/')[0]]
    verse = re.findall('\.(.*?)\?', first_split)[0]
    chapter = re.findall('\/(.*?)\.', first_split)[0]
    if '-' in verse:
        verse_final = expand_hyphen_ref(verse)
        book_final = [book] * len(verse_final)
        chapter_final = [chapter] * len(verse_final)
        return book_final, chapter_final, verse_final
    else:
        return book, chapter, verse

def scrape_talk_footnotes(url, print_progress = False):
    ''' Uses webscraping on churchofjesuschrist.org to identify the scriptures referenced in
    all general conference talks from a given period.
    
    Arguments:
        url(str): The URL of a given year's conference table of contents page.
        print_progress(bool): An indicator of whether or not to print the 
            URL of the talk being scraped. Will be replaced with logging
            in future.'''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    talk_toc_items = soup.find_all("a", {"class": "item-U_5Ca"}, href = True)
    talk_link_prefix = 'https://www.churchofjesuschrist.org/'
    talk_links = [talk_link_prefix + x['href'] for x in talk_toc_items]
    del talk_links[0]
    
    ########### Get the footnote links from each talk
    url_indiv_talk = talk_links[0]
    page_indiv_talk = requests.get(url_indiv_talk)
    soup_indiv_talk = BeautifulSoup(page_indiv_talk.content, "html.parser")
    footnotes = soup_indiv_talk.find_all('a', {'class':'scripture-ref'}, href = True)
    footnotes_links = [talk_link_prefix + x['href'] for x in footnotes]


    talk_names = []
    book_list = []
    chapter_list = []
    verse_list = []
    
    for url_indiv_talk in talk_links:
        if print_progress == True:
            print('Scraping ' + url_indiv_talk)
        page_indiv_talk = requests.get(url_indiv_talk)
        soup_indiv_talk = BeautifulSoup(page_indiv_talk.content, "html.parser")
        footnotes = soup_indiv_talk.find_all('a', {'class':'scripture-ref'}, href = True)
        footnotes_links = [talk_link_prefix + x['href'] for x in footnotes]
        for note in footnotes_links:
            if 'bofm' in note:
                
                try:
                    ref = get_book_verse(note)
                    if ',' in ref[2]:
                        for verse in ref[2].split(','):
                            book_list.append(ref[0])
                            chapter_list.append(ref[1])
                            verse_list.append(verse)
                            talk_names.append(url_indiv_talk)
                    else:
                        book_list.append(ref[0])
                        chapter_list.append(ref[1])
                        verse_list.append(ref[2])
                        talk_names.append(url_indiv_talk)
    
                except:
                    next
            else:
                continue
            
    refs_df = pd.DataFrame({'talk':talk_names,
                  'books':book_list,
                  'chapters':chapter_list,
                  'verses':verse_list}).explode(['books','chapters','verses']).reset_index(drop=True)

    refs_df[['chapters', 'verses']] = refs_df[['chapters', 'verses']].apply(pd.to_numeric)
    return refs_df

def check_verse(book, chapter, verse, refs_df, multiple_verse = False):
    ''' Determines if a given scripture reference is mentioned in the talk
    footnotes scraped.
    
    Arguments:
        book(str): The book of scripture in question.
        chapter(int): The chapter in question.
        verse(int): The int in question.
        refs_df(DataFrame): The pandas DataFrame obtained using scrape_talk_footnotes.
        multiple_verse(bool): Indicates whetehr the reference contains more than one verse.'''
        
    if multiple_verse == True:
        talks = refs_df.query('books == @book & chapters == @chapter & verses in @verse') 
    else:
        talks = refs_df.query('books == @book & chapters == @chapter & verses == @verse')
    return [x for x in talks['talk']]
