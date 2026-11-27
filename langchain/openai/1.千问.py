import os
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
  base_url="https://cn-beijing.maas.qianwenaiapi.com/compatible-mode/v1"
)
chat_history = []
# 第一次调用
user_message = {"role": "user", "content": "你好,我是陈尧，在学ai"}
chat_history.append(user_message)

completion = client.chat.completions.create(
  model="qwen3.8-max",
  messages=chat_history,

)
print(completion.choices[0].message.content)
chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})

#第二次调用
user_message2 = {"role": "user", "content": "我是谁"}
chat_history.append(user_message2)
completion = client.chat.completions.create(
  model="qwen3.8-max",
  messages=chat_history,
)
print(completion.choices[0].message.content)

chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})
