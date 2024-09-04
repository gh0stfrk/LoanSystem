def minimize_loss(n, price):
    min_loss = float('inf')
    best_buy_year = -1
    best_sell_year = -1

    for i in range(n):
        for j in range(i + 1, n):
            if price[i] > price[j]:
                loss = price[i] - price[j]
                if loss < min_loss:
                    min_loss = loss
                    best_buy_year = i
                    best_sell_year = j

    if min_loss == float('inf'):
        return -1, -1, -1
    else:
        return best_buy_year + 1, best_sell_year + 1, min_loss

    



if __name__ == "__main__":
    number_of_years = 5
    price = [20, 15, 7, 2, 13]
    
    buy, sell, loss = minimize_loss(number_of_years ,price)

    print(f"Buy at {buy}, sell at {sell} for a minimum loss of {loss}")