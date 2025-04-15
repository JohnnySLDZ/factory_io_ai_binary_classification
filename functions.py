from opcua import Client, ua
  
def write_value_int(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_bool(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_float(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = float(value)
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Float))  
    client_node.set_value(client_node_dv) 
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))

def read_input_value(client, node_id):
    client_node = client.get_node(node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    return client_node_value

def new_round(num):
    decimal_part = num - int(num) 
    if decimal_part >= 0.75:
        return int(num) + 1  
    else:
        return int(num)
    
if __name__ == "__main__":

    client_test = Client("opc.tcp://192.168.0.1:4840")
    try:
        client_test.connect()

        root = client_test.get_root_node()
        print("Objects root node is: ", root)

        # read_input_value(client_test, 'ns=3;s="CONFIG_VARS"."MOVE_2_BOX"')
        # read_input_value(client_test, 'ns=3;s="CONFIG_VARS"."INSTRUCTION_2_PY"')

        # write_value_bool(client_test, 'ns=3;s="CONFIG_VARS"."PY_RESPONSE"', True)
        # write_value_int(client_test, 'ns=3;s="COORDS"."CODE"', 25)


    finally:
        client_test.disconnect()
