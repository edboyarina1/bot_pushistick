import yaml
from src.bot import create_bot

def main():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    mode = config['mode']
    config = config[mode]

    bot = create_bot(config)
    bot.polling()

if __name__ == "__main__":
    main()

    