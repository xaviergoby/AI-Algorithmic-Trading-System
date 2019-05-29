import os
from data_loader.download_stocks_basket_data import StockDataBasket

def get_hdf_data(rel_path_file_name):
    parent_dir_name = ".." + "/" + rel_path_file_name.split('/')[0]
    file_rel_path = rel_path_file_name.split('/')[1]
    full_file_name = os.path.join(os.path.abspath(parent_dir_name), file_rel_path)
    my_data_dict = StockDataBasket().load_specific_stock_basket_data(full_file_name)
    return my_data_dict


if __name__ == "__main__":
    res = get_hdf_data("data/Semiconductors_stocks_data_01-06-2014_05-21-2019")
    print("get_hdf_data returned: ", res)
    print(type(res))
