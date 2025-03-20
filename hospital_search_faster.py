import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

COOKIE_FILE = "safedoc_cookies.pkl"

# 세이프닥 쿠키로 로그인 유지하는 함수
def load_safedoc_with_cookies(driver):
    driver.get("https://safedoc.io/sign")  # 세이프닥 로그인 페이지

    try:
        # 저장된 쿠키 불러오기
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        # 쿠키 적용 후 새로고침 (로그인 유지됨)
        driver.refresh()
        print("세이프닥 쿠키 적용 완료. 로그인 유지됨.")

    except FileNotFoundError:
        print("⚠️ 쿠키 파일 없음. 세이프닥 수동 로그인 후 쿠키 저장 필요!")
        time.sleep(20)  # 사용자가 직접 로그인할 시간 제공

        # 로그인 후 쿠키 저장
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
        print("로그인 완료. 쿠키 저장됨.")

# 병원 이름을 검색하는 함수
def search_hospital(hospital_name):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 웹드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    load_safedoc_with_cookies(driver)

    # 검색할 사이트 목록
    sites = [
        "https://clinicmarket.goodoc.co.kr/",
        f"https://safedoc.io/hospital/search/keyword?q={hospital_name}&tab=hospital",
        f"https://www.onemoawf.net/product/search.html?banner_action=&keyword={hospital_name}",
        f"https://mediwelfare5.net/product/search.html?banner_action=&keyword={hospital_name}&order_by=priceasc",
        f"https://cashdoc.me/search?searchType=TOTAL&keyword={hospital_name}",
        f"https://www.gangnamunni.com/search?q={hospital_name}",
        f"https://web.babitalk.com/search?keyword={hospital_name}",
        f"https://www.yeoshin.co.kr/search/category?q={hospital_name}&tab=events",
    ]

    for i, site in enumerate(sites):
        try:
            if i == 0:
                driver.get(site)  # 첫 번째 사이트는 기존 탭에서 열기
            else:
                driver.execute_script(f"window.open('{site}', '_blank');")  # 새 탭에서 열기
                driver.switch_to.window(driver.window_handles[-1])  # 새 탭으로 이동

        except Exception as e:
            print(f"Error on site {site}: {e}")

    print("검색 완료.\n캐시닥, 서울메디컬, 원모아, 굿닥, 세이프닥은 안 나올 시 진료과 탭으로 이동하여 있는지 찾기.")  # 안내 메시지 출력


# 사용자로부터 병원명 입력 받기
hospital_name = input("검색할 병원명을 입력하세요: ")
search_hospital(hospital_name)