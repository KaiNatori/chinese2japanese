import requests
import xml.etree.ElementTree as ET
import time

start_time = time.time()

print("chinese2japanese内に指定された形式のファイルを入れ、そのファイル名を入力してください。")


file_name = input(">>> ")

with open(file_name, "r") as f:
    data = f.read()

words_list = [word.strip() for word in data.split("，")]

print(f"{len(words_list)}個の単語が含まれています")


def get_data_from_api(word):
    url = f"http://www.ctrans.org/api.php?mode=search&word={word}"

    response = requests.get(url)

    root = ET.fromstring(response.content)

    result = root.find("Result")

    pinyin = result.find("pyn").text
    translation = result.find("jpn").text

    return (word, pinyin, translation)


def generate_markdown_table_row(word, pinyin, translation):
    return f"| {word} | {pinyin} | {translation} |\n"


with open(f"{file_name}.md", "w", encoding="utf-8") as f:
    f.write("| Word | Pinyin | Translation |\n")
    f.write("| ---- | ------ | ----------- |\n")

    for word in words_list:
        data = get_data_from_api(word)
        new_row = generate_markdown_table_row(*data)
        f.write(new_row)

end_time = time.time()
execution_time = end_time - start_time

print(f"{file_name}.mdを生成しました。")

print(f"実行時間: {execution_time}秒")
