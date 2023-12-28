import requests

link = 'https://raw.githubusercontent.com/devvspaces/readme_template/master/README.md'

def gen():
    with open('README.md', 'w', encoding="utf-8") as readme:
        file = requests.get(url=link).text
        readme.write(file)


if __name__ == "__main__":
    print('Calling the gen func')
    gen()