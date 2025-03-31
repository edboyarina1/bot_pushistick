from src.utils import load_config
from src.bot import create_bot

def main():
    config = load_config()

    bot = create_bot(config)
    bot.polling(none_stop=True, interval=0, timeout=123)

if __name__ == "__main__":
    main()

    