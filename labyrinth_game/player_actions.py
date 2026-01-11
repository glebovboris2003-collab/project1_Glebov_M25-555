# labyrinth_game/player_actions.py
from .constants import ROOMS
from .utils import attempt_open_treasure, describe_current_room, random_event


# Функция отображения инвентаря
def show_inventory(game_state: dict) -> None:
  '''
  game_state - текущее состояние игры
  '''
  if len(game_state['player_inventory']) > 0:
    print(f"Инвентарь игрока: {game_state['player_inventory']}")
  else:
    print("Инвентарь пуст")
    
# Функция получения ввода с клавиатуры
def get_input(prompt="\n> ") -> str:
  '''
  promt - как будет отображаться строка ввода пользователя
  '''
  try:
    return input(prompt)
  except (KeyboardInterrupt, EOFError):
    print("\nВыход из игры.")
    return "quit"

# Функция движения игрока по комнатам
def move_player(game_state: dict, direction: str) -> None:
  '''
  game_state - текущее состояние игры,
  direction - направление
  '''
  if direction in ROOMS[game_state['current_room']]['exits']:
    
    if ROOMS[game_state['current_room']]['exits'][direction] == "treasure_room":
      if "rusty_key" in game_state['player_inventory']:
      
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        game_state['current_room'] = ROOMS[game_state['current_room']]['exits'][direction] # noqa: E501
        game_state['steps_taken'] += 1
        describe_current_room(game_state=game_state)
        
      else:
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        
    else:
      game_state['current_room'] = ROOMS[game_state['current_room']]['exits'][direction] # noqa: E501
      game_state['steps_taken'] += 1
      describe_current_room(game_state=game_state)
    
    random_event(game_state=game_state)
    
  else:
    print("Нельзя пойти в этом направлении.")

# Функция поднятия предмета игроком
def take_item(game_state: dict, item_name: str) -> None:
  '''
  game_state - текущее состояние игры,
  item_name - название предмета
  '''
  if item_name in ROOMS[game_state['current_room']]['items']:
  
    if item_name == "treasure_chest":
      print("Вы не можете поднять сундук, он слишком тяжелый.")
    
    else:
      game_state['player_inventory'].append(item_name)
      ROOMS[game_state['current_room']]['items'].remove(item_name)
      print(f"Вы подняли: {item_name}")
    
  else:
    print("Такого предмета здесь нет.")

# Функция использования предмета
def use_item(game_state: dict, item_name: str) -> None:
  '''
  game_state - текущее состояние игры,
  item_name - название предмета
  '''
  if item_name in game_state['player_inventory']:
  
    if item_name == "torch":
      print("В помещении стало светлее.")
      
    elif item_name == "sword":
      print("Вы чувствуете небывалый прилив уверенности.")
      
    elif item_name == "bronze_box":
      print("Вы открыли шкатулку и получили таинственный ключ.")
      game_state['player_inventory'].remove('bronze_box')
      
      if "treasure_key" not in game_state['player_inventory']:
        game_state['player_inventory'].append('treasure_key')
    
    elif item_name == "old_armor":
      print("У вас есть старые доспехи, они помогут вам в трудную минуту.")
    
    elif item_name == "treasure_key":
      if game_state['current_room'] == 'treasure_room':
        attempt_open_treasure(game_state=game_state)
        
      else:
        print(f"Нельзя использовать {item_name} в этой комнате.")
    
    elif item_name == "old_note":
      print("Вы читаете старую записку:")
      print("В этом замке очень неспокойно... Опасайся ловушек.")
    
    else:
      print("Вы не знаете, что с этим делать.")
  
  else:
    print("У вас в инвентаре нет такого предмета.")

        