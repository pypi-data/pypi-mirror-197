import requests
import logging
from typing import List
from datetime import datetime


class DartAPI:
    def __init__(self, keys: List):
        self.keys: DartKeys = DartKeys(keys)

    def get_disclosure_list(self, end_de, depth=1):
        """
        :param end_de:
        :param depth:
        :return: rcp_no 내림차순 순으로 정렬된 공시 리스트
        """
        results = []
        hasMore = True
        page = 1
        total_page = 1
        page_no = 0

        while hasMore and depth > 0:
            json_data = self.get_disclosure(end_de=end_de, page=page)
            status = json_data.get("status")

            if status == '013':  # 조회된 데이터가 없습니다
                logging.info("no data")
                break
            elif status == '012':  # 접근할 수 없는 IP입니다.
                logging.error(f"접근할 수 없는 IP key")
                # self.dart_api.disable_key(key)
                # not increase page
            elif status == '020':  # API key 한도 초과
                logging.error(f"{status} API key 한도 초과 key")
                # self.dart_api.disable_key(key)
                # not increase page
            elif status == '021':
                logging.error(f"{status} 조회 가능한 회사 개수가 초과하였습니다.(최대 100건)")
            elif status == '100':
                logging.error(f"{status} 조회 가능한 회사 개수가 초과하였습니다.(최대 100건)")
            elif status == '101':
                logging.error(f"{status} 부적절한 접근입니다.")
            elif status == '800':
                logging.error(f"{status} 조회 가능한 회사 개수가 초과하였습니다.(최대 100건)")
            elif status == '900':
                logging.error(f"{status} 정의되지 않은 오류가 발생하였습니다.")
            elif status == '901':
                logging.error(f"{status} 사용자 계정의 개인정보 보유기간이 만료되어 사용할 수 없는 키입니다. 관리자 이메일(opendart@fss.or.kr)로 문의하시기 바랍니다.")
            elif status == '000':  # 정상조회
                page_no = json_data.get("page_no")
                page_count = json_data.get("page_count")
                total_count = json_data.get("total_count")
                total_page = json_data.get("total_page")
                page = page + 1
                logging.info(f"정상조회 total_count : {total_count}, total_page : {total_page}, page_count : {page_count}, page_no : {page_no}")
                results.extend(json_data.get("list"))
            else:
                logging.error(f"처리안된 예외 케이스 status : {status}")

            depth = depth - 1

            if total_page == page_no:
                break

        list_items = []

        for item in results:
            # 각 항목별로 데이터 추출
            rcept_dt = item.get('rcept_dt', '')

            data = {
                "company": item.get('corp_name', ''),
                "market": item.get('corp_cls', ''),
                "title": item.get('report_nm', ''),
                "code": item.get('stock_code', ''),
                "rcp_no": item.get('rcept_no', ''),
                "rcept_dt": rcept_dt[:4] + '.' + rcept_dt[4:6] + '.' + rcept_dt[6:],
            }
            list_items.append(data)

        list_items.sort(key=lambda x: int(x.get('rcp_no')[-4:]), reverse=True)  ## 내림차순 정렬
        logging.debug(
            f"sorted list_item rcp_no from : {list_items[0].get('rcp_no')}, to : {list_items[-1].get('rcp_no')}")

        return list_items

    def get_disclosure(self, end_de, page=1, page_count=100):
        key = self.keys.next_key()
        logging.info(f"fetching data  date : {end_de}, page : {page}, withkey : {key}")
        param = {
            'crtfc_key': key,
            'page_count': page_count,
            'page_no': page,
            'end_de': end_de
        }
        return requests.get("https://opendart.fss.or.kr/api/list.json", params=param).json()

    def get_document_zip_bytes(self, rcp_no):
        key = self.keys.next_key()
        logging.info(f"fetching data  rcp_no : {rcp_no}, withkey : {key}")
        param = {
            'crtfc_key': key,
            'rcept_no': rcp_no
        }
        response = requests.get("https://opendart.fss.or.kr/api/document.xml", params=param)
        return response.content

    def disable_key(self, key):
        self.keys.disable_key(key)


class DartKey:
    def __init__(self, key: str, disabled=False, disabledAt=None):
        self.key = key
        self.disabled = disabled
        self.disabledAt = disabledAt

    def __str__(self):
        return f"key : {self.key}, disabled : {self.disabled}, at : {self.disabledAt}"


class DartKeys:
    def __init__(self, keys: List):
        self.current = 0
        self.keys = list(map(lambda key: DartKey(key), keys))
        logging.info(f"keys {self}")

    def next_key(self):
        available_keys = list(filter(lambda x : not x.disabled, self.keys))
        logging.debug(f"available keys : {(','.join([str(elem) for elem in available_keys]))}")

        if self.current >= len(available_keys) - 1:
            self.current = 0

        key = available_keys[self.current].key
        self.current = self.current + 1
        return key

    def disable_key(self, keycode):
        for dartkey in self.keys:
            if dartkey.key == keycode:
                dartkey.disabled = True
                dartkey.disabledAt = datetime.now()
                logging.info(f"dart key {keycode} DISABLED")

    def __str__(self):
        return "\n".join(list(map(lambda key: f"{key}", self.keys)))