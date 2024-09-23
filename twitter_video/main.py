import requests
from bs4 import BeautifulSoup

donor_url = "https://tweeload.com/download/"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"


def download_video(status_id):
    """
    Download a tweet video from tweeload.com.
    Yep, guys, this is a bit of a quick-and-dirty fix.

    :param status_id: The ID of the tweet
    """
    headers = {'User-Agent': user_agent}
    result = requests.get(donor_url + status_id, headers=headers)

    # Check if the request was successful
    if result.status_code == 200:
        # Parse the HTML content of the page
        bs = BeautifulSoup(result.text, "html.parser")

        # Find the download links
        download_links = bs.find_all("a", attrs={'href': True, 'class': 'btn download__item__info__actions__button'}, string="Download")

        # Get the href attribute of the links
        hrefs = [link['href'] for link in download_links if 'token=' in link['href']]

        # If there are no download links, print an error message
        if hrefs is None or len(hrefs) == 0:
            print("Video not found!")
        else:
            # Create a file name with the tweet ID
            file_name = status_id + ".mp4"

            # Download the video
            response = requests.get(hrefs[0], stream=True)

            # Save the video to the file
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
    else:
        # If there is an error, print the status code
        print(f"An error in downloading video! status code: {result.status_code}")


if __name__ == '__main__':
    tw_url = "https://x.com/itsfoss2/status/1838202526899798466"
    status = tw_url.split('/')[-1]
    download_video(status)
