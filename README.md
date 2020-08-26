# scrapy-python-first-webcrawling-project

# Notion Reference
[Notion Link](https://www.notion.so/Scrapy-Fundamentals-7a9dff8da3cd4401b9b18c3d998893e4)

# Part - 1

- Start with Anaconda Virtual Environment
- Available Commands

    ```bash
    scrapy               #version 확인 및 기본적인 명령어들을 볼 수 있다.
    scrapy bench         #Run quick benchmark test
    scrapy fetch         #Fetch a URL using the Scrapy downloader
    scrapy genspider     #Generate new spider using pre-defined templates
    scrapy runspider     #Run a self-contained spider (without creating a project)
    scrapy settings      #Get settings values
    scrapy shell         #Interactive scraping console
    scrapy startproject  #Create new project
    scrapy version       #Print Scrapy version
    scrapy view          #Open URL in browser, as seen by Scrapy
    ```

# Part - 2, Project Creation and Start a project

- Start Project

```bash
scrapy startproject ${projectName}
```

### Project Structure

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9fe46837-f761-42a9-8c77-8628c36cd109/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9fe46837-f761-42a9-8c77-8628c36cd109/Untitled.png)

- Check if the project is successfully created

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c3b92615-8a1b-451e-bf08-5c623ea1b989/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c3b92615-8a1b-451e-bf08-5c623ea1b989/Untitled.png)

- `cfg` is very important. `scrapy.cfg`

⇒ execute the spiders

⇒ deploy your spiders

```bash
# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = worldometers.settings

[deploy]
#url = http://localhost:6800/
project = worldometers
```

- `/spiders` where all the spiders live
- `[items.py](http://items.py)` , we use it to clean the data we scrape and to sort out the data
- `[middlewares.py](http://middlewares.py)` , everything that has to do with requests and responses
    - `downloader middleware`
    - `spider middleware`
- `[pipelines.py](http://pipelines.py)`, store data
- `[settings.py](http://settings.py)` , extra configuration for your project

### First Scraping Exercise

worldometers.info/world-population/population-by-country 

```bash
scrapy genspider ${uniqueName} ${url Without Http And LastSlash}
```

```bash
scrapy genspider countries worldometers.info/world-population/population-by-country 
```

⇒ You don't need to add `http://` and `/` in the end of the url.

- You can check in the spider's folder, there's `[countries.py](http://countries.py)` file generated

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3b3aa8ec-e995-482d-a0b9-68ebfe638be2/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3b3aa8ec-e995-482d-a0b9-68ebfe638be2/Untitled.png)

- countries.py

⇒ Before being refactored

```python
# -*- coding: utf-8 -*-
import scrapy

class CountriesSpider(scrapy.Spider):
		#Each Spider must have a unique name
    name = 'countries'
    allowed_domains = ['worldometers.info/world-population/population-by-country']
    start_urls = ['http://worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        pass
```

⇒ After being refactored

```python
# -*- coding: utf-8 -*-
import scrapy

class CountriesSpider(scrapy.Spider):
		#Each Spider must have a unique name
    name = 'countries'
    allowed_domains = ['worldometers.info/'] #enlarge the scope of scraping by removing last parameters `world-population/population-by-country`
    start_urls = ['https://worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        pass
```

# Part - 3, use `scrapy shell` and run some code.

- Package Install `IPython`

```bash
conda install ipython
```

- go into `scrapy shell`

```bash
scrapy shell
```

### In the shell

1. fetch

    ```bash
    fetch("https://worldometers.info/world-population/population-by-country/")
    ```

2. create request

    ```bash
    # Create Request
    r = scrapy.Request(url='https://worldometers.info/world-population/population-by-country/')

    # Call `fetch()` 
    fetch(r)
    ```

3. get the body

    ```bash
    response.body
    ```

    ⇒ HTML markup of the website we are going to scrape will be printed.

