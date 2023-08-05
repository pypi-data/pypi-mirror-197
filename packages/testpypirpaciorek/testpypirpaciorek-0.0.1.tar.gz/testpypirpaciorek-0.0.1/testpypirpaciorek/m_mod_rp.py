import numpy

def name(first, last):
    """Returns full data of parameters"""

    full= first + " " + last
    return full.title()

def get_numpy_arr(lst):
    """Returns array of numppy package"""

    return numpy.array(lst)

if __name__=="__main__":
    print("Rafał", "Paciorek")
    print(get_numpy_arr([1,2,3,4,5]))