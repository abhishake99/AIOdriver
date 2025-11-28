import os
import requests
import zipfile
import subprocess
import re
import sys
import urllib
import json
import platform
import shutil

def get_chrome_version():
    try:
        # Check Chrome version based on OS
        if platform.system() == "Windows":
            output = subprocess.check_output(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version', shell=True).decode()
            version = re.search(r"([\d.]+)", output).group(1)
        elif platform.system() == "Darwin":
            output = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True).decode()
            version = re.search(r"([\d.]+)", output).group(1)
        else:  # Linux
            output = subprocess.check_output("google-chrome --version", shell=True).decode()
            version = re.search(r"([\d.]+)", output).group(1)
        return version
    except Exception as e:
        print("Could not get Chrome version:", e)
        return None
    
def get_chromedriver_url(chrome_version):
    all_matching_versions=[]
    chrome_version='.'.join(chrome_version.split('.')[0:3])
    response=requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
    try:
        data = json.loads(response.text)
        for ver in data['versions']:
            if chrome_version in ver['version']:
                all_matching_versions.append({ver['version']:ver['downloads']['chromedriver'][-1]['url']})
        print(list(all_matching_versions[-1].values())[0])
        return list(all_matching_versions[-1].values())[0],list(all_matching_versions[-1].keys())[0]
    except:
        return ''

def download_chromedriver(url):
    response = requests.get(url)
    if response.status_code == 200:
        zip_path = "chromedriver.zip"
        with open(zip_path, "wb") as file:
            file.write(response.content)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        
        os.remove(zip_path)
        print("ChromeDriver downloaded and extracted successfully.")
    else:
        print("Failed to download ChromeDriver.")

def copy_chromedriver_to_c(source_folder):
    source_path = os.path.join(source_folder, "chromedriver.exe")
    destination_path = r"C:\latest_chrome_driver"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        print("True")
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"chromedriver.exe has been copied to {destination_path}")
    else:
        print(f"chromedriver.exe not found in {source_folder}")

def c_driver_chromedriver():
    chrome_version = get_chrome_version()
    if chrome_version:
        print("Detected Chrome version:", chrome_version)
        chromedriver_url,fetched_chrome_version = get_chromedriver_url(chrome_version)
        # fetched_chrome_version='.'.join(fetched_chrome_version.split('.')[0:3])
        # chrome_version='.'.join(chrome_version.split('.')[0:3])
        # if fetched_chrome_version!=chrome_version:
        try:
            with open(r'C:\latest_chrome_driver\current_version.txt') as f:
                current_version = str(f.read().strip())
            current_version='.'.join(current_version.split('.')[0:3])
        except:
            current_version = ''
        print(current_version,'.'.join(fetched_chrome_version.split('.')[0:3]))
        if current_version!='.'.join(fetched_chrome_version.split('.')[0:3]):
            if chromedriver_url:
                print("Downloading ChromeDriver...")
                download_chromedriver(chromedriver_url)
                copy_chromedriver_to_c(os.path.join(os.getcwd(),'chromedriver-win64'))
                with open(r'C:\latest_chrome_driver\current_version.txt','w') as file:
                    file.write(fetched_chrome_version)
            else:
                print("Could not determine the ChromeDriver download URL.")
        else:
            print("Local chrome driver is of latest version")
    else:
        print("Chrome is not installed or could not be detected.")


