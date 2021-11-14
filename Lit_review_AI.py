#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:58:13 2021

Lit review AI

@author: timothy
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import pymongo
from datetime import date

today = date.today()

 
class archive_scrapper:
    """
    specific class to pull from acrhive condensed matter papers
    """

    def __init__(self, driver_path):

        self.url = "https://arxiv.org/archive/cond-mat"
        self.driver_path = driver_path

    def find_all_abstracts(self, keywords):
        """
        uses selenium webdriver to enter keywords in seachbar and grabs all paper titles and abstracts
        for those keywords, Note: currently misses the last page of search results
        """
        self.driver = webdriver.Chrome(self.driver_path)
        self.keywords = keywords
        self.driver.get(self.url)
        search_bar = self.driver.find_element_by_xpath(
            '//input[@class="input is-small"]'
        )
        search_bar.send_keys(self.keywords)

        button = self.driver.find_element_by_xpath(
            '//button[@class="button is-small is-cul-darker"]'
        )
        button.click()

        select_number_results = Select(
            self.driver.find_element_by_xpath('//select[@id="size"]')
        )
        select_number_results.select_by_value("200")
        self.driver.find_element_by_xpath(
            '//button[@class="button is-small is-link"]'
        ).click()

        titles_text = []
        abstracts_text = []
        i = 0

        while (
            len(self.driver.find_elements_by_xpath('//a[@class="pagination-next"]')) > 0
        ):
            i += 1
            Next = self.driver.find_element_by_xpath('//a[@class="pagination-next"]')
            titles = self.driver.find_elements_by_xpath(
                '//p[@class="title is-5 mathjax"]'
            )
            mores = self.driver.find_elements_by_xpath('//a[@class="is-size-7"]')
            for j in range(int(len(mores) / 2)):
                if mores[j * 2].is_displayed() and mores[j * 2].is_enabled():
                    try:
                        mores[j * 2].click()
                    except Exception as e:
                        print("error: at more " + str(j * 2), e)
            abstracts = self.driver.find_elements_by_xpath(
                '//p[@class="abstract mathjax"]'
            )
            titles_text = titles_text + [
                title.text.replace("\n", " ") for title in titles
            ]
            abstracts_text = abstracts_text + [
                abstract.text.replace("\n", " ") for abstract in abstracts
            ]
            try:
                Next.click()
            except:
                break
            if i == 100:
                break
        self.driver.close()
        results = pd.DataFrame({"Title": titles_text, "Abstract": abstracts_text})
        return results

    def find_papers(self, keywords, path_to_save):
        self.path_to_save = path_to_save
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": path_to_save,  # Change default directory for downloads
                "download.prompt_for_download": False,  # To auto download the file
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,  # It will not show PDF directly in chrome
            },
        )
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=options)
        self.keywords = keywords
        self.driver.get(self.url)
        search_bar = self.driver.find_element_by_xpath(
            '//input[@class="input is-small"]'
        )
        search_bar.send_keys(self.keywords)

        button = self.driver.find_element_by_xpath(
            '//button[@class="button is-small is-cul-darker"]'
        )
        button.click()

        select_number_results = Select(
            self.driver.find_element_by_xpath('//select[@id="size"]')
        )
        select_number_results.select_by_value("200")
        self.driver.find_element_by_xpath(
            '//button[@class="button is-small is-link"]'
        ).click()

        i = 0
        while (
            len(self.driver.find_elements_by_xpath('//a[@class="pagination-next"]')) > 0
        ):
            i += 1
            Next = self.driver.find_element_by_xpath('//a[@class="pagination-next"]')
            pdfs = self.driver.find_elements_by_link_text("pdf")
            print(len(pdfs))
            for pdf in pdfs:
                self.driver.get(pdf.get_attribute("href"))
            Next.click()
            if i > 5:
                break


class AIP_scrapper:
    '''
    class to mine papers and abstracts from AIP
    '''
    def __init__(self, driver_path):
        self.url = "https://aip.scitation.org/"
        self.driver_path = driver_path

# class PDF_cleaner

"""
magnetic_thin_films_archive = archive_scrapper(driver_path='/home/timothy/chromedriver')
lit = magnetic_thin_films_archive.find_all_abstracts('magnetic thin film')
skry = magnetic_thin_films_archive.find_all_abstracts('skyrmion thin film')
lit.reset_index(inplace=True)
data_dict = lit.to_dict("records")
skyrm_dict = skry.to_dict("records")
client = pymongo.MongoClient("mongodb+srv://tqh8pn:Hart7355@cluster0.2yo9g.mongodb.net/ArchiveretryWrites=true&w=majority")
db = client['Archive']
collection = db['skyrmion_thin_films_'+str(today)]
collection.insert_many(skyrm_dict)




skyrmion = archive_scrapper("/home/timothy/chromedriver")
skyrmion_papers = skyrmion.find_papers(
    keywords="skyrmion thin film", path_to_save="/home/timothy/NLP/skyrmion_papers/"
)

import glob
from PyPDF2 import PdfFileReader
import nltk
from nltk.tokenize import sent_tokenize
import re
import unicodedata



pdfs = glob.glob("/home/timothy/NLP/skyrmion_papers/*")
with open(pdfs[10],'rb') as f:
    pdf_object = PdfFileReader(f)
    paper = 'start: '
    for i in range(pdf_object.numPages):
        page_object = pdf_object.getPage(i)
        paper = paper + page_object.extractText()
        
def remove_line_breaks(text):
    text = re.sub('\n','',text)
    return text


paper = read_pdf(pdfs[0])
sentences = sent_tokenize(paper)
sentences_meaningful = filter_by_legnth(sentences, 30)
"""