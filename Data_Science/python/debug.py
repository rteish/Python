import logging

logging.basicConfig(level=logging.DEBUG)

def calculate_total(price, tax_rate):
    logging.debug(f"debug: price={price}, tax_rate={tax_rate}")
    total = price + (price * tax_rate)
    logging.debug(f"debug: total={total}")
    return total

calculate_total(100, 0.1)