import os

# os.environ['OPENAI_KEY'] = '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'
# os.environ['TELE_TOKEN1'] = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
# os.environ['OWM_TOKEN'] = 'f70b2868746d0a1f0c27740e7031549a'

# os.environ['HOME'] = '888'

# Создаём цикл, чтобы вывести все переменные среды
print('The keys and values of all environment variables:')
for key in os.environ:
    print(key, '= > ', os.environ[key])
    # Выводим значение одной переменной
    # print('The value of HOME is: ', os.environ['HOME'])
