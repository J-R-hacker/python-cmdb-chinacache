#this py get node of network id etc.
class get_subnet:
    def __init__(self, hosts):
        self.hosts = hosts

    def masktranspot(self, slenth):
        len_dict, mask_dict = {}, {}
        for lenth in range (1,33):
            subnetlen = lenth
            list = [2**8-1 for i in range (0,subnetlen/8)]
            if len(list) != 4:
                list.append(256-2**(8-subnetlen%8))
            for i in range (0,4-len(list)):
                list.append(0)
            for i in range (0,4):
                list[i] = str(list[i])
            len_dict[subnetlen] = '.'.join(list)
            mask_dict['.'.join(list)] = subnetlen
        result = re.search(r'\w+.\w+.\w+.\w+', slenth)
        if result:
            return mask_dict[slenth]
        else:
            return len_dict[int(slenth)]

    def get_subnet_id():

        pass

    def get_subnet_range():

        pass

    def host_num():

        pass