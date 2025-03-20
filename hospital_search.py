import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# 병원 이름을 검색하는 함수
def search_hospital(hospital_name):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 웹드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 검색할 사이트 목록
    sites = [
        "https://clinicmarket.goodoc.co.kr/",
        "https://www.onemoawf.net/",
        "https://mediwelfare5.net/",
        "https://cashdoc.me/home",
        "https://www.gangnamunni.com/",
        "https://web.babitalk.com/",
        "https://www.yeoshin.co.kr/",
    ]

    for i, site in enumerate(sites):
        try:
            if i == 0:
                driver.get(site)  # 첫 번째 사이트는 기존 탭에서 열기
            else:
                driver.execute_script(f"window.open('{site}', '_blank');")  # 새 탭에서 열기
                driver.switch_to.window(driver.window_handles[-1])  # 새 탭으로 이동

            if site == "https://www.gangnamunni.com/":
                # 강남언니 검색창 클릭 (Placeholder 요소)
                search_placeholder = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "SearchInput__StyledPlaceholderText-sc-8a2a154-1"))
                )
                search_placeholder.click()  # 클릭하여 검색 입력창 활성화
                
                # 실제 검색창 찾기
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
                )

            elif site == "https://web.babitalk.com/":
                # 바비톡 검색창 UI 요소 클릭 (검색창 활성화)
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.text-base.font-medium.w-full"))
                )

            elif site in ["https://www.yeoshin.co.kr/", "https://cashdoc.me/home"]:
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )

            elif site in ["https://www.onemoawf.net/", "https://mediwelfare5.net/"]:
                # 일반적인 사이트는 name="keyword"를 찾음
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "keyword"))
                )

            if site != "https://clinicmarket.goodoc.co.kr/":  # Goodoc은 검색이 아니라 텍스트 확인이므로 제외
                search_box.send_keys(hospital_name)
                search_box.send_keys(Keys.RETURN)

        except Exception as e:
            print(f"Error on site {site}: {e}")

    print("검색 완료.\n캐시닥, 서울메디컬, 원모아, 굿닥은 안 나올 시 진료과 탭으로 이동하여 있는지 찾기.\n굿닥은 다른 창에서 대학생 인증된(로그인 된) 창에서 하기.")  # 안내 메시지 출력

# 사용자로부터 병원명 입력 받기
hospital_name = input("검색할 병원명을 입력하세요: ")
search_hospital(hospital_name)
