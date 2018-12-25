import argparse
import logging

from prettytable import PrettyTable

from db_handler import DatabaseHandler
from models import *
from utils import cls

YES = "y"
QUIT = "q"
COFFEE_DB = DatabaseHandler("sqlite:///coffeeDB")

logger = logging.getLogger(__name__)
logfile = "coffee_shop_log.log"

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def init_args():
    """
    Initializes commandline arguments. Defines expected arguments. May cause parser errors in case of wrong arguments.
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='This utility helps to manage work of CoffeeShop')

    parser.add_argument('--name', type=str, help='An optional str argument with name of user')

    parser.add_argument('--position', type=str,
                        help='An optional str argument with position of user (salesman or manager)')

    parser.add_argument('--beverage', type=str,
                        help='An optional str argument with beverage to sell (available for salesman)')

    parser.add_argument('--ingredient', type=str,
                        help='An optional argument with ingredient to sell (available for salesman)')

    parser.add_argument('--save_bill', type=str,
                        help='An optional str argument with file to save bill (available for salesman)',
                        metavar="FILE_TO_SAVE")

    args = parser.parse_args()
    logger.info(
        "Initializing of commandline arguments: "
        " --name: {} --position: {} --beverage: {} --ingredient: {} --save_bill: {}".format(args.name,
                                                                                            args.position,
                                                                                            args.beverage,
                                                                                            args.ingredient,
                                                                                            args.save_bill,
                                                                                            ))
    validate_args(args, parser)
    return args


def validate_args(args, parser):
    """
    Validates commandline arguments
    :param args: command line arguments
    :param parser: ArgumentParser object
    """
    if args.position == UserType.MANAGER.name.lower() and (
            args.beverage is not None
            or args.ingredient is not None
            or args.save_bill is not None):
        logger.error("Unavailable action for manager was used")
        parser.error("You used unavailable action for manager")

    elif args.position is None and (
            args.beverage is not None
            or args.ingredient is not None
            or args.save_bill is not None):
        logger.error("Unavailable action was used for not chosen position")
        parser.error("You used unavailable action. You should choose position to do chosen action(s)")

    elif (args.position is not None and args.position != UserType.MANAGER.name.lower()
          and args.position != UserType.SALESMAN.name.lower()):
        logger.error(
            "Unavailable user position was chosen. Available positions: manager, salesman. Except got {}".format(
                args.position))
        parser.error("Unavailable user position. Available positions: manager, salesman")


def who_are_you(position):
    """
    Gives a list of users with given position.
    :param position: position of user
    :return:Salesman or Manager object
    """
    users = COFFEE_DB.get_all(position)
    while True:
        cls()
        print("Who are you? (q - for quiet or cancel)")
        for number, user in enumerate(users):
            print("{} {}".format(number + 1, user))
        print("0 create new account")
        choice = input("->")
        if choice == QUIT:
            raise SystemExit
        if not choice.isdigit() or int(choice) > len(users):
            continue
        elif int(choice) == 0:
            cls()
            return create_new_account(position)
        else:
            user = users[int(choice) - 1]
            logger.info("{} {} is chosen".format(position.name.lower(), user.name))
            return user


def create_account_with_new_name(position):
    """
    Creates account and requires to enter new name
    :param position: position of user
    :return:Salesman or Manager object
    """
    while True:
        name = input("Name of new {}: ".format(position.name.lower()))
        if name == QUIT:
            return who_are_you(position)
        user = position.value(name)
        if COFFEE_DB.get_by_name(position, user.name) is not None:
            print("user already exists")
        else:
            COFFEE_DB.add(user)
            return user


def create_account_with_given_name(position, name):
    """
    Offers to create new account with given name
    :param position: position of user
    :param name: name of user
    :return:Salesman or Manager object
    """
    print(
        "{} with name {} not found! do you want to create it? (y/n)".format(position.name.lower(), name))
    choice = input()
    if choice == YES:
        user = position.value(name)
        COFFEE_DB.add(user)
        return user
    else:
        return None


def create_new_account(position, name=None):
    """
    creates new account of given position
    :param position: position of user
    :param name: name of user
    :return:Salesman or Manager object
    """
    while True:
        if name is None:
            return create_account_with_new_name(position)
        else:
            return create_account_with_given_name(position, name)


def choose_position():
    """
    Requires to choose users position
    :return: UserType object with chosen position type
    """
    while True:
        cls()
        print("Who are you?\n"
              "    1 Salesman\n"
              "    2 Manager")
        choice = input("->")
        if choice.isdigit() and int(choice) == 1:
            logger.info("Salesman position was chosen")
            return UserType.SALESMAN
        elif choice.isdigit() and int(choice) == 2:
            logger.info("Manager position was chosen")
            return UserType.MANAGER
        elif choice == QUIT:
            logger.info("Exit from the program!")
            raise SystemExit


def get_user(position, name):
    """
    Get user by name and position
    :param position: user position
    :param name: user name
    :return:Salesman or Manager object
    """
    if name is None:
        return who_are_you(position)
    else:
        user = position.value(name)
        if COFFEE_DB.get_by_name(position, user.name) is None and create_new_account(position, user.name) is None:
            logger.info("Exit from the program, because user name \"{} \" not found and user dont "
                        "want to create new account with this name".format(user.name))
            raise SystemExit
        return user


def define_user(position, name):
    """
    Defines user, who uses this app
    :param position: user position
    :param name:user name
    :return:Salesman or Manager object
    """
    if position == UserType.SALESMAN.name.lower() or position == UserType.MANAGER.name.lower():
        position = UserType[position.upper()]
        return get_user(position, name)
    elif position is None:
        position = choose_position()
        return get_user(position, name)


def choose_product(product_type):
    """
    Allows to choose product from the list
    :param product_type: ProductType object
    :return: chosen product
    """
    products = COFFEE_DB.get_all(product_type)
    while True:
        cls()
        print("Choose(q - for quiet or cancel)")
        for number, product in enumerate(products):
            print("{} {}".format(number + 1, product))
        choice = input("->")
        if choice == QUIT:
            logger.info("Exit from the program!")
            raise SystemExit
        if not choice.isdigit() or int(choice) > len(products):
            continue
        else:
            chosen_product = products[int(choice) - 1]
            logger.info("{} \"{}\" was chosen".format(product_type.name.lower().capitalize(), chosen_product.name))
            return chosen_product


def define_beverage(beverage):
    """
    Defines beverage to sell
    :param beverage: chosen beverage
    :return: Beverage object
    """
    if beverage is None:
        return choose_product(ProductType.BEVERAGE)
    else:
        beverage = COFFEE_DB.get_by_name(ProductType.BEVERAGE, beverage)
        if beverage is not None:
            return beverage
        else:
            print("There are no in menu such beverage")
            logger.exception("Exit from the program, because unavailable beverage was chosen.")
            raise SystemExit


def define_ingredient(ingredient):
    """
    Defines ingredient to sell
    :param ingredient: chosen ingredient
    :return: Ingredient object
    """
    if ingredient is None:
        print("Do you want to add ingredient?(y/n)")
        answer = input("->")
        if answer == YES:
            return choose_product(ProductType.INGREDIENT)
        else:
            return None
    else:
        founded_ingredient = COFFEE_DB.get_by_name(ProductType.INGREDIENT, ingredient)
        if founded_ingredient is None:
            print("There are no in menu such ingredient")
            logger.exception("Exit from the program, because unavailable ingredient was chosen.")
            raise SystemExit
        else:
            return founded_ingredient


def create_report(file_name, sale):
    """
    Creates sell report
    :param file_name: name of file to save the report
    :param sale: Sale object
    """
    with open(file_name, 'w+') as report:
        report.write(str(sale))
        logger.info("Saving sell bill into file {}.".format(file_name))


def show_statistics():
    """
    Shows statistics of sales in table format
    """
    salesmen = COFFEE_DB.get_all(UserType.SALESMAN)
    table = PrettyTable(['Salesman', 'Number of sales', "Total Value ($)"])
    for salesman in salesmen:
        sales = COFFEE_DB.get_sales_by_salesman(salesman)
        total_sum = sum(sale.price for sale in sales)
        table.add_row(list((salesman, len(sales), total_sum)))
    print(table)
    logger.info("Showing statistics of sells.")


def salesman_action(cmd_args, salesman):
    """
    Handles actions of salesman
    :param cmd_args: commandline arguments
    :param salesman: Salesman object
    """
    beverage = define_beverage(cmd_args.beverage)
    ingredient = define_ingredient(cmd_args.ingredient)
    sale = Sale(salesman=salesman, beverage=beverage, ingredient=ingredient)
    COFFEE_DB.add(sale)
    if cmd_args.save_bill is not None:
        file_name = cmd_args.save_bill
        create_report(file_name, sale)
    else:
        print("Do you want to create a bill? (y/n)")
        answer = input("->")
        if answer == YES:
            file_name = input("Enter file to save bill: ")
            create_report(file_name, sale)
            print("Report was created successfully")
        else:
            raise SystemExit


def user_action(cmd_args, user):
    """
    Defines what to do in dependence of user position
    :param cmd_args: commandline arguments
    :param user: Salesman or Manager object
    """
    if isinstance(user, Salesman):
        salesman_action(cmd_args, user)
    if isinstance(user, Manager):
        show_statistics()
