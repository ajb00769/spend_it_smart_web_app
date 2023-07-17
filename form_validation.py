def validate_form_inputs(category, subcat, amount):
    form_category = ['purchase', 'sell', 'income', 'invest', 'debt']
    form_purchase_sub = ['snacks', 'groceries', 'resto', 'clothing',
                         'shoes', 'bags', 'luxury', 'electronics', 'utilities', 'transpo']
    form_sell_sub = ['oldelectronics', 'oldfurniture',
                     'oldclothes', 'oldshoes', 'oldbags', 'oldluxury']
    form_income_sub = ['salary', 'businesssvc', 'businesssku', 'allowance']
    form_invest_sub = ['stocks', 'bonds', 'mfund',
                       'insurance', 'crypto', 'preciousmetals']
    form_debt_sub = ['studentloan', 'salaryloan', 'carloan', 'mortgage']

    if category and subcat and amount:
        if amount.isdigit() and int(amount) > 0:
            if category == form_category[0] and subcat in form_purchase_sub:
                return True
            elif category == form_category[1] and subcat in form_sell_sub:
                return True
            elif category == form_category[2] and subcat in form_income_sub:
                return True
            elif category == form_category[3] and subcat in form_invest_sub:
                return True
            elif category == form_category[4] and subcat in form_debt_sub:
                return True
    return False
