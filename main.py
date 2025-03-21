from src.bot import create_bot

def main():
    # cfg = yaml.read ...
    # cfg = cfg[cfg['mode']]

    bot = create_bot()
    bot.polling()
if __name__ == "__main__":
    main()

    