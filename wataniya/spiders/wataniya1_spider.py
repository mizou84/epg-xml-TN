from datetime import date, datetime
from zoneinfo import ZoneInfo

import scrapy


class epgSpider(scrapy.Spider):
    name = "wataniya1"

    start_urls = [
        "https://www.tunisiatv.tn/ar/programme/3/69c58aac8d6cac7a55cd2e09/%D8%A7%D9%84%D9%88%D8%B7%D9%86%D9%8A%D8%A9%201"
    ]

    def parse(self, response):

        program = response.css("div.desc")

        scheduleAll = program.css("time::text").getall()
        titleAll = program.css("h3 a::text").getall()
        contentAll = program.css("p::text").getall()

        scheduleAllParsed = [schedule.split(" - ") for schedule in scheduleAll]
        today = date.today().strftime("%Y%m%d")
        tunis_tz = ZoneInfo("Africa/Tunis")

        beginAll = [row[0:1] for row in scheduleAllParsed]
        beginAllFormatted = list(map(lambda x: str(x)[2:-2] + ":00", beginAll))
        beginAllFormattedDated = [today + " " + str(i) for i in beginAllFormatted]
        beginn_object = [
            datetime.strptime(j, "%Y%m%d %H:%M:%S") for j in beginAllFormattedDated
        ]
        beginn_utc_object = [v.replace(tzinfo=tunis_tz) for v in beginn_object]
        begin_xml = [w.strftime("%Y%m%d%H%M%S %z") for w in beginn_utc_object]

        endAll = [row[1:2] for row in scheduleAllParsed]
        endAllFormatted = list(map(lambda x: str(x)[2:-2] + ":00", endAll))
        endAllFormattedDated = [today + " " + str(i) for i in endAllFormatted]
        end_object = [
            datetime.strptime(j, "%Y%m%d %H:%M:%S") for j in endAllFormattedDated
        ]
        end_utc_object = [v.replace(tzinfo=tunis_tz) for v in end_object]
        end_xml = [w.strftime("%Y%m%d%H%M%S %z") for w in end_utc_object]

        # write down in xml

        # one programm

        header = [
            '<?xml version="1.0" encoding="UTF-8"?>\n',
            '<tv source-info-name="tunisiatv.tn" source-info-url="https://www.tunisiatv.tn/ar/programme">\n',
            '  <channel id="wataniya1">\n',
            "    <display-name>Wataniya 1</display-name>\n",
            '    <icon src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Logo_T%C3%A9l%C3%A9vision_tunisienne_1%2C_2017.svg/960px-Logo_T%C3%A9l%C3%A9vision_tunisienne_1%2C_2017.svg.png"/>\n',
            "  </channel>\n",
        ]
        with open("wataniya1.xml", "w", encoding="utf-8") as file:
            file.writelines(header)

        progTotal = len(titleAll)

        for ind in range(0, progTotal):
            body = [
                '  <programme start="'
                + str(begin_xml[ind])
                + '" stop="'
                + str(end_xml[ind])
                + '" channel="wataniya1">\n',
                '    <title lang="ar">' + str(titleAll[ind]) + "</title>\n",
                '    <desc lang="ar">' + str(contentAll[ind]) + "</desc>\n",
                "  </programme>\n",
            ]
            with open("wataniya1.xml", "a", encoding="utf-8") as file:
                file.writelines(body)

        fin = "</tv>\n"

        with open("wataniya1.xml", "a", encoding="utf-8") as file:
            file.write(fin)

        # for program in programs:
        #     yield {
        #         "schedule": program.css("time::text").get(),
        #         "title": program.css("h3 a::text").get(),
        #         "content": program.css("p::text").get(),
        #     }
