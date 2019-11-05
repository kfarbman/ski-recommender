import pandas as pd
import requests
from bs4 import BeautifulSoup

# TODO: Request information with REST API
# http://docs.clientservice.onthesnow.com/docs/rest.html
# https://developer.weatherunlocked.com/documentation/skiresort/resources#resorts-list

class ResortStats:

    def __init__(self):

        self.URL_terrain = 'http://www.onthesnow.com/colorado/ski-resorts.html'
        self.URL_mtn_stats = 'http://www.onthesnow.com/colorado/statistics.html'
        self.URL_RM_terrain = 'http://www.onthesnow.com/rocky-mountain/ski-resorts.html'
        self.URL_RM_stats = 'http://www.onthesnow.com/rocky-mountain/statistics.html'

    def get_table(self, URL):
        content = requests.get(URL).content

        soup = BeautifulSoup(content, "html.parser")

        rows = soup.select('tr')

        print(rows)

        table_lst = []
        for row in rows:
            cell_lst = [cell for cell in row if cell != '\n']
            cell_lst = [cell.text for cell in cell_lst]
            table_lst.append(cell_lst)

        print(table_lst)

        ranking = pd.DataFrame(table_lst)
        column_names = [x.strip('\n') for x in table_lst[0]]
        ranking.columns = column_names
        ranking = ranking.drop(0)
        if len(ranking['Resort Name'][1]) == 1:
            ranking = ranking.drop(1)
        ranking['Last Updated'] = ranking['Resort Name'].apply(
            lambda x: x.split('\n')[3])
        ranking['Resort Location'] = ranking['Resort Name'].apply(
            lambda x: x.split('\n')[2])
        ranking['Resort Name'] = ranking['Resort Name'].apply(
            lambda x: x.split('\n')[1])
        ranking['User Rating'] = ranking['User Rating'].apply(
            lambda x: x.split('\n')[1:3])
        return ranking


if __name__ == '__main__':

    rs = ResortStats()

    terrain = rs.get_table(rs.URL_RM_terrain)
    mtn_stats = rs.get_table(rs.URL_RM_stats)

    # terrain['Runs'] = terrain['Runs'].apply(lambda x: int(x.strip('\n').replace('/','')))
    # levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    # level_columns = dict()
    # for level in levels:
    #     terrain[level] = terrain[level].apply(lambda x: int(x[:-1]) if len(x) > 2 else 0)
    #     level_columns[level] = '% '+level
    # terrain = terrain.rename(columns = level_columns)

    # num_fields = ['Base','Summit','Vertical Drop','Longest Run','Snow Making']
    # field_columns = dict()
    # for field in num_fields:
    #     field_columns[field] = field+' ({})'.format(mtn_stats[field][1][-2:])
    #     mtn_stats[field] = mtn_stats[field].apply(lambda x: float(x[:-2]) if x != 'N/A' else 0)
    # mtn_stats = mtn_stats.rename(columns=field_columns)
