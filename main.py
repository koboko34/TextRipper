"""
Armand Yilinkou
13/02/2023

Purpose of this project is to create an application which parses text from multiple websites and produced a neatly
formatted text file containing the desired text. In this file I will attempt to compile the text from 266 chapters of
お隣の天使様 into a single text file, with sections for each chapter.

Source = https://ncode.syosetu.com/n8440fe/
Chapter 1 = https://ncode.syosetu.com/n8440fe/1/
Chapter 2 = https://ncode.syosetu.com/n8440fe/2/
etc...

Resources:
    https://stackoverflow.com/questions/61862165/python-extract-text-from-webpage
    https://stackoverflow.com/questions/33566843/how-to-extract-text-from-html-page
    https://stackoverflow.com/questions/69141055/python-requests-does-not-get-website-that-opens-on-browser
"""
import os

import requests
from bs4 import BeautifulSoup

from timeit import default_timer as timer
from datetime import timedelta


NUM_OF_CHAPTERS = 266


def delete_lines(file, lines_to_delete=[]):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines_to_delete:
        if line < len(lines):
            lines[line] = ""
    with open(file, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    start = timer()
    with open('parsedText.txt', 'w', encoding="utf-8") as f:
        f.write("[TITLE]" + "お隣の天使様にいつの間にか駄目人間にされていた件" + "\n")

        for chapter in range(1, NUM_OF_CHAPTERS + 1):
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
            }
            url = "https://ncode.syosetu.com/n8440fe/" + str(chapter) + "/"
            response = session.get(url, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            subtitle = soup.find(id='novel_contents')
            subtitle = "[SUBTITLE]" + subtitle.select(".novel_subtitle")[0].getText()
            story = soup.find(id='novel_honbun').getText()

            with open('temp.txt', 'w', encoding="utf-8") as temp:
                temp.write(story)

            with open('temp.txt', 'r', encoding="utf-8") as temp:
                lines = temp.readlines()

            last_deleted = False
            lines_to_delete = []
            for num, line in enumerate(lines):
                # if not last_deleted and is \n, add line number to list
                if line == "\n":
                    if last_deleted:
                        continue
                    lines_to_delete.append(num)
                    last_deleted = True
                    continue
                if last_deleted:
                    last_deleted = False
            # once reached end of file, delete lines from list in REVERSE order
            lines_to_delete.reverse()

            with open('temp.txt', 'a', encoding="utf-8") as temp:
                print(f"Deleting {len(lines_to_delete)} empty lines...")
                delete_lines('temp.txt', lines_to_delete)

            with open('temp.txt', 'r', encoding="utf-8") as temp:
                clean_story = temp.read()

            os.remove('temp.txt')

            f.write("\n" + subtitle + "\n\n")
            f.write(clean_story)

            print(f"Chapter {chapter} parsing complete.")

        end = timer()
        print("\nParsing completed in " + str(timedelta(seconds=end - start)) + " seconds.")


if __name__ == '__main__':
    main()

