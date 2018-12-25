import logging

from actions import init_args, define_user, user_action

logger = logging.getLogger(__name__)
logfile = "coffee_shop_log.log"

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.info("Program started!")
    cmd_args = init_args()
    user = define_user(cmd_args.position, cmd_args.name)
    user_action(cmd_args, user)
    logger.info("Program finished!")
