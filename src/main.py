import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, EXPECTED_STATUS, PEP_URL
from outputs import control_output
from utils import find_tag, get_response, unexpected_status


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})

    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})

    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор'),]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        result.append(
            (version_link, h1.text, dl_text)
        )
    return result


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in tqdm(ul_tags):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python\s([\d\.]+)\s\((\w{1,}.*)\)'
    for a_tag in tqdm(a_tags):
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    download_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, download_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(download_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    pep_counter = {}
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    body_table = find_tag(section_tag, 'tbody')
    rows = body_table.find_all('tr')
    results = [('Статус', 'Количество')]
    for row in tqdm(rows[1:]):
        first_tag = find_tag(row, 'td')
        preview_status = first_tag.text[1:]
        a_tag = find_tag(row, 'a')
        href = a_tag['href']
        pep_link = urljoin(PEP_URL, href)
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        dl = find_tag(soup, 'dl')
        dt_tags = dl.find_all('dt')
        for dt in dt_tags:
            if dt.text == 'Status:':
                dt_status = dt
                break
        pep_status = dt_status.find_next_sibling('dd').string
        status_counter = pep_counter.get(pep_status) or 0
        pep_counter[pep_status] = status_counter + 1
        if pep_status not in EXPECTED_STATUS[preview_status]:
            unexpected_status(
                pep_link, pep_status, EXPECTED_STATUS[preview_status])
    for item in pep_counter.items():
        results.append(item)
    results.append(('Total', len(rows[1:])))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
