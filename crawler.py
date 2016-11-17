import urllib,json,re,csv,sys
from bs4 import BeautifulSoup
import Post

def parser(post):
    """
    :param post: str(post in html)
    :return postDic: dictionary
    """
    soup = BeautifulSoup(post,"html.parser")
    postDic = {}
    postDic["upVotes"] = soup.find("div")["data-apollo-up-votes"]
    postDic["downVotes"] = soup.find("div")["data-apollo-down-votes"]
    postDic["url"] = postBaseUrl+ soup.find("a",{"class":"title-link"})["href"]
    postDic["type"] = postType
    postDic["title"] = soup.find("span",{"class":"title-span"}).getText()
    postDic["username"] = soup.find("span",{"class":"username"}).getText()
    postDic["realm"] = soup.find("span",{"class":"realm"}).getText()
    postDic["posttime"] = soup.find("span",{"class":"timeago"})["title"]
    postDic["viewCount"] = soup.find("td",{"class":"view-counts byline"}).find("span",{"class":"number opaque"})["data-short-number"]
    postDic["commentCount"] = soup.find("td",{"class":"num-comments byline"}).find("span",{"class":"number opaque"})["data-short-number"]
    postPage = urllib.urlopen(postDic["url"])
    content = BeautifulSoup(postPage.read(),"html.parser")
    postDic["content"] = content.find("div",{"class":"body knockout-provided"}).getText()
    return postDic

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    global postBaseUrl,postType
    postAPI = "http://boards.na.leagueoflegends.com/api/PEr1qIcT/discussions?"   #API for crawling posts, 50 at a time.
    postBaseUrl = 'http://boards.na.leagueoflegends.com' #Base url for crawling the content of a single post
    postNum = 50
    postType = "recent"
    datapath = "posts.csv"
    fieldnames = ["upVotes","downVotes","url","type","title","username","realm","posttime","viewCount","commentCount","content"]
    with open(datapath, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,postNum,50):
            num_loaded = i
            #sample crawUrl: http://boards.na.leagueoflegends.com/api/PEr1qIcT/discussions?sort_type=recent&num_loaded=50
            crawUrl = postAPI+"sort_type="+postType+"&num_loaded="+str(num_loaded)
            response = urllib.urlopen(crawUrl)
            data = json.loads(response.read())
            discussions = data["discussions"]
            post_pattern = r"<tr[\s\S]*?\/tr>" #Separate 50 posts crawled at a time
            posts = re.findall(post_pattern,discussions)
            for post in posts:
                postDic = parser(post)
                writer.writerow(postDic)









