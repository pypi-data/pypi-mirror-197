"""mytools.py - Tools for working with functions and callable objects
"""

__all__ = ["expansion", "expansion_up"]

################################################################################
### expansion() and expansion_up() function
################################################################################


def expansion_up(array: list or tuple) -> list:
    """
    生成器实现列表扁平化方法，提升性能，适合大并多维度的列表操作
    :param array: 多维数据
    :return: 返回多维列表展开后的一维列表
    """
    def flatten(items: list):
        """
        扁平操作， 通过生成器让递归调用编程普通调用
        :param items: ...
        """
        for item in items:
            if type(item) is list or type(item) is tuple:
                yield from flatten(item)
            else:
                yield item

    return [fla for fla in flatten(array)]


def expansion(array: list or tuple, result: list or tuple = None) -> list:
    """
    递归实现列表扁平化方法， 调用栈过多可能造成程序性能下降
    :param array:  多维列表
    :param result:  默认参数， 一般不用传
    :return: 返回多维列表展开后的一维列表， 若传入参数 result， 则返回  一维array + result
    """
    if result is None:
        result = []
    for arr in array:
        if type(arr) is list or type(arr) is tuple:
            expansion(arr, result)
        else:
            result.append(arr)
    return result