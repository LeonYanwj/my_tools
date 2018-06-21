class PageInfo(object):
    def __init__(self,current_page,per_page_num,all_count,base_url,page_range=7):
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = int(1)
        self.current_page = current_page
        self.per_page_num = per_page_num
        self.all_count = all_count
        a,b = divmod(all_count,per_page_num)
        if b != 0:
            #self.all_page 是总页数
            self.all_page = a + 1
        else:
            self.all_count = a
        self.base_url = base_url
        self.page_range = page_range

    def start(self):
        return (self.current_page - 1) * self.per_page_num


    def end(self):
        return self.current_page * self.per_page_num

    def page_str(self):
        """
        在HTML页面中显示页码信息
        :return:
        """

        page_list = []
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            prev = '<li><a href="%s?p=%s">上一页</a></li>'%(self.base_url, self.current_page-1)
        page_list.append(prev)


        if self.all_page <= self.page_range:
            start = 1
            end = self.all_page + 1
        else:
            if self.current_page > int(self.page_range / 2):
                if self.current_page + int(self.page_range / 2) > self.all_page:
                    start = self.all_page - self.page_range + 1
                    end = self.all_page + 1
                else:
                    start = self.current_page - int(self.page_range / 2)
                    end = self.current_page + int(self.page_range / 2) + 1
            else:
                start = 1
                end = self.page_range
        for i in range(start,end):
            tmp = '<li><a href="%s?p=%s">%s</a></li>'%(self.base_url,i,i)
            page_list.append(tmp)

        if self.current_page >= self.all_page:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            nex = '<li><a href="%s?p=%s">下一页</a></li>'%(self.base_url, self.current_page+1)
        page_list.append(nex)
        # tmp = """
        # <a href='/app02/page1?p=%s'>上一页</a>
        # <a href='/app02/page1?p=%s'>下一页</a>
        # """%(self.current_page-1,self.current_page+1)

        return " ".join(page_list)