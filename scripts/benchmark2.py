def concat(len_list=1000):
    l = []
    for i in range(len_list):
        l = l + [i]
    return l 
    
def test_concat(benchmark):

    len_list = 1000 
    res = benchmark.pedantic(concat, kwargs={'len_list': len_list}, iterations=100)
    assert res == list(range(len_list))
