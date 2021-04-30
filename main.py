import mysql.connector
from tabulate import tabulate

con = mysql.connector.connect(host="localhost", user="root", password="123456789", database="stock_business")


def view_stock():
    cur = con.cursor()
    q = "SELECT * FROM stock"
    cur.execute(q)
    data = cur.fetchall()
    print(tabulate(data, headers=["ID", "CEREALS", "QUANTITY", "AVG. COST PRICE"]))
    main()


def view_finance():
    cur = con.cursor()
    q = "SELECT * FROM finance"
    cur.execute(q)
    data = cur.fetchall()
    print(tabulate(data, headers=["ID", "COST PRICE", "PROFIT/LOSS", "STATUS"]))
    main()


def buy_cereal():
    i = input("Enter ID of cereal: ")
    data = (i,)
    quantity = int(input("Enter quantity: "))
    pc = float(input("Enter purchase cost: "))
    cur = con.cursor()
    q = "SELECT cost_price,quantity FROM stock WHERE ID=%s"
    cur.execute(q, data)
    x = cur.fetchone()
    cp = x[0]
    net_quantity = x[1]
    cp = (pc * quantity + cp * net_quantity) / (quantity + net_quantity)
    data1 = (cp, quantity, i)
    data2 = (cp, i)
    q1 = "UPDATE stock SET cost_price=%s,quantity=%s+quantity WHERE ID=%s"
    q2 = "UPDATE finance SET cost_price=%s WHERE ID=%s"
    cur.execute(q1, data1)
    cur.execute(q2, data2)
    con.commit()
    main()


def sell_cereal():
    i = input("Enter ID of cereal: ")
    quantity = int(input("Enter quantity: "))
    sp = float(input("Enter selling price: "))
    data = (i,)
    q = "SELECT cost_price,quantity FROM stock WHERE ID=%s"
    cur = con.cursor()
    cur.execute(q, data)
    x = cur.fetchone()
    net_quantity = x[1]
    cp = x[0]
    status = 'N'
    if net_quantity - quantity < 0 or net_quantity == 0:
        print("Stock not available")
    else:
        q1 = "UPDATE stock SET quantity=quantity-%s WHERE ID=%s"
        q2 = "UPDATE finance SET profit_loss=profit_loss+(%s-%s)*%s WHERE ID=%s"
        data1 = (quantity, i)
        data2 = (sp, cp, quantity, i)
        cur.execute(q1, data1)
        cur.execute(q2, data2)
        con.commit()
        q2 = "SELECT profit_loss FROM finance WHERE ID=%s"
        data2 = (i,)
        cur.execute(q2, data2)
        x = cur.fetchone()
        s = x[0]
        if s < 0:
            status = 'L'
        elif s > 0:
            status = 'P'
        q2 = "UPDATE finance SET status=%s WHERE ID=%s"
        data2 = (status, i)
        cur.execute(q2, data2)
        con.commit()
        print(i, " sold successfully")
    if net_quantity - quantity == 0:
        q1 = "UPDATE stock SET cost_price=0 WHERE ID=%s"
        q2 = "UPDATE finance SET cost_price=0 WHERE ID=%s"
        data = (i,)
        cur.execute(q1, data)
        cur.execute(q2, data)
        con.commit()
    main()


def add_cereal():
    i = input("Enter ID of new cereal: ")
    name = input("Enter name of cereal: ")
    quantity = input("Enter quantity: ")
    pc = float(input("Enter purchase cost: "))
    data1 = (i, name, quantity, pc)
    data2 = (i, 0, 0, 'N')
    q1 = "INSERT INTO stock VALUES(%s,%s,%s,%s)"
    q2 = "INSERT INTO finance VALUES(%s,%s,%s,%s)"
    cur = con.cursor()
    cur.execute(q1, data1)
    cur.execute(q2, data2)
    con.commit()
    print(name, " added successfully")
    main()


def remove_cereal():
    i = input("Enter ID of cereal to be deleted: ")
    data = (i,)
    q = "DELETE FROM stock WHERE id=%s"
    cur = con.cursor()
    cur.execute(q, data)
    con.commit()
    print(i, " removed successfully")
    main()


def main():
    print("""
                        **********  B A L A J I--S T O C K--T R A D E R S  ********** 
+---------------+----------------+--------------+---------------+------------------+------------------+--------+
|  1.VIEW STOCK | 2.VIEW FINANCE | 3.BUY CEREAL | 4.SELL CEREAL | 5.ADD NEW CEREAL | 6.REMOVE CEREAL  | 7.EXIT |              
+---------------+----------------+--------------+---------------+------------------+------------------+--------+                            
                 
    """)
    choice = input("Enter Choice: ")
    if choice == '1':
        view_stock()
    elif choice == '2':
        view_finance()
    elif choice == '3':
        buy_cereal()
    elif choice == '4':
        sell_cereal()
    elif choice == '5':
        add_cereal()
    elif choice == '6':
        remove_cereal()
    elif choice == '7':
        exit(0)
    else:
        print("Wrong Choice")
        main()


def password():
    p = input("Enter Password: ")
    if p == "1234":
        main()
    else:
        password()


password()
