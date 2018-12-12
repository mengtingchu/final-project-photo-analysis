import bs4
import os
import urllib.request

def get_html_files_names():
    return [file for file in os.listdir('.') if file[-4:] == "html"]

class Fignoss_dl:
    def __init__(self, outdir, filename):
        self.outdir = outdir
        self.filename = filename
        self.img_nbr = None
        self.remaining_img = None
        self.alldiv = None
        return

#alldiv : get the list of all divisions containing image links
    def open_file(self):
        with open(self.filename, "r", encoding = "ISO-8859-1") as f:
            fread = f.read()
            soup = bs4.BeautifulSoup(fread)
            self.alldiv = soup.find_all("img", {"height": "1200"})
            self.img_nbr = len(self.alldiv)
        return

# download and save all divisions 
    def dl_from_div(self, div):
        link = "https:" + div['src']
        image_name = div['alt']
        if not os.path.isfile(self.outdir + "/" + image_name + ".jpg"):
            try:
                urllib.request.urlretrieve(link, self.outdir + "/" + image_name + ".jpg")
            except:
                print('dl_failed')
            self.check_remaining_img()
            print('image downloaded, remaining :    ' + str(self.remaining_img) + "   " + str(round(self.remaining_img/self.img_nbr*100,0)) + "  %")
        return

# check 
    def check_remaining_img(self):
        i = 0
        for div in self.alldiv:
            image_name = div['alt']
            if not os.path.isfile(self.outdir + "/" + image_name + ".jpg"):
                i+= 1

        a = len([1 for div in self.alldiv if not os.path.isfile(self.outdir + "/" + div['alt'] + ".jpg")])
        self.remaining_img = i
        return

    def dl_all_images(self):
        [self.dl_from_div(div) for div in self.alldiv]

    def main(self):
        print(self.filename)
        self.open_file()
        self.dl_all_images()
        print(self.filename + "    all images downloaded")


def main2():
    list_names = get_html_files_names()
    for filename in list_names:
        # output directory for images
        outdir = filename.split(".")[0]
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        downloader = Fignoss_dl(outdir, filename)
        downloader.main()

main2()
