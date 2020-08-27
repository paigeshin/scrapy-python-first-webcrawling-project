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

- https://worldometers.info/world-population/population-by-country/
- a tag => 'https://www.worldometers.info/world-population/mozambique-population/'
- get `name` of the country and `year`, `population`

ℹ️ vsCode Terminal, switch to `Virtual Workspace`

```bash
conda activate Virtual_Workspace
```

```bash
conda activate ${Virtual_Workspace}
```

# Part 1, loop

```python
# -*- coding: utf-8 -*-
import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info/']
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    def parse(self, response):

        countries = response.xpath("//td/a")
        # '<a href="/world-population/saint-barthelemy-population/">Saint Barthelemy</a>',
        #'<a href="/world-population/saint-helena-population/">Saint Helena</a>',
        #'<a href="/world-population/saint-pierre-and-miquelon-population/">Saint Pierre &amp; Miquelon</a>',
        #'<a href="/world-population/montserrat-population/">Montserrat</a>',
        #'<a href="/world-population/falkland-islands-malvinas-population/">Falkland Islands</a>',
        #'<a href="/world-population/niue-population/">Niue</a>',
        #'<a href="/world-population/tokelau-population/">Tokelau</a>',
        # '<a href="/world-population/holy-see-population/">Holy See</a>'
        for country in countries:
            # Montserrat, Tokelau ... Holy See
            name = country.xpath('.//text()').get()
            # href link를 잡아준다.
            link = country.xpath('.//@href').get()

            yield {
                'country_name': name,
                'country_link': link
            }
```

1. 먼저 모든 tag를 잡는다.
2. loop를 돌리면서 detail한 element로 들어간다. 
3. 각각의 값을 yield.

# Part 2, make requests

```python
# -*- coding: utf-8 -*-
import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']  # 필요없는 extra slash를 지워줘야 한다.
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    def parse(self, response):

        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # URL이 Relative Path일 때를 대비하여, absolute URL을 만들어준다.

            # 1. One way to make Absolute URL, however this is not the best way
            # absolute_url = f'https://www.worldometers.info{link}'

            # 2. Second way to make Absolute URL, using `join`
            # absolute_url = response.urljoin(link)

            # 3. Third way to make Absolute URL, using `response object`
            yield response.follow(url=link)

            # request `link` fetched with xpath

            # yield scrapy.Request(url=absolute_url)

            ### Error ###
            # ValueError: Missing scheme in request url: /world-population/china-population/
            # Scheme in URL is `Http` or `Https`
            # 이런 에러가 발생하는 이유는, relative URL이기 때문에 scrapy에서 Request를 보내지 못하는 경우다.
            # 에러를 해결하려면 Absolute URL을 만들어준다.
            # Solution: make `absoluteURL`
```

### How to make `Absolute URL` , when it's relative URL

1. hardcoding

    ```python
    absolute_url = f'https://www.worldometers.info{link}'
    ```

2. `join`

    ```python
    absolute_url = response.urljoin(link)
    ```

3. `response` object

    ```python
    yield response.follow(url=link)
    ```

### Possible Errors that can occur while crawling

1. Relative URL `scheme is missing`
2. extra `/` in `allowed_domains`

    ```python
    allowed_domains = ['worldometers.info']  # 필요없는 extra slash를 지워줘야 한다.
    ```

# Part 3, fetch the response from request we sent

- 받은 URL을 통해서 또 다시 url에 들어가서 새로운 데이터 가져오기.

```python
# -*- coding: utf-8 -*-
import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']  # 필요없는 extra slash를 지워줘야 한다.
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    # 첫 번째 웹사이트에서 crawling
    def parse(self, response):

        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # absolute_url = f*https://www.worldometers.info{link}
            # absolute_url = response.urljoin(link)

            yield response.follow(url=link, callback=self.parse_country)

    # 각각의 a tag의 값을 긁어와서 crawling
    # Example URL https://www.worldometers.info/world-population/mozambique-population/
    def parse_country(self, response):
        # table이 2개 이상일 때 잡는 방법.   (//table)[index]
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()  # table row는 1부터 시작함.
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'year': year,
                'population': population
            }
```

# Part 4, give meta data to second function

```python
# -*- coding: utf-8 -*-
import scrapy
import logging

#  Practice
# 'https://worldometers.info/world-population/population-by-country/'
# a tag => 'https://www.worldometers.info/world-population/mozambique-population/'
# get `name` of the country and `year`, `population`

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']  # 필요없는 extra slash를 지워줘야 한다.
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    # 첫 번째 웹사이트에서 crawling
    def parse(self, response):

        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # absolute_url = f*https://www.worldometers.info{link}
            # absolute_url = response.urljoin(link)

            # give meta information
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    # 각각의 a tag의 값을 긁어와서 crawling
    # Example URL https://www.worldometers.info/world-population/mozambique-population/
    def parse_country(self, response):
        # retreive meta information
        name = response.request.meta['country_name']
        # table이 2개 이상일 때 잡는 방법.   (//table)[index]
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()  # table row는 1부터 시작함.
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'name': name,
                'year': year,
                'population': population
            }
```

- meta={'country_name' : name}
- response.request.meta['country_name']

# Practice 1

- https://worldometers.info/world-population/population-by-country/
- a tag => 'https://www.worldometers.info/world-population/mozambique-population/'
- get `name` of the country and `year`, `population`

# Practice 2

### **Debt to GDP ratio by country**

So your job is to scrape the **national debt to GDP** for each country listed in this website '[http://worldpopulationreview.com/countries/countries-by-national-debt/](http://worldpopulationreview.com/countries/countries-by-national-debt/)'.

![https://udemy-images.s3.amazonaws.com/redactor/raw/2019-09-18_08-48-58-40f744fdffa5df11d8765597398a24b6.PNG](https://udemy-images.s3.amazonaws.com/redactor/raw/2019-09-18_08-48-58-40f744fdffa5df11d8765597398a24b6.PNG)

The population is not required to be scraped, however if you want to scrape it that's fine.

Now since this will be your first exercise, I'm gonna list below the steps you need to follow:

1. First thing first please scaffold a new project called '**national_debt**' and then generate a spider within that same project called "**gdp_debt**"
2. The website does use the "http" protocol by default so there is no need to modify that in the '**start_urls'** since by default Scrapy will use "**http**"
3. Next inside the **parse** method make sure to iterate(loop) through all rows and yield two keys '**country_name**' and '**gdp_debt**'
4. Finally make sure to execute the spider

**A sample of the output:**

![https://udemy-images.s3.amazonaws.com/redactor/raw/2019-09-18_08-59-05-95722bf60d7539375501f52446ec6053.PNG](https://udemy-images.s3.amazonaws.com/redactor/raw/2019-09-18_08-59-05-95722bf60d7539375501f52446ec6053.PNG)

If you get stuck feel free to reach me out in the Q&A section.

Solution source code can be downloaded from this link '[https://www.dropbox.com/sh/7etr8cmrc9av5mr/AAB0QmO4Cdcg2dpqBHlTXbDta?dl=0](https://www.dropbox.com/sh/7etr8cmrc9av5mr/AAB0QmO4Cdcg2dpqBHlTXbDta?dl=0)' **please don't check it out unless you've done the exercise and you want to see my solution.**

Good luck,

Ahmed.