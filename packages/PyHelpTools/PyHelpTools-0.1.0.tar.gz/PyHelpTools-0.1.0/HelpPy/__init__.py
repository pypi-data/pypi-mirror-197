class HelpPyError():
  def ApiError():
    return """Please make sure you set your key using GPT.key = {key}"""
  def ServerOverFlow():
    return "Servers are having huge overload"
def InstallPackages(Librarys=[]):
  import os
  for lib in Librarys:
    os.system(f"python -m pip install {lib}")

class GPTAI():
  import openai
  
  def __init__(self):
    self.api = ""
    self.answer = ""

  def sendResponse(self, question):
    import openai
    openai.api_key = self.api
    model = "text-davinci-003"
    try:
      response = openai.Completion.create(model=model,
                                          prompt=question,
                                          temperature=0,
                                          max_tokens=1000,
                                          top_p=1.0,
                                          frequency_penalty=0.0,
                                          presence_penalty=0.0,
                                          stop=["\"\"\""])
    except openai.error.AuthenticationError:
      raise HelpPyError.ApiError()
    except openai.error.RateLimitError:
      raise HelpPyError.ServerOverFlow()
    self.answer = response['choices'][0]['text']
  def setApi(self,api):
    self.api = api

def CreateEnv(Name):
  import os
  os.system("python -m pip --upgrade virtualenv")
  os.system(F"python3 -m venv {Name}")