def download_chromedriver_testing_new():
    
    if not os.path.exists(r'C:\new_chrome\current_version.txt'):
        src = r'C:\latest_chrome_driver\current_version.txt'
        dest = r'C:\new_chrome\current_version.txt'
        shutil.copy(src,dest)
        print('copied')
        
    current_version_testing = ''
    current_version = ''
    with open(r'C:\new_chrome\current_version.txt','r') as f:
        current_version_testing = str(f.read().strip())
    
    with open(r'C:\latest_chrome_driver\current_version.txt','r') as f:
        current_version = str(f.read().strip())
        
    if current_version_testing != current_version:
        
        print("New Version Found, Downloading New Version...")

        current_version_testing = current_version
        chrome_exe = f"https://storage.googleapis.com/chrome-for-testing-public/{current_version_testing}/win64/chrome-win64.zip"
        chrome_driver=f"https://storage.googleapis.com/chrome-for-testing-public/{current_version_testing}/win64/chromedriver-win64.zip"
        downlodable_content={'chromdriver':chrome_driver,'chromedriver-win64':chrome_exe}

        for content in downlodable_content:

            zip_path = r'C:\new_chrome\{}.zip'.format(content)  
            extract_path = r'C:\new_chrome\extract'                  

            os.makedirs(extract_path, exist_ok=True)

            urllib.request.urlretrieve(downlodable_content[content], zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            os.remove(zip_path)

            print(f"ChromeDriver extracted to: {extract_path}")
            with open(r'C:\new_chrome\current_version.txt','w') as f:
                    f.write(current_version_testing)
        print("New testing chrome downloaded successfully")  
    else:
        print("Chrome Testing is already on latest version.")

def download_chromedriver_testing_old():

    chrome_exe_url = "https://storage.googleapis.com/chrome-for-testing-public/121.0.6100.0/win64/chrome-win64.zip"
    chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/121.0.6100.0/win64/chromedriver-win64.zip"
    downlodable_content = {'chrome_exe': chrome_exe_url, 'chromedriver': chromedriver_url}
    for content in downlodable_content:

            zip_path = r'C:\old_chrome\{}.zip'.format(content)  
            extract_path = r'C:\old_chrome\extract'                  

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

def driver_initialisation_profile(username='Administrator',profile_directory='Default'):
    
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    user_data_dir = "C:/Users/{0}/AppData/Local/Google/Chrome/User Data".format(username)
    profile_directory = profile_directory
    service = Service(executable_path='C:/latest_chrome_driver/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_directory}")
    options.add_argument("--no-sandbox")  # Add this
    options.add_argument("--disable-dev-shm-usage")  # Add this
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver

def mobile_emulation_driver():
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait

    service = Service(executable_path='C://latest_chrome_driver//chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36')
    chrome_options.add_argument("--window-size=200,1000")
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("force-device-scale-factor=1.5")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def createwebdriver(driver,crawler_type='osa',driver_type="chrome",username='Administrator',profile_directory='Default',use_old_chrome = False):

    if crawler_type=='bh' or crawler_type=='rr':

        if driver_type=="chrome":

            chromedriver_win64_path=r'C:\new_chrome\extract\chromedriver-win64'
            chrome_win64_path=r'C:\new_chrome\extract\chrome-win64'
            if not os.path.exists(chrome_win64_path) and not os.path.exists(chromedriver_win64_path):
                download_chromedriver_testing_new()
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
            chrome_options.add_argument("--start-maximized")
            
            if use_old_chrome == True:
                print('USING OLD CHROME FOR TESTING')
                chrome_options.binary_location="C:\old_chrome\extract\chrome-win64\chrome.exe"
                service = Service(r"C:\old_chrome\extract\chromedriver-win64\chromedriver.exe")
                driver = webdriver.Chrome(service=service,options=chrome_options)
                
            else:
                print('USING NEW CHROME FOR TESTING')
                chromedriver_win64_path=r'C:\new_chrome\extract\chromedriver-win64'
                chrome_win64_path=r'C:\new_chrome\extract\chrome-win64'

                download_chromedriver_testing_new()
                
                chrome_options.binary_location="C:\\new_chrome\\extract\\chrome-win64\\chrome.exe"
                service = Service(r"C:\new_chrome\extract\chromedriver-win64\chromedriver.exe")
                driver = webdriver.Chrome(service=service,options=chrome_options)

            # driver.maximize_window()
            driver.get('chrome://settings/')
            driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.7);')

            return driver
        
        elif driver_type=='edge':
            edge_version = get_edge_version() #Downloading the Edge driver 
            temp_version='.'.join(edge_version.split('.')[:3])
            try:
                with open(r'C:\new_edge\current_version.txt') as file:
                    current_ver=str(file.read().strip())
                    current_ver='.'.join(current_ver.split('.')[:3])
            except:
                current_ver=''
            print("Current Edge Version : ",current_ver)
            if temp_version!=current_ver:
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
        
        elif driver_type=='chrome_old':
            chromedriver_win64_path=r'C:\old_chrome'
            if not os.path.exists(chromedriver_win64_path):
                download_chromedriver_testing_old()
            else:
                print("Old Testing Chrome Setup already present")   
        elif driver_type=='cdrive':
            c_driver_chromedriver()
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait
            service = Service(executable_path='C:/latest_chrome_driver/chromedriver.exe')
            options = webdriver.ChromeOptions()
            # options.add_argument('--proxy-server={}'.format(curr_proxy))
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver,10)
            return driver
        
        elif driver_type=='profile':
            driver=driver_initialisation_profile(username=username,profile_directory=profile_directory)
            return driver
        
        elif driver_type=='mobile':
            driver=mobile_emulation_driver()
            return driver


                    
