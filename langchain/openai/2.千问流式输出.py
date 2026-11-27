import os
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
  base_url="https://cn-beijing.maas.qianwenaiapi.com/compatible-mode/v1"
)
# 第一次调用
user_message = {"role": "user", "content": "你好,我是陈尧，在学ai"}
completion = client.chat.completions.create(
  model="qwen3.8-max",
  messages=
  [
    {"role": "user", "content": "你好,我是陈尧，在学ai"}
  ],
  stream=True

)
for chunk in completion:
    #print(chunk.model_dump_json())
  if chunk.choices:
    if chunk.choices[0].delta.content:
      print(chunk.choices[0].delta.content, end="", flush=True)
  if chunk.usage:
      print(chunk.usage)



