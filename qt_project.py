import bs4
import os
import urllib.request



# https://galeries.delepinay.fr/-/galeries/evenementiel/grand-gala-des-arts-et-metiers/la-nuit-des-fignoss-2018/studiobooth/escalier/de-23h-a-minuit
# go to this URL and save the webpage as html. Save it in the same folder as this script

def open_file(filename):
    """
    This method parse the saved webpages and get all the divs with a picture link
    :return: a list of divisions containing the img link, and also return the number of images
    """
    # open the html file and return all the instances of the html element we are looking for
    with open(filename, "r", encoding='ansi') as f:
        soup = bs4.BeautifulSoup(f.read())

        # alldiv is a list of all the divisions containing the images links
        alldiv = soup.find_all("img", {"height": "1200"})
        img_nbr = len(alldiv)

    return alldiv,img_nbr

def dl_from_div( div):
    """

    :param div: one division from the list alldiv
    :return: nothing, but save the image contained in the div
    """
    # recreate an internet link by adding https/ in front of the src link
    link = "https:" + div['src']

    # get the image name
    image_name = div['alt']

    #this line check if the photo exist in the folder
    if not os.path.isfile(image_name + ".jpg"):
        try:
            # this line download the image in the folder
            urllib.request.urlretrieve(link, image_name + ".jpg")

        else:
            print('dl_failed')

        print('image downloaded    ' + str(image_name))


def dl_all_images(alldiv):
    """
    :param alldiv: a list of divisions containing the src links of the image
    :return: nothing, just save the image in the current folder
    """
    [dl_from_div(div) for div in alldiv]


def main():
    """
    This function open the html file,  and download all the images
    :return: nothing, download all the images
    """
    alldiv, img_nbr = open_file('blabla_test.html')
    print('downloading  '+str(img_nbr)+'  images')
    dl_all_images(alldiv)
    print('DONE all images downloaded')


# run the main function to download
main()