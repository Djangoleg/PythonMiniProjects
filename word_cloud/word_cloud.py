import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from text_for_image import text

stopwords = set(STOPWORDS)
stopwords.add("И")
stopwords.add("на")
stopwords.add("умрет")
stopwords.add("больше")
stopwords.add("мы")
stopwords.add("что")
stopwords.add("нам")

wordcloud = WordCloud(background_color="black", stopwords=stopwords, width=300, height=300, max_words=100,
                      contour_width=0, contour_color='green').generate(text)

wordcloud.to_file("img/word_cloud.png")

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
