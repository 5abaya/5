import requests
from bs4 import BeautifulSoup
import time

url = "https://www.redbubble.com/sitemap/popular_fitted-mask_00000.xml"
response = requests.get(url)

if response.status_code == 200:
    sitemap_xml = response.content
    sitemap_soup = BeautifulSoup(sitemap_xml, "xml")

    # استخراج جميع عناوين URL من خريطة الموقع
    product_urls = [loc.text for loc in sitemap_soup.find_all("loc")] 
    last_modified_dates = [lastmod.text for lastmod in sitemap_soup.find_all("lastmod")] 

    # تعيين حجم الجزء
    chunk_size = 5 

    # فتح الملف للكتابة
    with open("output.txt", "w") as f:
        # تكرار كل URL واستخراج المعلومات ذات الصلة
        for i in range(len(product_urls)): 
            product_url = product_urls[i] 
            last_modified_date = last_modified_dates[i] 

            try:
                product_response = requests.get(product_url) 
                product_soup = BeautifulSoup(product_response.text, "html.parser") 

                # استخراج اسم المتجر
                store_name = product_soup.find("a", class_="ProductConfiguration__artistLink--2CvXt").text.strip() 

                # استخراج عنوان المنتج
                product_title = product_soup.find("h1", class_="styles__box--2Ufmy styles__text--23E5U styles__display2--3HydH styles__display-block--3kWC4 styles__margin-none--3Ub2V styles__marginTop-xs--2KZR5").text.strip() 

                # استخراج جميع العلامات المنتج
                tag_list = product_soup.find("div", id="work-tags") 
                tag_links = tag_list.find_all("a") 
                tag_data = [tag_link.text.strip().title() for tag_link in tag_links] 

                # تنسيق البيانات
                output = "------------------------------------------\n"
                output += f"🔸️Store Name: {store_name}\n"
                output += f"🔸️Product Title: {product_title}\n"
                output += f"🔸️Tags: {', '.join(tag_data)}.\n"
                output += f"🔸️Last Modified Date: {last_modified_date}\n"
                output += f"🔸️URL: {product_url}\n"

                # طباعة وكتابة البيانات
                print(output)
                f.write(output)

            except:
                # إذا حدث خطأ في استخراج بيانات المنتج، استمر في العملية
                pass

            # تأخير قليلاً بين كل استخراج لتجنب الحظر من الموقع
            time.sleep(2)
