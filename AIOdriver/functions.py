import os
import requests
import zipfile
import subprocess
import re
import sys
import urllib



def download_chromedriver():

    chrome_driver_url = "https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.58/win64/chrome-win64.zip"
    chrome_driver="https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.58/win64/chromedriver-win64.zip"
    downlodable_content={'chromdriver':chrome_driver,'chromedriver-win64':chrome_driver_url}

    for content in downlodable_content:

        zip_path = r'C:\new_chrome\{}.zip'.format(content)  
        extract_path = r'C:\new_chrome\extract'                  

        os.makedirs(extract_path, exist_ok=True)

        urllib.request.urlretrieve(downlodable_content[content], zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        os.remove(zip_path)

        print(f"ChromeDriver extracted to: {extract_path}")


def get_edge_version():
    try:
        version_output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version', shell=True
        ).decode('utf-8')
        version = re.search(r'version\s+REG_SZ\s+([\d.]+)', version_output, re.IGNORECASE)
        if version:
            return version.group(1)
        else:
            raise ValueError("Edge version not found.")
    except Exception as e:
        print(f"Error getting Edge version: {str(e)}")
        return None


def get_edgedriver_version(edge_version):
    major_version = edge_version.split('.')[0]
    url = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}"
    print(url)
    try:
        response = requests.get(url)
        print(response.text.strip())
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Edge WebDriver version for Edge {major_version}: {e}")
        return None


def download_and_extract_edgedriver(version, extract_to):
    download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"  
    
    try:
        print(f"Downloading Edge WebDriver from {download_url}...")
        response = requests.get(download_url)
        response.raise_for_status()

        # Save the zip file
        zip_file_path = os.path.join(extract_to, "edgedriver.zip")
        with open(zip_file_path, "wb") as file:
            file.write(response.content)
        
        # Extract the contents to the desired folder
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        os.remove(zip_file_path)  # Clean up by removing the zip file after extraction
        print(f"Edge WebDriver extracted to: {extract_to}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading Edge WebDriver: {e}")


