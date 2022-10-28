import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

from text_for_image import text

mask = np.array(Image.open("img/my_elefant.png"))

stopwords = set(STOPWORDS)
stopwords.add("И")
stopwords.add("на")
stopwords.add("умрет")
stopwords.add("больше")
stopwords.add("мы")
stopwords.add("что")

wordcloud = WordCloud(background_color="black", stopwords=stopwords, max_words=1500,
                      mask=mask, contour_width=0, contour_color='green').generate(text)

# create coloring from image
image_colors = ImageColorGenerator(mask)

wordcloud.recolor(color_func=image_colors).to_file("img/word_elephant_mask.png")

plt.figure()
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.show()
