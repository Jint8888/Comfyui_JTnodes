import json
from openai import OpenAI as openai_client

def chat(client, model, messages, max_tokens):
    """
    使用OpenAI客户端发送聊天请求
    
    Args:
        client: OpenAI客户端实例
        model: 模型名称
        messages: 消息历史列表
        max_tokens: 最大生成token数
    
    Returns:
        str: 模型的响应内容
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

class SiliconflowFreeNode:
    def __init__(self):
        self.session_history = []  # 用于存储会话历史的列表
        self.system_content="You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."

    @classmethod
    def INPUT_TYPES(cls):
        model_list= [ 
            "Pro/deepseek-ai/DeepSeek-V3",
            "Qwen/QwQ-32B",
            "Qwen/Qwen2.5-32B-Instruct",
            "Pro/deepseek-ai/DeepSeek-R1"
            ]
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "your-api-key-here",
                    "dynamicPrompts": False,
                    "displayedLength": 100
                }),
                "prompt": ("STRING", {"multiline": True,"dynamicPrompts": False}),
                "system_content": ("STRING", 
                                   {
                                       "default": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.", 
                                       "multiline": True,"dynamicPrompts": False
                                       }),
                "model": ( model_list, 
                    {"default": model_list[0]}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "context_size":("INT", {"default": 1, "min": 0, "max":30, "step": 1}),
                "max_tokens":("INT", {"default": 2048, "min": 512, "max":200000, "step": 1}),
            },
               "optional":{
                    "custom_model_name":("STRING", {"forceInput": True,}), #适合自定义model
                },
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("text","messages","session_history",)
    FUNCTION = "generate_contextual_text"
    CATEGORY = "JT/text"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,False,False,)

    def generate_contextual_text(self,
                                api_key,
                                prompt, 
                                system_content,
                                model, 
                                seed,
                                context_size,
                                max_tokens,
                                custom_model_name=None):

        if custom_model_name!=None:
            model=custom_model_name

        api_url="https://api.siliconflow.cn/v1"
        
        if system_content:
            self.system_content=system_content
        
        client = openai_client(
            api_key=api_key,
            base_url=api_url
        )

        def crop_list_tail(lst, size):
            if size >= len(lst):
                return lst
            elif size==0:
                return []
            else:
                return lst[-size:]
            
        session_history=crop_list_tail(self.session_history,context_size)

        messages=[{"role": "system", "content": self.system_content}]+session_history+[{"role": "user", "content": prompt}]

        response_content = chat(client,model,messages,max_tokens)
        
        self.session_history=self.session_history+[{"role": "user", "content": prompt}]+[{'role':'assistant',"content":response_content}]

        return (response_content,json.dumps(messages, indent=4),json.dumps(self.session_history, indent=4),)
