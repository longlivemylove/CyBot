# !aptgroup is to query a Google spreadsheet containing information on common APT groups

import os, requests, re, csv, io, sys
from errbot import BotPlugin, botcmd, arg_botcmd

class aptgroup(BotPlugin):

    @arg_botcmd('query', type=str) # flags a command
    def aptgroup(self, msg, query=None):

        # Create headers for HTTP request
        headers={}
        headers["User-Agent"]= "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"
        headers["DNT"]= "1"
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        headers["Accept-Encoding"] = "deflate"
        headers["Accept-Language"]= "en-US,en;q=0.5"

        # Construct the URL to fetch the spreadsheet
        file_id="1ljXt_ct2J7TuQ45KtvGppHwZUVF7lNxiaAKII6frhOs"
        url = "https://docs.google.com/spreadsheets/d/{0}/pub?gid=1747640944&output=csv".format(file_id)

        try:
            r = requests.get(url, headers=headers)
        except:
            return("Error:  Request failed")
            exit()

        #read html code
        sio = io.StringIO( r.text, newline=None)
        reader = csv.DictReader(sio, dialect=csv.excel)

        # Build answer to return it
        answer=""
        for row in reader:
            m = re.search(query, str(row), re.IGNORECASE)
            if m:
                answer = answer + "\r\n## Group: " + row["Group"] + " ##"
                answer = answer + "\r\nAliases: " + row["Aliases"]
                answer = answer + "\r\nDescription: " + row["Description"]

        if not answer:
            answer = "Did not find anything.  Please refine your search."

        return(answer)

