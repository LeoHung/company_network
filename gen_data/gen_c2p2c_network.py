#encoding=utf8
import json
import sys
def gen_b2b_network(c2p2c_filename, index_output_filename, b2b_output_filename):
    b2b_network = {}
    # read index
    index2detail = {}
    for l in open(index_output_filename):
        detail_data = json.loads(l)
        index2detail[detail_data[u'公司編號']] = detail_data

    for l in open(c2p2c_filename):
        c2p2c = json.loads(l)
        if c2p2c.get(u'所代表法人') :
            if index2detail.get(c2p2c.get(u'被投資公司編號')) and index2detail.get(c2p2c.get(u'所代表法人')):
                invested_company = unicode(index2detail.get(c2p2c.get(u'被投資公司編號')).get(u'公司名稱'))
                invest_company = unicode(index2detail.get(c2p2c.get(u'所代表法人')).get(u'公司名稱'))
                print invested_company, invest_company
                if not b2b_network.has_key((invest_company, invested_company)):
                    b2b_network[ (invest_company, invested_company) ] = 0
                if c2p2c.get(u'出資額'):
                    b2b_network[ (invest_company, invested_company) ] += c2p2c.get(u'出資額')

    output_data = [(keys[0], keys[1], value) for keys, value in b2b_network.items()]

    try:
        json.dump(fp=open(b2b_output_filename,'w'), obj=output_data, ensure_ascii=False, indent=4)
    except:
        json.dump(fp=open(b2b_output_filename,'w'), obj=output_data, indent=4)

def gen(input_filenames, c2p2c_output_filename, index_output_filename):
    """
        transform g0v.company raw data into index2company and c2p2c graph input_files
    """
    c2p2c_out = open(c2p2c_output_filename, 'w')
    index_out = open(index_output_filename, 'w')

    for filename in input_filenames:
        f = open(filename)
        for l in f:
            l = l.decode("utf8")
            tmp = l.split(",", 1)
            if len(tmp) == 2 :
                index, detail = tmp
                index = int(index)
                detail = json.loads(detail)
                # print index_out
                index_data = {u"公司編號":index}
                index_fields = [u"公司名稱", u"代表人姓名"]
                for index_field in index_fields:
                    index_data[index_field] = detail.get(index_field)
                index_int_fields = [u"資本總額(元)", u"實收資本額(元)"]
                for index_int_field in index_int_fields:
                    if detail.get(index_int_field):
                        index_data[index_int_field] = int(detail.get(index_int_field).replace(",",""))
                print >> index_out, json.dumps(index_data)
                # print c2p2c
                if detail.get(u"董監事名單") and len(detail.get(u"董監事名單")) > 0:
                    for person_item in detail.get(u"董監事名單"):
                        c2p2c_data = {}
                        c2p2c_fields = [u'職稱', u'姓名']
                        for c2p2c_field in c2p2c_fields:
                            c2p2c_data[c2p2c_field] = person_item.get(c2p2c_field).strip()
                        c2p2c_int_fields = [u'出資額']
                        for c2p2c_int_field in c2p2c_int_fields:
                            if person_item.get(c2p2c_int_field):
                                c2p2c_data[c2p2c_int_field] = int(person_item.get(c2p2c_int_field).replace(",",""))
                        if person_item.get(u'所代表法人') and len(person_item.get(u'所代表法人'))>0:
                            if person_item[u'所代表法人'][0] == 0: ## wrong index
                                continue
                            else:
                                c2p2c_data[u'所代表法人'] = int(person_item[u'所代表法人'][0])
                        c2p2c_data[u'被投資公司編號'] = index
                        print json.dumps(c2p2c_data, ensure_ascii=False)
                        print >> c2p2c_out, json.dumps(c2p2c_data)
    index_out.close()
    c2p2c_out.close()
