"""
webscraping and NLP of Applied Physics Letters
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import pandas as pd
driver = webdriver.Chrome('/home/timothy/chromedriver')

url = 'https://arxiv.org/archive/cond-mat'

keywords = ['magnetic thin films']

driver.get(url)

search_bar = driver.find_element_by_xpath('//input[@class="input is-small"]')
search_bar.send_keys(keywords[0])

button = driver.find_element_by_xpath('//button[@class="button is-small is-cul-darker"]')
button.click()

select_number_results = Select(driver.find_element_by_xpath('//select[@id="size"]'))
select_number_results.select_by_value('200')
driver.find_element_by_xpath('//button[@class="button is-small is-link"]').click()

titles_text = []
abstracts_text = []
i=0

while len(driver.find_elements_by_xpath('//a[@class="pagination-next"]'))>0:
    i +=1
    Next = driver.find_element_by_xpath('//a[@class="pagination-next"]')
    titles = driver.find_elements_by_xpath('//p[@class="title is-5 mathjax"]')
    mores = driver.find_elements_by_xpath('//a[@class="is-size-7"]')
    for j in range(int(len(mores)/2)):
        if mores[j*2].is_displayed() and mores[j*2].is_enabled():
            mores[j*2].click()
    abstracts =  driver.find_elements_by_xpath('//p[@class="abstract mathjax"]')
    titles_text = titles_text + [title.text for title in titles]
    abstracts_text = abstracts_text + [abstract.text for abstract in abstracts]
    Next.click()
    if i == 100:
        break




#driver.close()