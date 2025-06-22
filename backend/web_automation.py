# backend/web_automation.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from voice_utils import speak

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def play_video_on_youtube(product):
    speak("Opening YouTube")
    driver = get_driver()
    driver.get("https://www.youtube.com")
    try:
        time.sleep(3)
        box = driver.find_element(By.NAME, "search_query")
        box.send_keys(product)
        box.send_keys(Keys.ENTER)
        time.sleep(3)
        box1 = driver.find_element(By.ID, "video-title")
        box1.click()
        speak("Playing the video now")
        return f"Playing {product} on YouTube."
    except Exception as e:
        print("Error:", e)
        speak("Could not play the video.")
        return "Error in playing video."

def order_product(product, platform):
    speak(f"Opening {platform} to order {product}")
    driver = get_driver()
    driver.get("https://www.google.com")
    try:
        box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        box.send_keys(platform)
        box.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@id="search"]//a)[1]'))
        ).click()
        time.sleep(3)

        if platform == 'amazon':
            search_box = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            search_box.send_keys(product)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]')[0].click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="addToCart_feature_div"]').click()
            speak("Product added to cart on Amazon.")
            return "Added to Amazon cart."

        elif platform == 'flipkart':
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
            )
            search_box.send_keys(product)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]')[0].click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li[1]').click()
            speak("Product added to cart on Flipkart.")
            return "Added to Flipkart cart."
    except Exception as e:
        print("Order error:", e)
        speak("There was a problem placing your order.")
        return "Order failed."

def order_food_on_platform(food_item, restaurant, location, platform):
    speak(f"Ordering {food_item} from {restaurant} in {location} on {platform}")
    driver = get_driver()

    if platform == "swiggy":
        driver.get("https://www.swiggy.com")
    elif platform == "zomato":
        driver.get("https://www.zomato.com")
    else:
        speak("Unsupported food platform.")
        return "Unsupported platform."

    try:
        time.sleep(5)
        loc_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'location')]")
        loc_box.send_keys(location)
        time.sleep(2)
        loc_box.send_keys(Keys.DOWN)
        loc_box.send_keys(Keys.ENTER)
        time.sleep(5)
        search = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")
        search.send_keys(restaurant)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_elements(By.XPATH, "//a[contains(@href,'/restaurant')]")[0].click()
        time.sleep(5)
        driver.find_element(By.XPATH, f"//*[contains(text(), '{food_item}')]").click()
        speak(f"Ordered {food_item} from {restaurant}")
        return f"Ordered {food_item} from {restaurant}"
    except Exception as e:
        print("Order error:", e)
        speak("There was a problem placing your order.")
        return "Food order failed."

def search_google(query):
    driver = get_driver()
    driver.get("https://www.google.com")
    try:
        box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        box.send_keys(query)
        box.send_keys(Keys.ENTER)
        time.sleep(3)
        return f"Searching Google for {query}"
    except Exception as e:
        print("Error while searching Google:", e)
        speak("I couldn't search Google.")
        return "Google search failed."