4. view(response)

    ```bash
    view(response)
    ```

    ⇒ Prompt webbrowser

    ⇒ Actually, Scrapy see the website without javascript code.

# Part - 4,  xPath & CSS Selectors

ℹ️ Disable Javascript on Chrome

- Command Prompt, `command + shift + p`
- type `javascript` and disable it.

ℹ️ on Chrome, get `xPath`

- on Chrome Development Tool, press `command + f`
- //${htmlElement}

`[//h1](//h1)` , one element matches

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/033c77aa-7cfa-4812-ac9a-d403fc33d90e/Screen_Shot_2020-08-26_at_14.53.38.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/033c77aa-7cfa-4812-ac9a-d403fc33d90e/Screen_Shot_2020-08-26_at_14.53.38.png)

⇒ It will return all `h1` elements on the webpage.

`[//a](//a)` , 290 elements match

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7261a689-d3db-4b8a-9d4b-ffebfe24e13f/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7261a689-d3db-4b8a-9d4b-ffebfe24e13f/Untitled.png)

`[//td/a](//td/a)` , 235 elements match 

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e1ebb84c-4ba8-4d89-811b-43b828a0f19e/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e1ebb84c-4ba8-4d89-811b-43b828a0f19e/Untitled.png)

### xPath

- on Scrapy Console

```bash
title = response.xpath("//h1")
title
# this will return `h1` of the webpage.
```

- special xPath function `text()`

```bash
title = response.xpath("//h1/text()")
title.get()
# this will only return `text`
```

- countries, `text()` , `getall()`

```bash
countries = response.xpath("//td/a/text()").getall()
```

### CSS Selector

- on Scrapy Console

```bash
title_css = response.css("h1::text").getall()
```

❗️In Scrapy Project `xPath` is recommended, because `CSS Selector` takes more steps, which can result in slower performance.

- countries, `getall()`

```bash
countries_css = response.css("td a::text").getall()
```

# Part - 5, Create your own spider

### xCode Configuration

- python

### Write code

```python
# -*- coding: utf-8 -*-
import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info/']
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        yield {
            'title': title,
            'countries': countries
        }
```

### Execute your own spider

- example of command

```bash
scrapy crawl ${spiderName} 
```

- actual execution

```bash
#on the project folder where cfg file exists.
scrapy crawl countries 
```

- result of execution

