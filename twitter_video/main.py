import io

import requests
from bs4 import BeautifulSoup

# Yep, guys, this is a bit of a quick-and-dirty fix.

donor_url = "https://tweeload.com/download/"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"


def get_video_links(text) -> list:
    """
    Parse the page to extract video links.

    :param text: The HTML of the page
    :return: A list of video links
    """
    bs = BeautifulSoup(text, "html.parser")
    download_links = bs.find_all("a", attrs={'href': True, 'class': 'btn download__item__info__actions__button'},
                                 string="Download")

    # Filter the links to only include the ones with a token
    return [link['href'] for link in download_links if 'token=' in link['href']]



def download_twitter_video(status_id) -> None:
    """
    Download a tweet video from tweeload.com.

    :param status_id: The ID of the tweet
    """
    headers = {'User-Agent': user_agent}
    result = requests.get(donor_url + status_id, headers=headers)

    # Check if the request was successful
    if result.status_code == 200:
        # Get the href attribute of the links
        hrefs = get_video_links(result.text)

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


def get_twitter_video(status_id: str) -> io.BytesIO | None:
    """
    Download a tweet video from tweeload.com.

    :param status_id: The ID of the tweet
    :return: A BytesIO object containing the video, or None if the video was not found
    """
    headers = {'User-Agent': user_agent}
    result = requests.get(donor_url + status_id, headers=headers)

    if result.status_code == 200:
        # Get the href attribute of the links
        hrefs = get_video_links(result.text)

        # If there are no download links, return None
        if hrefs is None or len(hrefs) == 0:
            return None

        # Download the video
        response = requests.get(hrefs[0], stream=True)
        buf = io.BytesIO()

        # Write the video to the buffer
        for chunk in response.iter_content(chunk_size=1024):
            buf.write(chunk)
        buf.seek(0)

        return buf

    return None


if __name__ == '__main__':
    tw_url = "https://x.com/itsfoss2/status/1838202526899798466"
    status = tw_url.split('/')[-1]
    buffer = get_twitter_video(status)

    with open(status + ".mp4", 'wb') as f:
        # Write the file-like object to the file
        f.write(buffer.read())
