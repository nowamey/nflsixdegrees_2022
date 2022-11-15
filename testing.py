import retrieval

def test_team_list():
    print((retrieval.get_teams("Josh Allen")))

def testdict_idea():
    finallist = []
    test_dict = dict()
    
    test_dict["dawg"] = ["meow","cat","dog"]
    test_dict["chicken"] = ["home","love","her"]
    for key in test_dict.keys():
        for val in test_dict[key]:
            print(val)
def tuplekeys(year =2022,team = 'buf'):
    key = (team,year)
    team_dict = dict()
    team_dict[key] = "josh allen"
    return team_dict[team,year]
if __name__ == "__main__":
    #testdict_idea()
    test_team_list()