```json
{
   "title":"None",
   "countries":[
      "China",
      "India",
      "United States",
      "Indonesia",
      "Pakistan",
      "Brazil",
      "Nigeria",
      "Bangladesh",
      "Russia",
      "Mexico",
      "Japan",
      "Ethiopia",
      "Philippines",
      "Egypt",
      "Vietnam",
      "DR Congo",
      "Turkey",
      "Iran",
      "Germany",
      "Thailand",
      "United Kingdom",
      "France",
      "Italy",
      "Tanzania",
      "South Africa",
      "Myanmar",
      "Kenya",
      "South Korea",
      "Colombia",
      "Spain",
      "Uganda",
      "Argentina",
      "Algeria",
      "Sudan",
      "Ukraine",
      "Iraq",
      "Afghanistan",
      "Poland",
      "Canada",
      "Morocco",
      "Saudi Arabia",
      "Uzbekistan",
      "Peru",
      "Angola",
      "Malaysia",
      "Mozambique",
      "Ghana",
      "Yemen",
      "Nepal",
      "Venezuela",
      "Madagascar",
      "Cameroon",
      "Côte d'Ivoire",
      "North Korea",
      "Australia",
      "Niger",
      "Taiwan",
      "Sri Lanka",
      "Burkina Faso",
      "Mali",
      "Romania",
      "Malawi",
      "Chile",
      "Kazakhstan",
      "Zambia",
      "Guatemala",
      "Ecuador",
      "Syria",
      "Netherlands",
      "Senegal",
      "Cambodia",
      "Chad",
      "Somalia",
      "Zimbabwe",
      "Guinea",
      "Rwanda",
      "Benin",
      "Burundi",
      "Tunisia",
      "Bolivia",
      "Belgium",
      "Haiti",
      "Cuba",
      "South Sudan",
      "Dominican Republic",
      "Czech Republic (Czechia)",
      "Greece",
      "Jordan",
      "Portugal",
      "Azerbaijan",
      "Sweden",
      "Honduras",
      "United Arab Emirates",
      "Hungary",
      "Tajikistan",
      "Belarus",
      "Austria",
      "Papua New Guinea",
      "Serbia",
      "Israel",
      "Switzerland",
      "Togo",
      "Sierra Leone",
      "Hong Kong",
      "Laos",
      "Paraguay",
      "Bulgaria",
      "Libya",
      "Lebanon",
      "Nicaragua",
      "Kyrgyzstan",
      "El Salvador",
      "Turkmenistan",
      "Singapore",
      "Denmark",
      "Finland",
      "Congo",
      "Slovakia",
      "Norway",
      "Oman",
      "State of Palestine",
      "Costa Rica",
      "Liberia",
      "Ireland",
      "Central African Republic",
      "New Zealand",
      "Mauritania",
      "Panama",
      "Kuwait",
      "Croatia",
      "Moldova",
      "Georgia",
      "Eritrea",
      "Uruguay",
      "Bosnia and Herzegovina",
      "Mongolia",
      "Armenia",
      "Jamaica",
      "Qatar",
      "Albania",
      "Puerto Rico",
      "Lithuania",
      "Namibia",
      "Gambia",
      "Botswana",
      "Gabon",
      "Lesotho",
      "North Macedonia",
      "Slovenia",
      "Guinea-Bissau",
      "Latvia",
      "Bahrain",
      "Equatorial Guinea",
      "Trinidad and Tobago",
      "Estonia",
      "Timor-Leste",
      "Mauritius",
      "Cyprus",
      "Eswatini",
      "Djibouti",
      "Fiji",
      "Réunion",
      "Comoros",
      "Guyana",
      "Bhutan",
      "Solomon Islands",
      "Macao",
      "Montenegro",
      "Luxembourg",
      "Western Sahara",
      "Suriname",
      "Cabo Verde",
      "Maldives",
      "Malta",
      "Brunei ",
      "Guadeloupe",
      "Belize",
      "Bahamas",
      "Martinique",
      "Iceland",
      "Vanuatu",
      "French Guiana",
      "Barbados",
      "New Caledonia",
      "French Polynesia",
      "Mayotte",
      "Sao Tome & Principe",
      "Samoa",
      "Saint Lucia",
      "Channel Islands",
      "Guam",
      "Curaçao",
      "Kiribati",
      "Micronesia",
      "Grenada",
      "St. Vincent & Grenadines",
      "Aruba",
      "Tonga",
      "U.S. Virgin Islands",
      "Seychelles",
      "Antigua and Barbuda",
      "Isle of Man",
      "Andorra",
      "Dominica",
      "Cayman Islands",
      "Bermuda",
      "Marshall Islands",
      "Northern Mariana Islands",
      "Greenland",
      "American Samoa",
      "Saint Kitts & Nevis",
      "Faeroe Islands",
      "Sint Maarten",
      "Monaco",
      "Turks and Caicos",
      "Saint Martin",
      "Liechtenstein",
      "San Marino",
      "Gibraltar",
      "British Virgin Islands",
      "Caribbean Netherlands",
      "Palau",
      "Cook Islands",
      "Anguilla",
      "Tuvalu",
      "Wallis & Futuna",
      "Nauru",
      "Saint Barthelemy",
      "Saint Helena",
      "Saint Pierre & Miquelon",
      "Montserrat",
      "Falkland Islands",
      "Niue",
      "Tokelau",
      "Holy See"
   ]
}
```

⇒ Python dictionary will be printed out.