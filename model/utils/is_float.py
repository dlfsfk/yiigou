def is_fioat(s):
    s=str(s)
    if s.count(".")==1:#小数点个数
        s_list=s.split(".")
        left = s_list[0]#小数点左边
        right =s_list[1]#小数点右边
        if left.isdigit() and right.isdigit():
            return  True
        elif left.startswith('-') and left.count('-')==1 and left.split('-')[1].isdigit()and right.isdigit():
            return  True
    return  False