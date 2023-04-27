import requests
from bs4 import BeautifulSoup

url = "https://www.redbubble.com/sitemap/popular_fitted-mask_00000.xml"
response = requests.get(url)
sitemap_xml = response.content
sitemap_soup = BeautifulSoup(sitemap_xml, "xml")


# Extract all the URLs from the sitemap 
product_urls = [loc.text for loc in sitemap_soup.find_all("loc")] 
last_modified_dates = [lastmod.text for lastmod in sitemap_soup.find_all("lastmod")] 

# Set the chunk size 
chunk_size = 5 

# Open the file for writing
with open("output.txt", "w") as f:
    # Iterate through each URL and extract the relevant information 
    for i in range(len(product_urls)): 
        product_url = product_urls[i] 
        last_modified_date = last_modified_dates[i] 

        product_response = requests.get(product_url) 
        product_soup = BeautifulSoup(product_response.text, "html.parser") 

        # Extract the store name 
        store_name = product_soup.find("a", class_="ProductConfiguration__artistLink--2CvXt").text.strip() 

        # Extract the product title 
        product_title = product_soup.find("h1", class_="styles__box--2Ufmy styles__text--23E5U styles__display2--3HydH styles__display-block--3kWC4 styles__margin-none--3Ub2V styles__marginTop-xs--2KZR5").text.strip() 

        # Extract all the product tags 
        tag_list = product_soup.find("div", id="work-tags") 
        tag_links = tag_list.find_all("a") 
        tag_data = [] 
        for tag_link in tag_links: 
            tag = tag_link.text.strip() 
            tag_data.append(tag) 

        # Format the data
        output = "------------------------------------------\n"
        output += f"🔸️Store Name: {store_name}\n"
        output += f"🔸️Product Title: {product_title}\n"
        output += "🔸️Tags: "
        for i in range(len(tag_data)): 
            if i != len(tag_data) - 1: 
                output += tag_data[i].title() + ", " 
            else: 
                output += tag_data[i].title() + ".\n"
        output += f"🔸️Last Modified Date: {last_modified_dates[i]}\n"
        output += f"🔸️URL: {product_url}\n"
        
        # Print and write the data
        print(output)
        f.write(output)

        # Wait 1 second before making the next request
        time.sleep(1)
print("✅ Done extracting all data from the sitemap!")