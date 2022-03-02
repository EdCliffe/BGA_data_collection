"""The Scraper class is the base class which contains useful methods for
webscraping.

    Main Features:
    -------------
        - Using BeautifulSoup
            - Create a BeautifulSoup object from a given URL
            - Find web-links from a data-table BeautifulSoup object
        - Using Selenium
            - Request a Url
            - Send keys to an html element id
            - Click an element using xpath
            - Click an element using id
            - Gather links from a table
            - Download images
            - Save data to a file
            """
# %%
from email.mime import image
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
import shutil
from selenium.common.exceptions import NoSuchElementException


class Scraper:
    def __init__(self) -> None:
        self.url = None
        self.soup = None
        self.driver = webdriver.Chrome
        self.link_list = []
        pass

    def soup_page(self, url: str, headers=None, cookies=None) -> BeautifulSoup:

        """Create BeautifulSoup object using the text from the target url.

        Keyword arguments:
        -----------------
        url -- target url, string
        headers -- optional access headers, string
        cookies -- optional access cookies, string
        Returns:
        -------
        html parsed BeautifulSoup object
        """

        page = requests.get(url, headers=headers, cookies=cookies)
        html = page.text  # Get the content of the webpage
        self.soup = BeautifulSoup(html, 'html.parser')
        # print('soups up')

        return self.soup

    def soup_links_from_table(self, soup, table_name: str, table_attrs: str,
                              element_tag: str, link_tag: str,
                              limit: int = 0) -> list:

        """Get url links from a data table which is stored as BeautifulSoup object.
        Returns a list of links.

        Keyword arguments:
        -----------------
        soup -- target BeautifulSoup page,
        table_name -- target data table on the page
        table_attrs -- target data table id attribute
        element_tag -- tag associated wth desired elements
        link_tag -- tag associated with links, which are inside the elements
        limit -- this is used to reduce the final link list,
                 defaults to no limit if left blank

        Returns:
        ------
        URL's stored in list
        """

        i = 0
        table_tree = soup.find(name=table_name, attrs={'id': table_attrs})

        element = table_tree.findAll(element_tag)

        for link in element:
            url = link.get(link_tag)
            self.link_list.append(url)
            i += 1

        # data limiter, set "links" to determine list length
        if limit == 0:
            pass
        else:
            self.link_list = self.link_list[0:limit]
        print(self.link_list)
        return self.link_list

    def sel_get_url(self, url: str):

        """Use selenium to navigate to a chosen url.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        url - desired url as string
        """

        driver = self.driver
        driver.get(url)
        time.sleep(4)

    def sel_send_keys_id(self, element_id: str, keys: str):

        """Use selenium to send keys to a chosen element on the page.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        element_id - the id of the element to send keys to, string
        keys - characters to send to the page element, string
        """

        driver = self.driver
        driver.find_element_by_id(element_id).send_keys(keys)

    def sel_click_xpath(self, xpath: str):

        """Use selenium to click an element, identified by xpath.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        xpath - the xpath address of the element to click
        """

        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            return None

    def sel_click_id(self, id: str):

        """Use selenium to click an element, identified by id.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        id - the id of the element to click
        """

        driver = self.driver
        driver.find_element_by_id(id).click()


    def sel_links_from_table(self, table_class_name: str,
                             element_class_name: str,
                             link_attribute: str) -> list:
        """Use selenium to retrieve links stored in a table.
        Nested 3 layers deep from the page -> table -> element -> link

        Keyword arguments:
        -----------------
        driver -- the selenium webdriver of choice
        table_class_name -- string identifying the data table
        element_class_name -- string identifying the class of the element
        link_attribute -- string identifying the attribute of the link in
                          the element

        Returns:
        -------
        list of links
        """

        driver = self.driver
        link_table = driver.find_element_by_class_name(table_class_name)

        link_list = link_table.find_elements_by_class_name(element_class_name)

        temp_link_list = []

        for item in link_list:
            # link = item.find_element_by_tag_name('a')
            temp_link_list.append(item.get_attribute(link_attribute))

        self.link_list.append(temp_link_list)
        return self.link_list

    def download_image(self, url: str, filename: str) -> image:

        """Downloads image from a url and saves
        to a filename. Uses url which contains
        only an image. Filepath can be adjusted
        below.

        Keyword arguments:
        ------------------
        url: desired image url, string
        filename: desired image filename, string
        see below to adjust filepath,
        could use arguments to specificy this if desired
        """

        r = requests.get(url, stream=True)

        # Open a local file with wb ( write binary ) permission.
        with open(f'./Data/Images/{filename}', 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    def save_results(self, data, filename: str) -> json:

        """ Saves results objects to JSON format.

        Keyword arguments:
        ------------------
        data - a resulting data object, list, dictionary etc
        filename -  desired name of file,
                    which in this case includes the desired directory path
        """

        with open(filename, mode='w') as f:
            json.dump(data, f)

        return

    if __name__ == "__main__":
        print('done!')
        pass
