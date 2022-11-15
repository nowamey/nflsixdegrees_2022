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
def testretrieval():
    #(retrieval.get_roster(2022,'rav'))
    retrieval.get_players(retrieval.get_roster("rav","2022"))

if __name__ == "__main__":
    #testdict_idea()
    print(testretrieval())