# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import logging
import time
import csv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def fetch(patent_num):
    url = 'https://patents.google.com/patent/' + patent_num
    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Fetched {url}")
        parse(url, response)

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        with open('error.txt', mode='a', encoding='utf-8') as f:
            f.write(url + '\n')


def parse(url, response):
    soup = BeautifulSoup(response.text, "lxml")
    field_dict = {
        'title': '',
        'abstract': '',
        'inventors': '',
        'application_number': '',
        'publication_number': '',
        'publication_date': '',
        'pdf_url': '',
        'assignee_current': '',
        'claims_texts': '',
        'events': [],
        'classifications': [],
        'descriptions': '',
        'patent_citations': [],
        'non_patent_citations': [],
        'city_bys': [],
        'similar_documents': [],
        'legal_events': [],
        'concepts': []
    }

    # title
    title_span = soup.find("span", {"itemprop": "title"})
    if title_span:
        field_dict["title"] = title_span.text.strip()
    else:
        return None

        # Extracting other fields
    field_dict["pdf_url"] = soup.find('a', {'itemprop': 'pdfLink'})['href'] if soup.find('a', {
        'itemprop': 'pdfLink'}) else ''
    field_dict["abstract"] = soup.find(class_="abstract").text.strip() if soup.find(class_="abstract") else ''
    field_dict["inventors"] = ', '.join([i.text.strip() for i in soup.findAll(itemprop="inventor")])
    field_dict["assignee_current"] = ', '.join([i.text.strip() for i in soup.findAll(itemprop="assigneeCurrent")])
    field_dict["publication_number"] = soup.find(itemprop="publicationNumber").text.strip() if soup.find(
        itemprop="publicationNumber") else ''
    field_dict["publication_date"] = soup.find(itemprop="publicationDate").text.strip() if soup.find(
        itemprop="publicationDate") else ''
    field_dict["application_number"] = soup.find(itemprop="applicationNumber").text.strip() if soup.find(
        itemprop="applicationNumber") else ''

    # events
    events = soup.find_all(itemprop="events")
    if events:
        for event in events:
            event_document_id = event.find(itemprop="documentId")
            event_dict = {
                "date": event.find(itemprop="date").text.strip() if event.find(itemprop="date") else "",
                "title": event.find(itemprop="title").text.strip() if event.find(itemprop="title") else "",
                "type": event.find(itemprop="type").text.strip() if event.find(itemprop="type") else "",
                "document_id": event_document_id.text.strip() if event_document_id else "",
            }
            field_dict["events"].append(event_dict)

    classifications_list = soup.find_all("li", itemprop='classifications')
    if classifications_list:
        for classifications in classifications_list:
            classifications_dict = {
                "code": classifications.find(itemprop='Code').text.strip(),
                "description": classifications.find(itemprop='Description').text.strip()
            }
            field_dict["classifications"].append(classifications_dict)

    claims_texts_div = soup.find(class_="claims")
    if claims_texts_div:
        field_dict["claims_texts"] = claims_texts_div.text.strip()
    description_div = soup.find(class_="description")
    if description_div is None:
        logging.error("Unable to parse text:", url)

    content_dict = {}
    headings = description_div.find_all("heading")
    if headings is None or len(headings) == 0:
        split_tag_list = ["background-art", "disclosure", "description-of-drawings", "mode-for-invention"]
        invention_title = soup.find('invention-title')
        if invention_title is None:
            div_list = description_div.find_all(class_="description-paragraph")
            content_dict["description"] = '\n'.join([i.text.strip() for i in div_list])
        else:
            background_art = description_div.find("background-art")
            tmp_list = []
            sibling = invention_title.find_next_sibling()
            while sibling and sibling != background_art:
                tmp_list.append(sibling.text.strip())
                sibling = sibling.find_next_sibling()
            content_dict["交叉引用"] = "\n".join(tmp_list[1:])
            for tag in split_tag_list:
                tag_obj = description_div.find(tag)
                if tag_obj or len(tag_obj) > 1:
                    div_list = tag_obj.find_all(class_="description-paragraph")
                    content_dict[div_list[0].text.strip()] = '\n'.join([i.text.strip() for i in div_list[1:]])
    else:
        for heading in headings:
            content_list = []
            next_element = heading.find_next_sibling()
            while next_element and next_element.name != 'heading':
                if next_element.name is not None:
                    content_list.append(next_element.get_text().strip())
                next_element = next_element.find_next_sibling()
            content_dict[heading.get_text().strip()] = "\n".join(content_list)
    field_dict["descriptions"] = content_dict
    patent_citations = soup.find_all("tr", {"itemprop": "backwardReferencesOrig"})
    if patent_citations is None or len(patent_citations) == 0:
        patent_citations = soup.find_all("tr", {"itemprop": "backwardReferencesFamily"})
    for patent_citation in patent_citations:
        assignee_original_obj = patent_citation.find("span", {"itemprop": "assigneeOriginal"})
        patent_citation_dict = {
            "publication_number": patent_citation.find("span", {"itemprop": "publicationNumber"}).text.strip(),
            "primary_language": patent_citation.find("span", {"itemprop": "primaryLanguage"}).text.strip(),
            # "url": base_url + patent_citation.find("a")['href'],
            "priority_date": patent_citation.find("td", {"itemprop": "priorityDate"}).text.strip(),
            "publication_date": patent_citation.find("td", {"itemprop": "publicationDate"}).text.strip(),
            "assignee_original": "" if assignee_original_obj is None else assignee_original_obj.text.strip(),
            "title": patent_citation.find("td", {"itemprop": "title"}).text.strip(),
        }
        field_dict["patent_citations"].append(patent_citation_dict)
    non_patent_citations = soup.find_all("tr", {"itemprop": "detailedNonPatentLiterature"})
    if non_patent_citations:
        for non_patent_citation in non_patent_citations:
            # non_patent_citation.find("a")['href'],
            non_patent_citation_dict = {
                # "url": non_patent_citation.find("a")['href'],
                "title": non_patent_citation.find("span", {"itemprop": "title"}).text.strip(),
            }
            field_dict["non_patent_citations"].append(non_patent_citation_dict)
    city_bys = soup.find_all("tr", {"itemprop": "forwardReferencesFamily"})
    if city_bys is None or len(city_bys) == 0:
        city_bys = soup.find_all("tr", {"itemprop": "forwardReferencesOrig"})
    for city_by in city_bys:
        city_by_original_obj = city_by.find("span", {"itemprop": "assigneeOriginal"})
        city_by_dict = {
            "publication_number": city_by.find("span", {"itemprop": "publicationNumber"}).text.strip(),
            "primary_language": city_by.find("span", {"itemprop": "primaryLanguage"}).text.strip(),
            # "url": base_url + city_by.find("a")['href'],
            "priority_date": city_by.find("td", {"itemprop": "priorityDate"}).text.strip(),
            "publication_date": city_by.find("td", {"itemprop": "publicationDate"}).text.strip(),
            "assignee_original": "" if city_by_original_obj is None else city_by_original_obj.text.strip(),
            "title": city_by.find("td", {"itemprop": "title"}).text.strip(),
        }
        field_dict["city_bys"].append(city_by_dict)
    similar_documents = soup.find_all("tr", {"itemprop": "similarDocuments"})
    if similar_documents:
        for similar_document in similar_documents:
            publication_number = ''
            scholar_id = ''
            primary_language = ''
            publication_date = ''
            if similar_document.find("meta", {"itemprop": "isScholar"}):
                type = "scholar"
                scholar_id = similar_document.find("meta", {"itemprop": "scholarID"})["content"]
            else:
                type = "patent"
                primary_language_span = similar_document.find("span", {"itemprop": "primaryLanguage"})
                if primary_language_span:
                    primary_language = primary_language_span.text.strip()
                publication_number_span = similar_document.find("span", {"itemprop": "publicationNumber"})
                if publication_number_span:
                    publication_number = publication_number_span.text.strip()
            publication_date_time = similar_document.find("time", {"itemprop": "publicationDate"})
            if publication_date_time:
                publication_date = publication_date_time.text.strip()
            similar_document_dict = {
                "type": type,
                "scholar_id": scholar_id,
                "publication_number": publication_number,
                "primary_language": primary_language,
                # "url": base_url + similar_document.find("a")['href'],
                "publication_date": publication_date,
                "title": similar_document.find("td", {"itemprop": "title"}).text.strip(),
            }
            field_dict["similar_documents"].append(similar_document_dict)
    legal_events = soup.find_all("tr", {"itemprop": "legalEvents"})

    if legal_events:
        for legal_event in legal_events:
            legal_event_dict = {
                "date": legal_event.find("time", {"itemprop": "date"}).text.strip(),
                "code": legal_event.find("td", {"itemprop": "code"}).text.strip(),
                "title": legal_event.find("td", {"itemprop": "title"}).text.strip(),
                "attributes": '\n'.join(
                    [i.text.strip().replace("\n", "") for i in legal_event.findAll("p", itemprop="attributes")]),
            }
            field_dict["legal_events"].append(legal_event_dict)

    concepts_ul = soup.find("ul", {"itemprop": "concept"})
    if concepts_ul:
        for concept in concepts_ul.find_all("li", {"itemprop": "match"}):
            concept_dict = {
                "id": concept.find("span", {"itemprop": "id"}).text.strip(),
                "name": concept.find("span", {"itemprop": "name"}).text.strip(),
                "sections": ', '.join([i.text.strip() for i in concept.find_all("span", itemprop="sections")]),
                "similarity": concept.find("span", {"itemprop": "similarity"}).text.strip(),
                "count": concept.find("span", {"itemprop": "count"}).text.strip(),
            }
            field_dict["concepts"].append(concept_dict)

    pipline(field_dict)


def pipline(field_dict):
    # print(field_dict)
    ...


def main():
    with open(file='output_10000.txt', mode='r', encoding='utf-8') as f:
        patent = f.read()

    patent_list = patent.split(',')

    # Split the list into chunks of 20 patents
    chunk_size = 20
    chunks = [patent_list[i:i + chunk_size] for i in range(0, len(patent_list), chunk_size)]

    # Create a thread pool and execute the fetch function
    with ThreadPoolExecutor(max_workers=20) as executor:
        for i, chunk in enumerate(chunks):
            executor.map(fetch, chunk)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        logging.error(f"An error occurred: {error}.")
