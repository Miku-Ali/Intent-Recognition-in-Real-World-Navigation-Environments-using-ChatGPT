import os
import replicate 

os.environ["REPLICATE_API_TOKEN"] = "r8_Qt6S32ODYwwRG21z52uWBhemTSWZE6m12tmas"


output = replicate.run(
  "liuhaotian/llava-v1.5-13b",
  input={
    "debug": False,
    "top_k": 50,
    "top_p": 1,
    "prompt": "give me the path from Manchester Piccadilly station to Kilburn Building .",
    "temperature": 0.75,
    "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
    "max_new_tokens": 500,
    "min_new_tokens": -1
  }
)
# for i in output:
#     print(i)
print(output)