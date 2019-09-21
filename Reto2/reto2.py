from pyquery import PyQuery as pq

url = "https://twitter.com/tyleroakley/status/1173977672701157376"

##	Abriendo pagina
f= open("tweet_page.html","r+")
page = f.read()
f.close()

pagina = pq(page)
##	Obteniendo likes, retweets y respuestas
likes = pq(pagina("#profile-tweet-action-favorite-count-aria-" + url.split("/")[-1]))
retweets = pq(pagina("#profile-tweet-action-retweet-count-aria-" + url.split("/")[-1]))
replies_num = pq(pagina("#profile-tweet-action-reply-count-aria-" + url.split("/")[-1]))
replies = pq(pagina(".ThreadedConversation--loneTweet\
  \
  "))

##	Abriendo archivo para guardar data
f = open("reto2.txt", "w+")
f.write("Likes: {}\nRetweets: {}\nReplies: {}\n\n".format(likes.html(), retweets.html(), replies_num.html()))
f.write("\n\nReplies: \n")

##	Iterando las respuestas
for r in replies:
	r = pq(r)
	username = r(".username > b").html()
	text_obj = r(".tweet-text")
	##	Removiendo referencias a emojis e imagenes
	text_obj("img").remove()
	text_obj(".twitter-timeline-link").remove()
	if username and text_obj.html():
		##	Parseando tags
		a = text_obj("a")
		b = text_obj("a > b")
		texto = text_obj.html()
		if a and b:
			texto = texto.replace(a.outerHtml(), "@" + b.html())
		f.write("@{}: {}\n".format(username, texto))
f.close()


