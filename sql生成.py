for i in range(1,40):
        if i<10:
                print('delete from oiw0{}.dbo.ashare_cjhb;\n'
                'delete from oiw0{}.dbo.ashare_ordwth;\n'
                'delete from oiw0{}.dbo.ashare_ordwth2;\n'
                'delete from oiw0{}.dbo.reqresp;\n'
                'delete from oiw0{}.dbo.ashare_cjhb_etf;\n'
                'delete from oiw0{}.dbo.exerpt;\n'
                'delete from oiw0{}.dbo.execreport;\n'
                'delete from oiw0{}.dbo.orders;\n'
                'delete from oiw0{}.dbo.pubdata;\n'.format(i,i,i,i,i,i,i,i,i))
        else:
                print('delete from oiw{}.dbo.ashare_cjhb;\n'
                'delete from oiw{}.dbo.ashare_ordwth;\n'
                'delete from oiw{}.dbo.ashare_ordwth2;\n'
                'delete from oiw{}.dbo.reqresp;\n'
                'delete from oiw{}.dbo.ashare_cjhb_etf;\n'
                'delete from oiw{}.dbo.exerpt;\n'
                'delete from oiw{}.dbo.execreport;\n'
                'delete from oiw{}.dbo.orders;\n'
                'delete from oiw{}.dbo.pubdata;\n'.format(i,i,i,i,i,i,i,i,i))