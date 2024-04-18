# # load the large language model file
# from llama_cpp import Llama
# LLM = Llama(model_path="model\mistral-7b-instruct-v0.1.Q5_K_M.gguf")

# # create a text prompt
# prompt = "Q: What are the names of the days of the week? A:"

# # generate a response (takes several seconds)
# output = LLM(prompt)

# # display the response
# print(output["choices"][0]["text"])

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ChatRoom(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('簡易聊天室')
        self.geometry('400x450')  # 設定初始窗口大小

        self.build_ui()

    def build_ui(self):
        # 文本顯示框
        self.text_area = ScrolledText(self)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)  # 禁止直接在文本框編輯

        # 消息輸入框
        self.message_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.message_var)
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)  # 綁定回車鍵發送消息

        # 發送按鈕
        send_button = tk.Button(self, text='發送', command=self.send_message)
        send_button.pack(padx=10, pady=5, fill=tk.X)

    def send_message(self, event=None):
        msg = self.message_var.get().strip()
        if msg:
            # 將消息添加到文本顯示框
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, msg + '\n')
            self.text_area.config(state=tk.DISABLED)
            self.text_area.yview(tk.END)  # 滾動到最新消息
        self.message_var.set('')  # 清空輸入框

if __name__ == "__main__":
    app = ChatRoom()
    app.mainloop()

