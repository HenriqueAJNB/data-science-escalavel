def concat(len_list=1000):
    l = []
    for i in range(len_list):
        l = l + [i]
    return l 
    
def test_concat(benchmark):

    res = benchmark(concat)
