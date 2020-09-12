from selenium import webdriver
import time
import json

def crawl_ridibooks(driver, targets):
    # get first address
    uncrawled_targets = [target for target in targets if not target['crawled']]
    target = uncrawled_targets.pop(0)
    url = target['url']
    depth = target['depth']

    for i, t in enumerate(targets):
        if t['url'] == url:
            targets[i]['crawled'] = True

    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 1/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 2/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 3/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 4/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 5/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 5/5);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 5/5);")
    time.sleep(1.5)

    # driver를 만든 후 implicitly_wait 값(초단위)을 넣어주세요.
    # driver.get('https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=251281173')

    retval = []

    title = driver.find_element_by_css_selector('h3.info_title_wrap').text
    author = driver.find_element_by_css_selector('h4.author_name').text

    try:
        introduce_book = driver.find_element_by_css_selector('#introduce_book')
        retval.append(dict(src='ridi', title=title, author=author, depth=depth, type='introduction', content=introduce_book.text))
    except:
        pass

    try:
        publisher_book_review = driver.find_element_by_css_selector('#publisher_book_review')
        retval.append(dict(src='ridi', title=title, author=author, depth=depth, type='review', content=publisher_book_review.text))
    except:
        pass

    try:
        purchase_similar_books_links = driver.find_elements_by_css_selector("article#purchase_similar_books>div.detail_block>div>div.book_metadata_wrapper>h3>a")
        # purchase_similar_books  = driver.find_elements_by_css_selector("article#purchase_similar_books>div.detail_block>div>div.book_metadata_wrapper")
        for t in purchase_similar_books_links:
            url = t.get_attribute('href')
            visited = False
            for target in targets:
                if target['url'] == url:
                    target['frequency'] += 1
                    visited = True
                    break

            if not visited:
                targets.append(dict(depth=depth+1, url=t.get_attribute('href'), crawled=False, frequency=0))
    except:
        pass

    # try:
    #     view_similar_books_links = driver.find_elements_by_css_selector("article#view_similar_books>div.detail_block>div>div.book_metadata_wrapper>h3>a")
    #     # view_similar_books = driver.find_elements_by_css_selector("article#view_similar_books>div.detail_block>div>div.book_metadata_wrapper")
    #     for t in view_similar_books_links:
    #         url = t.get_attribute('href')
    #         visited = False
    #         for target in targets:
    #             if target['url'] == url:
    #                 target['frequency'] += 1
    #                 visited = True
    #                 break
                # if not visited:
                #     urls.append(dict(depth=depth+1, url=t.get_attribute('href'), crawled=False, frequency=1))
    # except:
    #     pass
    
    return retval



class g():
    MAX_ITR = 30

if __name__ == "__main__":
    driver = webdriver.Chrome('/Users/hc/Dropbox/Projects/crawler/sources/chromedriver')
    
    count = 0
    results = []
    urls = [dict(url='https://ridibooks.com/books/371002104?_s=category_best&_s_id=509000862', depth=0, frequency=1, crawled=False)]

    while(1):
        if count >= g.MAX_ITR:
            break
        results += crawl_ridibooks(driver, urls)
        count += 1
        # break
    
    driver.quit()

    with open("ridibooks.json", mode='w', encoding='UTF-8-sig') as f:
        json.dump(results, f, ensure_ascii=False)

    with open("ridibooks_urls.json", mode='w', encoding='UTF-8-sig') as f:
        json.dump(urls, f, ensure_ascii=False)

        

# for l in view_similar_books_links:
#     print()==

driver.quit()