def createwebdriver(driver,crawler_type='osa',driver_type="chrome"):

    if crawler_type=='bh' or crawler_type=='rr':

        if driver_type=="edge":
            edge_version = get_edge_version() #Downloading the Edge driver 
            try:
                with open(r'C:\new_edge\current_version.txt') as file:
                    current_ver=str(file.read().strip())
            except:
                current_ver=''
            print("Current Edge Version : ",current_ver)
            if edge_version!=current_ver:
                print(f"Detected Edge version: {edge_version}")
                edgedriver_version = get_edgedriver_version(edge_version)
                if edgedriver_version:
                    extract_path = r"C:\new_edge\extract"  
                    if not os.path.exists(extract_path):
                        os.makedirs(extract_path)
                    print(f"Downloading Edge WebDriver version: {edgedriver_version}")
                    try:
                        download_and_extract_edgedriver(edge_version, extract_path)
                    except:
                        download_and_extract_edgedriver(edgedriver_version, extract_path)
                    with open(r'C:\new_edge\current_version.txt','w') as file:
                        file.write(edgedriver_version)
                else:
                    print("Failed to get Edge WebDriver version.")
            else:
                print("Already on latest version")

            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            edge_driver_path=r"C:\new_edge\extract\msedgedriver.exe"
            service = Service(edge_driver_path)
            try:
                driver = webdriver.Edge(service=service)
            except:
                driver=webdriver.Edge(executable_path=edge_driver_path)
            print("successfully created Edge instance")
            return driver 
          
        elif driver_type=="chrome":

            chromedriver_win64_path=r'C:\new_chrome\extract\chromedriver-win64'
            chrome_win64_path=r'C:\new_chrome\extract\chrome-win64'
            if not os.path.exists(chrome_win64_path) and not os.path.exists(chromedriver_win64_path):
                download_chromedriver()
            else:
                print("Setup already present")
            def install(package):
                os.system('pip install blinker==1.7.0')
                os.system('pip install {}'.format(package))

            try:
                from seleniumwire import webdriver
            except:
                install('selenium-wire')
            
            from seleniumwire import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options

            options = {
            'headers': {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
                "Accept-Encoding": "gzip, deflate, br, zstd", 
                "Accept-Language": "en-US,en;q=0.9", 
                "Priority": "u=0, i", 
                "Sec-Ch-Ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"", 
                "Sec-Ch-Ua-Mobile": "?0", 
                "Sec-Ch-Ua-Platform": "\"Windows\"", 
                "Sec-Fetch-Dest": "document", 
                "Sec-Fetch-Mode": "navigate", 
                "Sec-Fetch-Site": "cross-site", 
                "Sec-Fetch-User": "?1", 
                "Upgrade-Insecure-Requests": "1", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", 
                "X-Amzn-Trace-Id": "Root=1-66ed0eb2-3c09e85b31bbd0d66ad02596"
            }
        
            }
            chrome_options = Options()
            chrome_options.binary_location=r'C:\new_chrome\extract\chrome-win64\chrome.exe'
            service = Service(executable_path=r'C:\new_chrome\extract\chromedriver-win64\chromedriver.exe')
            driver = webdriver.Chrome(seleniumwire_options=options,service=service,options=chrome_options)
            print("successfully created wire instance")
            return driver
        
        elif driver_type=="uc":
            import undetected_chromedriver as uc
            options = uc.ChromeOptions()
            prefs = {"profile.default_content_settings.geolocation": 2}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--deny-permission-prompts")
            driver = uc.Chrome(options=options)
            return driver

    else:    
        if driver_type=="chrome":
            from selenium.webdriver.chrome.options import Options
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            try:
                driver.close()
                driver.quit()
            except:
                pass
            
            print('in createwebdriver')
            chrome_options = Options()
            chrome_options.binary_location="C:\\chrome-win64\\chrome.exe"

            try:
                driver = webdriver.Chrome(service=service,options=chrome_options)
            except:
                try:

                    print('IN EXCEPTION')
                    service = Service(r"C:\olddriver\chromedriver.exe")
                    driver = webdriver.Chrome(service=service,options=chrome_options)
                except:
                    chromedriver_win64_path=r'C:\new_chrome\extract\chromedriver-win64'
                    chrome_win64_path=r'C:\new_chrome\extract\chrome-win64'

                    if not os.path.exists(chrome_win64_path) and not os.path.exists(chromedriver_win64_path):
                        download_chromedriver()
                    else:
                        print("Setup already present")

                    chrome_options.binary_location="C:\\new_chrome\\extract\\chrome-win64\\chrome.exe"
                    service = Service(r"C:\new_chrome\extract\chromedriver-win64\chromedriver.exe")
                    driver = webdriver.Chrome(service=service,options=chrome_options)

            driver.maximize_window()
            driver.get('chrome://settings/')
            driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.7);')

            return driver
        
        elif driver_type=='edge':
            edge_version = get_edge_version() #Downloading the Edge driver 
            try:
                with open(r'C:\new_edge\current_version.txt') as file:
                    current_ver=str(file.read().strip())
            except:
                current_ver=''
            print("Current Edge Version : ",current_ver)
            if edge_version!=current_ver:
                print(f"Detected Edge version: {edge_version}")
                edgedriver_version = get_edgedriver_version(edge_version)
                if edgedriver_version:
                    extract_path = r"C:\new_edge\extract"  
                    if not os.path.exists(extract_path):
                        os.makedirs(extract_path)
                    print(f"Downloading Edge WebDriver version: {edgedriver_version}")
                    try:
                        download_and_extract_edgedriver(edge_version, extract_path)
                    except:
                        download_and_extract_edgedriver(edgedriver_version, extract_path)
                    with open(r'C:\new_edge\current_version.txt','w') as file:
                        file.write(edgedriver_version)
                else:
                    print("Failed to get Edge WebDriver version.")
            else:
                print("Already on latest version")
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            edge_driver_path=r"C:\new_edge\extract\msedgedriver.exe"
            service = Service(edge_driver_path)
            try:
                driver = webdriver.Edge(service=service)
            except:
                driver=webdriver.Edge(executable_path=edge_driver_path)
            print("successfully created Edge instance")
            return driver
        
        elif driver_type=="uc":
            import undetected_chromedriver as uc
            options = uc.ChromeOptions()
            prefs = {"profile.default_content_settings.geolocation": 2}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--deny-permission-prompts")
            driver = uc.Chrome(options=options)
            return driver


            

