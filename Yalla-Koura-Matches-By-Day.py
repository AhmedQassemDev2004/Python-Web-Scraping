'''
    Web scraping application that gets all matches and their details from Yallakoura.com website
    in specific date given by the user
'''

from bs4 import BeautifulSoup, ResultSet
import csv
import requests as req
import os

date = input("Please Enter targeted date as MM/DD/YYYY format: ")
# Replace forward slashes with underscores in the filename
date_for_filename = date.replace('/', '_')
page = req.get(f"https://www.yallakora.com/Match-Center/?date={date}#")
src = page.content

# results
matches_details=[]

def get_match_info(championship: ResultSet):
    info = {}

    info['title'] = championship.find('div', attrs={'class':'title'}).find('h2').text.strip()

    info['all_matches'] = []

    all_matches = championship.find("div", attrs={'class':'ul'}).find_all("div", attrs={'class':'liItem'})
    
    info['number_of_matches'] = len(all_matches)

    for m in all_matches:
        teamA = m.find("div", attrs={"class":"teamA"}).find('p').text.strip()
        teamB = m.find("div", attrs={"class":"teamB"}).find('p').text.strip()

        teamA_score = m.find("div", attrs={"class":"MResult"}).find_all("span")[0].text.strip()
        teamB_score = m.find("div", attrs={"class":"MResult"}).find_all("span")[2].text.strip()

        match_time = m.find("div", attrs={"class":"MResult"}).find_all("span")[3].text.strip()

        info['all_matches'].append({
            "team1": teamA,
            "team2": teamB,
            "team1_score": teamA_score,
            "team2_score": teamB_score,
            "match_time": match_time
        })

    matches_details.append(info)
    return info

# lxml is the parser
soup = BeautifulSoup(src, "lxml")

championships = soup.find_all("div", {'class':'matchCard'})

for c in championships:
    get_match_info(c)

# Create the results directory if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

with open(f'results/matches_details_{date_for_filename}.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Championship Title", "Team 1", "Team 2", "Score", "Match Time"])

    for championship in matches_details:
        title = championship['title']
        number_of_matches = championship['number_of_matches']
        for match in championship['all_matches']:
            writer.writerow([
                title,
                match['team1'],
                match['team2'],
                f"{match['team1_score']} - {match['team2_score']}",
                match['match_time']
            ])
