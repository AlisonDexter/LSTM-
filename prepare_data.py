import os
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = ''
    
    for item in book.get_items():
        # 使用EpubHtml代替ITEM_DOCUMENT
        if isinstance(item, epub.EpubHtml):
            content = item.get_content().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            text += soup.get_text() + '\n'
    return text


def merge_epubs_to_txt(folder_path, output_file='merge_books.txt'):
    # 如果目标文件已经存在，则跳过合并操作
    if os.path.exists(output_file):
        print(f"{output_file} 已存在，跳过合并过程。")
        return

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.epub'):
                epub_path = os.path.join(folder_path, filename)
                print(f'正在处理 {filename}....')
                text = epub_to_text(epub_path)
                outfile.write(f'开始：{filename}\n')
                outfile.write(text)
                outfile.write(f'\n# 最后：{filename}\n\n')  # 修复这里的格式问题
                print(f'处理完成 {filename}....')
    print(f"合并完成，结果保存为 {output_file}")


def split_text(file, train_num=6000):
    split_file = "split_7.txt"
    
    # 如果分割后的文件已存在，则跳过分割
    if os.path.exists(split_file):
        print(f"{split_file} 已存在，跳过分割过程。")
        with open(split_file, "r", encoding="utf-8") as f:
            return f.read()[:train_num * 64]  # 直接读取并返回需要的部分

    # 文件不存在时进行分割
    all_data = open(file, "r", encoding="utf-8").read()
    with open(split_file, "w", encoding="utf-8") as f:
        split_data = " ".join(all_data)
        f.write(split_data)
    
    return split_data[:train_num * 64]





if __name__ == '__main__':
    merge_epubs_to_txt('fairy-tale-dataset')
    split_text('merge_books.txt')
