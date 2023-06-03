import openai
import traceback

def openai_chat ( prompt_msg ):
  model = "text-davinci-003"
  # model = "code-davinci-002"
  # model = "gpt-3.5-turbo"
  # model = "babbage"
  # model = "ada"
  try:
    openai_resp = openai.Completion.create(
      engine=model,
      prompt=prompt_msg,
      max_tokens=900,
      temperature=0.5,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
      )
    ai_answer = openai_resp['choices'][0]['text']
    if 'choices' in openai_resp:
        if len(openai_resp['choices']) > 0:
            ai_answer = openai_resp['choices'][0]['text']
        else:
            ai_answer = 'Opps sorry, you beat the AI this time1'
    else:
        ai_answer = 'Opps sorry, you beat the AI this time2'
  except Exception:
    ai_answer = 'Opps sorry, you beat the AI this time ' + traceback.format_exc()
  return ai_answer