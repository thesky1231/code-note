from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


file_path = r"E:\My_github\Learn-NLP\my_utils\中华人民共和国刑法.pdf"
# 预约快递员，绑定文件，这个时候并没有读
loader = PyPDFLoader(file_path)


print("正在读取PDF文件。。。")
# 快递员取快递
docs = loader.load()
print(f"成功读取！文件一共有{len(docs)}页。")


# 创建一个切书机器
# chunk_size指多少字符切一刀
# chunk_overlap是前一段和后一段有多少重叠，防止断章取义
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

print("正在切割文档。。。")
# 运用切书机器切割文本
splits = text_splitter.split_documents(docs)

print(f"切割完成！一共切成了{len(splits)}个小块。")


# 查看切割出来的内容
print("\n--- 第一块的内容 ---")
print(splits[0].page_content)
print("-"*12)
