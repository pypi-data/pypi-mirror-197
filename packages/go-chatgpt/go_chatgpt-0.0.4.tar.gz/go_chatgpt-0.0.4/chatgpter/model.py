import os
import time
import logging
import openai
import tiktoken


ymd_stamp = time.strftime('%Y%m%d', time.localtime())


# 加载GPT模型
class CallChatGPT:
    def __init__(self,
                 api_key = "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",
                 model="gpt-3.5-turbo",
                 temperature=1,
                 top_p=1,
                 n=1,
                 stream=False,
                 presence_penalty=0,
                 frequency_penalty=0,
                 logsdir="./logging",
                 logsname=f"chatgpt_{ymd_stamp}.log",
                 trend="general",):
        # 模型参数
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.n = n 
        self.stream = stream
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        # 日志参数
        self.logsdir = logsdir
        self.logsname = logsname
        self.logspath = os.path.join(logsdir, logsname)
        self.logs = self.built_logger()
        # 消息参数
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.trend = trend
        self.messages = []
        self.token_nums = []
        self.token_usage = []
        self.token_gaps = 2**4
        self.token_current = 0
        self.system_messages()
    
    def openai_gptapi(self): 
        openai.api_key = self.api_key    
        response = openai.ChatCompletion.create(model=self.model,
                                                messages=self.messages,
                                                temperature=self.temperature,
                                                top_p=self.top_p,
                                                n=self.n,
                                                stream=self.stream,
                                                presence_penalty=self.presence_penalty,
                                                frequency_penalty=self.frequency_penalty)
        
        return response    
    
    def built_logger(self):
        os.makedirs(self.logsdir, exist_ok=True)
        logs = logging.getLogger(__name__)
        logs.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=self.logspath, encoding="UTF-8")
        formatter = logging.Formatter(fmt="[%(asctime)s - %(levelname)s]: %(message)s",
                                      datefmt="%Y%m%d %H:%M:%S")
        handler.setFormatter(formatter)
        if not logs.handlers:
            logs.addHandler(handler)    
        
        return logs
    
    def reset_logger(self):
        if self.logs.handlers:
            self.logs.handlers = []
        if os.path.exists(self.logspath):
            os.remove(self.logspath)
            
    def check_logger(self):
        if not os.path.exists(self.logspath) or not self.logs.handlers:
            self.reset_logger()
            self.logs = self.built_logger() 
    
    def system_messages(self):
        setflag = False
        if not self.messages:
            setflag = True
        else:
            for message in self.messages:
                if message["role"] != "system":
                    setflag = True
                else:
                    setflag = False
                    break
        if setflag:
            if self.trend == "general":
                prompt = "You are a helpful assistant."
                self.messages.insert(0, {"role": "system", "content": prompt})
                self.token_current += (len(self.tokenizer.encode(prompt)) + self.token_gaps)
                self.token_usage = {"completion_tokens": 0,
                                    "prompt_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps), 
                                    "total_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps)}
                self.token_nums.insert(0, self.token_usage.copy())
            elif self.trend == "poet":
                prompt = "You are ChatGPT, a large language model trained by OpenAI. You can generate poems based on the user's input. You can write poems in different styles and formats, such as haiku, sonnet, free verse, etc. You are creative, expressive, and poetic."
                self.messages.insert(0, {"role": "system", "content": prompt})
                self.token_current += (len(self.tokenizer.encode(prompt)) + self.token_gaps)
                self.token_usage = {"completion_tokens": 0,
                                    "prompt_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps), 
                                    "total_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps)}
                self.token_nums.insert(0, self.token_usage.copy())
            elif self.trend == "tutor":
                prompt = "You are ChatGPT, a large language model trained by OpenAI. You can follow instructions given by the user. You can perform various tasks such as arithmetic calculations, text manipulation, web search, etc. You are smart, efficient, and reliable."
                self.messages.insert(0, {"role": "system", "content": prompt})
                self.token_current += (len(self.tokenizer.encode(prompt)) + self.token_gaps)
                self.token_usage = {"completion_tokens": 0,
                                    "prompt_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps), 
                                    "total_tokens": (len(self.tokenizer.encode(prompt)) + self.token_gaps)}
                self.token_nums.insert(0, self.token_usage.copy())
    
    def control_messages(self,
                         role=None,
                         content=None,
                         usage=None,
                         mode=None): 
        if mode == "message":
            if role == "user":
                self.messages.append({"role": "user", "content": content})
                self.token_current += (len(self.tokenizer.encode(content)) + self.token_gaps)
            elif role == "assistant":
                self.messages.append({"role": "assistant", "content": content})
                self.token_current += (len(self.tokenizer.encode(content)) + self.token_gaps)
        elif mode == "decrease":
            for _ in range(1+self.n):
                self.messages.pop(1)
            self.token_current -= (self.token_nums.pop(1)["total_tokens"] - self.token_gaps)
        elif mode == "increase":
            self.token_nums.append({"completion_tokens": usage["completion_tokens"],
                                    "prompt_tokens": usage["prompt_tokens"] - self.token_usage["total_tokens"], 
                                    "total_tokens": usage["total_tokens"] - self.token_usage["total_tokens"]})
            self.token_usage["completion_tokens"] = usage["completion_tokens"]
            self.token_usage["prompt_tokens"] = usage["prompt_tokens"]
            self.token_usage["total_tokens"] = usage["total_tokens"]
            self.token_current = usage["total_tokens"]
        
    def reset_messages(self):
        self.messages = []
        self.token_nums = []
        self.token_usage = []
        self.token_gaps = 2**4
        self.token_current = 0
        self.system_messages()
    
    
    def __call__(self, prompt):
        self.control_messages(role="user", content=prompt, mode="message")
        while self.token_current >= 4096:
            if len(self.messages) >= (1+1+self.n):
                self.control_messages(mode="decrease")
            else:
                answer_list = ["输入过长，请精简输入！"]
                self.reset_messages()
                
                return answer_list
        
        self.check_logger()
        self.logs.info(f"提问: {prompt}\n")        
          
        answer_list = []
        try:
            response = self.openai_gptapi()  
            answer_dict = {index: response.choices[index].message.content for index in range(self.n)}
            for index, answer in answer_dict.items():
                self.control_messages(role="assistant", content=answer, mode="message")            
                if self.n > 1:
                    self.check_logger()
                    self.logs.info(f"回答({index+1}): {answer.strip()}\n\n")
                else:
                    self.check_logger()
                    self.logs.info(f"回答: {answer.strip()}\n\n")    
                answer_list.append(answer.strip())            
            self.control_messages(usage=response.usage, mode="increase")             
        except openai.error.RateLimitError:
            answer_list = ["延迟较大，请稍后重试！"]
            self.reset_messages()
            
            return answer_list
        except openai.error.InvalidRequestError: 
            answer_list = ["请求无效，将重新启动！"]
            self.reset_messages()

            return answer_list
        
        return answer_list
    